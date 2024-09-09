import azure.functions as func
import logging
import requests
import os

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="spotbot", methods=[func.HttpMethod.POST])
def spotbot(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        fullCallsign = req_body.get('fullCallsign', 'Unknown')
        source = req_body.get('source', 'Unknown')
        frequency = req_body.get('frequency', 'Unknown')
        mode = req_body.get('mode', 'Unknown')
        summitRef = req_body.get('summitRef', '')
        wwffRef = req_body.get('wwffRef', '')

    
    content = {"content": f"{fullCallsign} | {source} | freq: {frequency} | mode: {mode} | loc: {summitRef}{wwffRef}"}

    target_url = os.getenv('TARGET_URL')
    response = requests.post(target_url, json=content)
    return func.HttpResponse(response.text, status_code=response.status_code)