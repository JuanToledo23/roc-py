# ROC API

This is the API for the ROC mobile application.

## Getting Started

### Prerequisites

- [Python 3.12](https://www.python.org/downloads/release/python-3120/)
- [Poetry](https://python-poetry.org/docs/#installation)
- [Docker](https://docs.docker.com/get-docker/)

### Installation

1. Clone the repo
   ```sh
   git clone
    ```
2. Install dependencies with poetry
   ```sh
   poetry install
   ```
3. Run the database
   ```sh
   docker compose up -d
   ```
4. Run the server
    ```sh
    poetry run uvicorn app.main:app --reload
    ```
