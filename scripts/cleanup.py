
import os
import logging
import mysql.connector
from datetime import datetime, timedelta, timezone

def main():
    logging.basicConfig(level=logging.INFO)
    conn = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', ''),
        database=os.getenv('MYSQL_DATABASE', '')
    )
    cursor = conn.cursor()
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
    cursor.execute('DELETE FROM spots WHERE utctimestamp < %s', (cutoff,))
    conn.commit()
    logging.info(f"Deleted {cursor.rowcount} entries older than 24 hours.")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
