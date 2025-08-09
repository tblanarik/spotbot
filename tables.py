import logging
import os
import sqlite3
import mysql.connector

class BaseAlertTable:
    def query_for_entity(self, callsign):
        raise NotImplementedError

    def upsert_entity(self, callsign, messageId):
        raise NotImplementedError

def create_table_client():
    return HamAlertMySqlTable()

class HamAlertMySqlTable(BaseAlertTable):
    def __init__(self):
        self.conn = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', ''),
            database=os.getenv('MYSQL_DATABASE', 'spotbot')
        )
        self._create_table()

    def _create_table(self):
        cursor = self.conn.cursor()
        # Add the new column if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS spots (
                callsign VARCHAR(255) PRIMARY KEY,
                message_id TEXT,
                utctimestamp DATETIME
            )
        ''')
        # Try to add the column if the table already exists and doesn't have it
        try:
            cursor.execute('ALTER TABLE spots ADD COLUMN utctimestamp DATETIME')
        except mysql.connector.errors.DatabaseError:
            pass  # Ignore if column already exists
        self.conn.commit()

    def query_for_entity(self, callsign):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute('SELECT callsign, message_id, utctimestamp FROM spots WHERE callsign = %s', (callsign,))
        result = cursor.fetchone()
        if result:
            logging.info(f"Entity already exists for {callsign}")
            return {
                'PartitionKey': result['callsign'],
                'RowKey': result['callsign'],
                'MessageId': result['message_id'],
                'UtcTimestamp': result['utctimestamp']
            }
        return None

    def upsert_entity(self, callsign, messageId):
        from datetime import datetime, timezone
        utc_now = datetime.now(timezone.utc)
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO spots (callsign, message_id, utctimestamp)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE message_id = VALUES(message_id), utctimestamp = VALUES(utctimestamp)
        ''', (callsign, messageId, utc_now))
        self.conn.commit()