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
TARGET_URL=<target_url> DESTINATION_URL=<destination_url> python spotbot.py
```

Replace `<target_url>` with the actual target URL and `<destination_url>` with the desired port number for the Flask app. If `DESTINATION_URL` is not set, the default port will be 5000.

## Sending a POST Request to the `/forward` Endpoint

To send a POST request to the `/forward` endpoint, you can use a tool like `curl` or Postman. Here is an example using `curl`:

```sh
curl -X POST http://localhost:5000/forward -H "Content-Type: application/json" -d '{"key": "value"}'
```

Replace `{"key": "value"}` with the actual JSON content you want to send.

## Deploying and Running the App as an Azure Function App

To deploy and run the app as an Azure Function App, follow these steps:

1. Create an Azure Function App in the Azure portal.

2. Set up the required environment variables in the Azure Function App configuration:
   - `TARGET_URL`: The target URL to which the content will be forwarded.

3. Deploy the app to the Azure Function App using the provided GitHub Actions workflow.

4. Once deployed, you can send POST requests to the Azure Function App endpoint to forward the content to the target URL.
