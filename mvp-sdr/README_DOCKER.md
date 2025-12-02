# Running with Docker

## Prerequisites

- Docker installed on your machine.

## Quick Start

1. **Build and Run**:

    ```bash
    docker-compose up --build
    ```

    This will build the image and run `main.py` inside the container.

2. **View Output**:
    The logs will appear in your terminal. You should see `[BrightData] Enriched: ...` and other pipeline logs.

3. **Access Files**:
    The current directory is mounted to `/app` in the container, so `generated_emails.csv` will be updated on your host machine.

## Manual Docker Commands

If you prefer not to use Compose:

1. **Build**:

    ```bash
    docker build -t sdr-agent .
    ```

2. **Run**:

    ```bash
    docker run -v ${PWD}:/app sdr-agent
    ```
