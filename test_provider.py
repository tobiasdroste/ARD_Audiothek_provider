import requests
import time
import sys

def test_search():
    url = "http://localhost:8000/search"
    params = {"query": "Neurobiest"}
    
    with open("test_output.txt", "w", encoding="utf-8") as f:
        f.write(f"Testing {url} with params {params}...\n")
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            f.write(f"Response status code: {response.status_code}\n")
            f.write(f"Response keys: {list(data.keys())}\n")
            
            if "matches" in data:
                f.write(f"Found {len(data['matches'])} matches.\n")
                if len(data['matches']) > 0:
                    first_match = data['matches'][0]
                    f.write("First match sample:\n")
                    f.write(f"  Title: {first_match.get('title')}\n")
                    f.write(f"  Author: {first_match.get('author')}\n")
                    f.write(f"  Series: {first_match.get('series')}\n")
                    f.write(f"  Cover: {first_match.get('cover')}\n")
            else:
                f.write("ERROR: 'matches' key not found in response.\n")
                
        except requests.RequestException as e:
            f.write(f"Request failed: {e}\n")

if __name__ == "__main__":
    # Wait a bit for server to start if running immediately after
    time.sleep(2) 
    test_search()
