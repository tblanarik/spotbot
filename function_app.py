import azure.functions as func
import logging
import requests
import os

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="spotbot", methods=[func.HttpMethod.POST])
def spotbot(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = {}

    try:
        req_body = req.get_json()
        logging.info(f"Received JSON: {req_body}")
    except ValueError:
        logging.error('Invalid JSON received')
        return func.HttpResponse("Invalid JSON", status_code=400)

    content = create_content(req_body)
    return call_target(content)

def create_content(req_body):
    fullCallsign = req_body.get('fullCallsign', 'Unknown')
    source = req_body.get('source', 'Unknown')
    frequency = req_body.get('frequency', 'Unknown')
    mode = req_body.get('mode', 'Unknown')
    summitRef = req_body.get('summitRef', '')
    wwffRef = req_body.get('wwffRef', '')

    spot_deeplink = create_spot_deeplink(source, fullCallsign, wwffRef)

    content = {"content": f"{fullCallsign} | {source} | freq: {frequency} | mode: {mode} | loc: {summitRef}{wwffRef} | {spot_deeplink}", "flags": 4}
    return content

def call_target(content):
    target_url = os.getenv('TARGET_URL')
    response = requests.post(target_url, json=content)
    return func.HttpResponse(response.text, status_code=response.status_code)

def create_spot_deeplink(source, fullCallsign, wwffRef):

    match source:
        case "sotawatch":
            return f"[See their latest spot](https://sotl.as/activators/{fullCallsign})"
        case "pota":
            return f"[See their latest spot](https://api.pota.app/spot/comments/{fullCallsign}/{wwffRef})"
        case _:
            return ""