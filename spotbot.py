import logging
import os
import datetime
from pytz import timezone
import requests
import tables


def run(req):
    logging.info('Python HTTP trigger function processed a request.')
    dd = datetime.datetime.now(timezone('US/Pacific'))

    req_body = req.get_json()
    logging.info(f"Received JSON: {req_body}")

    callsign = req_body.get('callsign')

    content = create_content(req_body, dd)

    table = tables.get_table()
    entity = tables.query_for_entity(table, callsign)
    messageId = None
    existingMessage = None

    if is_entity_recent(entity):
        messageId = entity['MessageId']
        existingMessage = get_previous_message(messageId)
        content = existingMessage + "\n" + content

    # flags = 4 means it will suppress embeds: https://discord.com/developers/docs/resources/message#message-object-message-flags
    content_payload = {"content":content, "flags": 4}

    messageId = post_message(content_payload, messageId)
    tables.upsert_entity(table, callsign, messageId)

def create_content(req_body, dd):
    callsign = req_body.get('callsign', 'Unknown')
    source = req_body.get('source', 'Unknown')
    frequency = req_body.get('frequency', 'Unknown')
    mode = req_body.get('mode', 'Unknown')
    summitRef = req_body.get('summitRef', '')
    wwffRef = req_body.get('wwffRef', '')

    spot_deeplink = create_spot_deeplink(source, callsign, wwffRef)
    formatted_time = dd.strftime("%H:%M")

    content = f"{callsign} | {spot_deeplink} | freq: {frequency} | mode: {mode} | loc: {summitRef}{wwffRef} | {formatted_time}"
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

def post_message(content, messageId=None):
    target_url = os.getenv('TARGET_URL')
    verb = "POST"
    if messageId is not None:
        target_url = target_url + f"/messages/{messageId}"
        verb = "PATCH"
    response = requests.request(verb, url=target_url, params={"wait": "true"}, json=content)
    return extract_message_id(response)

def get_previous_message(messageId):
    target_url = os.getenv('TARGET_URL')
    verb = "GET"
    target_url = target_url + f"/messages/{messageId}"
    response = requests.request(verb, url=target_url)
    return response.json()['content']

def extract_message_id(response):
    return response.json()['id']