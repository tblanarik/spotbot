import azure.functions as func
import requests
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    content = req.get_json()
    target_url = os.getenv('TARGET_URL')
    if not target_url:
        return func.HttpResponse("Error: TARGET_URL environment variable is not set.", status_code=500)
    response = requests.post(target_url, json=content)
    return func.HttpResponse(response.text, status_code=response.status_code)
