# ARD Audiothek Provider

This is a simple custom metadata provider for Audiobookshelf that fetches audiobook information from the [ARD Audiothek](https://www.ardaudiothek.de/) (Audiothek of the public broadcasters in Germany).

## Features
- Fetches metadata from Audiobooks from ARD Audiothek.
- Cover images.
- Title
- Author
- Description
- Publisher
- genre
- language

## Installation
1. Clone or download this repository.
2. Navigate to the directory where the Dockerfile is located.
3. Start the Docker container with the following command:
   ```bash
   docker-compose up --build -d
   ```
4. In Audiobookshelf, go to Settings > Metadata Providers.
5. Add a new custom metadata provider and enter the URL of your running container (e.g., `http://localhost:8000`).

## Limitations
- Only works when the audiobook is available on ARD Audiothek, keep in mind to run the match right after the downloading the audiobook.

