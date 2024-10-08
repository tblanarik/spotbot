import logging
import os
import datetime
import requests
import tables


def run(req):
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()
    logging.info(f"Received JSON: {req_body}")

    callsign = req_body.get('callsign')

    table = tables.get_table()
    entity = tables.query_for_entity(table, callsign)
    messageId = None
    if is_entity_recent(entity):
        messageId = entity['MessageId']
    content = create_content(req_body)
    messageId = call_target(content, messageId)
    tables.upsert_entity(table, callsign, messageId)
    
def create_content(req_body):
    callsign = req_body.get('callsign', 'Unknown')
    source = req_body.get('source', 'Unknown')
    frequency = req_body.get('frequency', 'Unknown')
    mode = req_body.get('mode', 'Unknown')
    summitRef = req_body.get('summitRef', '')
    wwffRef = req_body.get('wwffRef', '')

    spot_deeplink = create_spot_deeplink(source, callsign, wwffRef)

    # flags = 4 means it will suppress embeds: https://discord.com/developers/docs/resources/message#message-object-message-flags
    content = {"content": f"{callsign} | {spot_deeplink} | freq: {frequency} | mode: {mode} | loc: {summitRef}{wwffRef}", "flags": 4}
    return content

def create_spot_deeplink(source, callsign, wwffRef):
    match source:
        case "sotawatch":
            return f"[{source}](https://sotl.as/activators/{callsign})"
        case "pota":
            return f"[{source}](https://api.pota.app/spot/comments/{callsign}/{wwffRef})"
        case _:
            return ""
        
def is_entity_recent(entity):
    if entity is None:
        return False
    ent_time = entity.metadata['timestamp']
    cur_time = datetime.datetime.now(datetime.timezone.utc)
    lookback_seconds = int(os.getenv('LOOKBACK_SECONDS', 7200))
    return (cur_time - ent_time).total_seconds() < lookback_seconds

def call_target(content, messageId=None):
    target_url = os.getenv('TARGET_URL')
    verb = "POST"
    if messageId is not None:
        target_url = target_url + f"/messages/{messageId}"
        verb = "PATCH"
    response = requests.request(verb, url=target_url, params={"wait": "true"}, json=content)
    return extract_message_id(response)

def extract_message_id(response):
    return response.json()['id']