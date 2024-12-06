import logging
import os
import sqlite3
from azure.data.tables import TableServiceClient
from azure.data.tables import UpdateMode

class BaseAlertTable:
    def query_for_entity(self, callsign):
        raise NotImplementedError

    def upsert_entity(self, callsign, messageId):
        raise NotImplementedError

class HamAlertAzureTable(BaseAlertTable):
    def __init__(self):
        connection_string = os.getenv('AzureWebJobsStorage')
        table_name = os.getenv('TABLE_NAME')
        table_service_client = TableServiceClient.from_connection_string(conn_str=connection_string)
        self.table_client = table_service_client.get_table_client(table_name=table_name)

    def query_for_entity(self, callsign):
        safe_callsign = callsign.replace("'", "''")
        entities = [ent for ent in self.table_client.query_entities(f"PartitionKey eq '{safe_callsign}' and RowKey eq '{safe_callsign}'")]
        if len(entities) > 0:
            logging.info(f"Entity already exists for {safe_callsign}")
        return entities[0] if len(entities) > 0 else None

    def upsert_entity(self, callsign, messageId):
        entity = {
            u'PartitionKey': callsign,
            u'RowKey': callsign,
            u'MessageId': messageId
        }
        self.table_client.upsert_entity(mode=UpdateMode.REPLACE, entity=entity)

class HamAlertSqliteTable(BaseAlertTable):
    def __init__(self):
        db_path = os.getenv('SQLITE_DB_PATH', 'ham_alerts.db')
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ham_alerts (
                callsign TEXT PRIMARY KEY,
                message_id TEXT
            )
        ''')
        self.conn.commit()

    def query_for_entity(self, callsign):
        cursor = self.conn.cursor()
        cursor.execute('SELECT callsign, message_id FROM ham_alerts WHERE callsign = ?', (callsign,))
        result = cursor.fetchone()
        if result:
            logging.info(f"Entity already exists for {callsign}")
            return {'PartitionKey': result[0], 'RowKey': result[0], 'MessageId': result[1]}
        return None

    def upsert_entity(self, callsign, messageId):
        cursor = self.conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO ham_alerts (callsign, message_id) VALUES (?, ?)',
                      (callsign, messageId))
        self.conn.commit()

def create_table_client():
    storage_type = os.getenv('STORAGE_TYPE', 'sqlite').lower()
    if storage_type == 'azure':
        return HamAlertAzureTable()
    return HamAlertSqliteTable()