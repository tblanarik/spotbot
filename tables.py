import logging
import os
from azure.data.tables import TableServiceClient
from azure.data.tables import UpdateMode

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

def upsert_entity(table_client, callsign, messageId):
    entity = {
        u'PartitionKey': callsign,
        u'RowKey': callsign,
        u'MessageId': messageId
    }
    table_client.upsert_entity(mode=UpdateMode.REPLACE, entity=entity)