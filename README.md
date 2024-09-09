# spotbot

## Description

Spotbot is a simple webserver that listens for HTTP POST requests and forwards the content of those requests to another URL via another HTTP POST request. It is built using Flask.

## Requirements

- Python 3.x
- Flask
- requests

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/tblanarik/spotbot.git
   cd spotbot
   ```

2. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Running the Webserver

To run the webserver, execute the following command:
```sh
python spotbot.py
```

The webserver will start and listen on port 5000.

## Sending a POST Request to the `/forward` Endpoint

To send a POST request to the `/forward` endpoint, you can use a tool like `curl` or Postman. Here is an example using `curl`:

```sh
curl -X POST http://localhost:5000/forward -H "Content-Type: application/json" -d '{"key": "value"}'
```

Replace `{"key": "value"}` with the actual JSON content you want to send.

## Running the Webserver using Docker

To run the webserver using Docker, follow these steps:

1. Build the Docker image:
   ```sh
   docker build -t spotbot .
   ```

2. Run the Docker container:
   ```sh
   docker run -p 5000:5000 spotbot
   ```

The webserver will start and listen on port 5000 inside the Docker container.
