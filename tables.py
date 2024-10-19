import logging
import os
from azure.data.tables import TableServiceClient
from azure.data.tables import UpdateMode

class HamAlertTable:
    def __init__(self):
        connection_string = os.getenv('AzureWebJobsStorage')
        table_name = os.getenv('TABLE_NAME')
        table_service_client = TableServiceClient.from_connection_string(conn_str=connection_string)
        self.table_client = table_service_client.get_table_client(table_name=table_name)

    def initialize_table(self):
        connection_string = os.getenv('AzureWebJobsStorage')
        table_name = os.getenv('TABLE_NAME')
        table_service_client = TableServiceClient.from_connection_string(conn_str=connection_string)
        self.table_client = table_service_client.get_table_client(table_name=table_name)

    def query_for_entity(self, callsign):
        entities = [ent for ent in self.table_client.query_entities(f"PartitionKey eq '{callsign}' and RowKey eq '{callsign}'")]
        if len(entities) > 0:
            logging.info(f"Entity already exists for {callsign}")
        return entities[0] if len(entities) > 0 else None

    def upsert_entity(self, callsign, messageId):
        entity = {
            u'PartitionKey': callsign,
            u'RowKey': callsign,
            u'MessageId': messageId
        }
        self.table_client.upsert_entity(mode=UpdateMode.REPLACE, entity=entity)