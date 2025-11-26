# ARD Audiothek Provider

This project provides an API to search for audiobooks and radio plays from the ARD Audiothek. It is designed to be used as a metadata provider for **Audiobookshelf**.

## Usage with Audiobookshelf

This service acts as a bridge between Audiobookshelf and the ARD Audiothek.

1.  **Deploy this service** using Docker (see instructions below).
2.  **Configure Audiobookshelf**:
    *   Ensure this service is reachable from your Audiobookshelf instance (e.g., `http://localhost:8000` or `http://ard-audiothek-provider:8000` if in the same Docker network).
    *   Use the endpoint `/search` for searching books.
    *   Example query: `GET http://localhost:8000/search?query=Harry%20Potter`

## Docker Support

This project is packaged with Docker for easy deployment.

### Prerequisites

- Docker
- Docker Compose

### Running with Docker Compose

1.  Build and start the container:

    ```bash
    docker-compose up --build
    ```

2.  The API will be available at `http://localhost:8000`.

3.  To stop the container:

    ```bash
    docker-compose down
    ```

### Running with Docker directly

1.  Build the image:

    ```bash
    docker build -t ard-audiothek-provider .
    ```

2.  Run the container:

    ```bash
    docker run -p 8000:8000 ard-audiothek-provider
    ```
