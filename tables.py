from datetime import datetime, timezone
import logging
import os
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
        pass

    def get_connection(self):
        return mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', ''),
            database=os.getenv('MYSQL_DATABASE', 'spotbot')
        )

    def query_for_entity(self, callsign):
        conn = self.get_connection()
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute('''
                           SELECT callsign,
                                  message_id,
                                  utctimestamp
                                  FROM spots
                                  WHERE callsign = %s
                                  ORDER BY utctimestamp DESC
                                  LIMIT 1''', (callsign,))
            result = cursor.fetchone()
        if result:
            logging.info(f"Entity already exists for {callsign}")
            return result
        return None

    def upsert_entity(self, callsign, messageId):
        utc_now = datetime.now(timezone.utc)
        conn = self.get_connection()
        with conn.cursor() as cursor: 
            cursor.execute('''
                INSERT INTO spots (callsign, message_id, utctimestamp)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE message_id = VALUES(message_id), utctimestamp = VALUES(utctimestamp)
            ''', (callsign, messageId, utc_now))
            conn.commit()