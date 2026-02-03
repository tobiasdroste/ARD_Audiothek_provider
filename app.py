from fastapi import FastAPI, HTTPException, Query
import requests
import logging
from typing import List, Optional
from pydantic import BaseModel

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="ARD Audiothek Metadata Provider", version="0.1.0")

ARD_API_URL = "https://api.ardaudiothek.de/search/programsets"

class SeriesMetadata(BaseModel):
    series: str
    sequence: Optional[str] = None

class BookMetadata(BaseModel):
    title: str
    subtitle: Optional[str] = None
    author: Optional[str] = None
    narrator: Optional[str] = None
    publisher: Optional[str] = None
    publishedYear: Optional[str] = None
    description: Optional[str] = None
    cover: Optional[str] = None
    isbn: Optional[str] = None
    asin: Optional[str] = None
    genres: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    series: Optional[List[SeriesMetadata]] = None
    language: Optional[str] = None
    duration: Optional[int] = None

class SearchResponse(BaseModel):
    matches: List[BookMetadata]

@app.get("/search", response_model=SearchResponse)
def search_books(query: str, author: Optional[str] = None):
    params = {"query": query}
    try:
        response = requests.get(ARD_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching data from ARD Audiothek: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching data from ARD Audiothek: {e}")
    except ValueError as e:
        logger.error(f"Error parsing JSON response from ARD Audiothek: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Invalid JSON response from ARD Audiothek")

    matches = []
    try:
        # Updated path to nodes based on programsets endpoint
        items = data.get("data", {}).get("search", {}).get("programSets", {}).get("nodes", [])

        for item in items:
            try:
                # Extract basic info
                title = item.get("title")
                title = title.replace('„', '').replace('"', '')
                synopsis = item.get("synopsis")
                
                # Duration is not directly available in programSet summary, usually sum of episodes
                # But we don't have that here. We can leave it None or try to fetch details if needed.
                # For now, we'll leave it as None or 0.
                duration = None 
                
                # Publication year is also not directly in the summary node
                published_year = None

                # Extract images
                image_template_url = item.get("image", {}).get("url1X1")
                if not image_template_url:
                    image_template_url = item.get("image", {}).get("url")
                cover_url = image_template_url.replace("{width}", "1200") if image_template_url else None

                # Extract Author from title
                # Pattern often: "Title von Author" or "Author: Title"
                author_name = None
                clean_title = title
                if title:
                    if " von " in title:
                        parts = title.split(" von ")
                        if len(parts) > 1:
                            author_name = parts[1]
                            clean_title = parts[0].strip()
                    elif ":" in title:
                         parts = title.split(":")
                         if len(parts) > 1:
                            author_name = parts[0]
                            clean_title = parts[1].strip()
                
                # In programSet, it's under publicationService -> organizationName
                publisher = item.get("publicationService", {}).get("organizationName") or "ARD"

                # Genres
                genres = []
                genre = item.get("publicationService", {}).get("genre")
                if genre:
                    genres.append(genre)

                # Series Metadata
                # For program sets, the title itself is often the series name
                series_list = []
                
                # We can treat the program set as a series
                series_list.append(SeriesMetadata(series=clean_title, sequence=None))

                book = BookMetadata(
                    title=clean_title,
                    author=author_name,
                    description=synopsis,
                    cover=cover_url,
                    publishedYear=published_year,
                    publisher=publisher,
                    duration=duration,
                    language="de",
                    genres=genres,
                    series=series_list
                )
                matches.append(book)
            except Exception as e:
                logger.warning(f"Error parsing individual item: {e}", exc_info=True)
                # Continue processing other items instead of failing completely
                continue

    except Exception as e:
        logger.error(f"Error processing search results: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error processing search results")

    return SearchResponse(matches=matches)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
