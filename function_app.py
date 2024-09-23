import azure.functions as func
from azure.data.tables import TableServiceClient
from azure.data.tables import UpdateMode
import json
import datetime
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
    callsign = req_body.get('callsign')

    table = get_table()
    entity = query_for_entity(table, callsign)
    messageId = None
    if is_entity_recent(entity):
        messageId = entity['MessageId']
    messageId = call_target(content, messageId)
    upsert_entity(table, callsign, messageId)

    return func.HttpResponse(status_code=202)

def create_content(req_body):
    callsign = req_body.get('callsign', 'Unknown')
    source = req_body.get('source', 'Unknown')
    frequency = req_body.get('frequency', 'Unknown')
    mode = req_body.get('mode', 'Unknown')
    summitRef = req_body.get('summitRef', '')
    wwffRef = req_body.get('wwffRef', '')

    spot_deeplink = create_spot_deeplink(source, callsign, wwffRef)

    # flags = 4 means it will suppress embeds: https://discord.com/developers/docs/resources/message#message-object-message-flags
    content = {"content": f"{callsign} | {source} | freq: {frequency} | mode: {mode} | loc: {summitRef}{wwffRef} | {spot_deeplink}", "flags": 4}
    return content

def call_target(content, messageId=None):
    target_url = os.getenv('TARGET_URL')
    verb = "POST"
    if messageId is not None:
        target_url = target_url + f"/messages/{messageId}"
        verb = "PATCH"
    response = requests.request(verb, url=target_url, params={"wait": "true"}, json=content)
    return extract_message_id(response)
    #return func.HttpResponse(response.text, status_code=response.status_code)

def create_spot_deeplink(source, callsign, wwffRef):
    match source:
        case "sotawatch":
            return f"[See their latest spot](https://sotl.as/activators/{callsign})"
        case "pota":
            return f"[See their latest spot](https://api.pota.app/spot/comments/{callsign}/{wwffRef})"
        case _:
            return ""

def get_table():
    connection_string = os.getenv('AzureWebJobsStorage')
    table_name = os.getenv('TABLE_NAME')
    table_service_client = TableServiceClient.from_connection_string(conn_str=connection_string)
    table_client = table_service_client.get_table_client(table_name=table_name)
    return table_client

def query_for_entity(table_client, callsign):
    entities = [ent for ent in table_client.query_entities(f"PartitionKey eq '{callsign}' and RowKey eq '{callsign}'")]
    if len(entities) > 0:
        logging.info(f"Entity already exists for {callsign}")
    return entities[0] if len(entities) > 0 else None

def is_entity_recent(entity):
    if entity is None:
        return False
    ent_time = entity.metadata['timestamp']
    cur_time = datetime.datetime.now(datetime.timezone.utc)
    two_hours_in_seconds = 60 * 60 * 2
    return (cur_time - ent_time).total_seconds() < two_hours_in_seconds

def upsert_entity(table_client, callsign, messageId):
    entity = {
        u'PartitionKey': callsign,
        u'RowKey': callsign,
        u'MessageId': messageId
    }
    table_client.upsert_entity(mode=UpdateMode.REPLACE, entity=entity)

def extract_message_id(response):
    return response.json()['id']