import logging
import os
import datetime
from hamalertmessage import HamAlertMessage
from tables import HamAlertTable
from discord_http import DiscordHttp

class SpotBot:
    def __init__(self, http_req):
        self.http_req = http_req
        self.ham = HamAlertMessage(http_req.get_json())
        self.table = HamAlertTable()
        self.discord_http = DiscordHttp()

    def process(self):
        logging.info('Processing HamAlert message')
        previous_message, message_id = self.get_last_message()
        previous_message = self.strikethrough_mesage(previous_message)
        content = self.combine_messages(previous_message, self.ham)
        self.discord_http.post_message(content, message_id)
        self.table.upsert_entity(self.ham.callsign, message_id)

    def strikethrough_mesage(self, message):
        return f"~~{message}~~"

    def combine_messages(self, m1, m2):
        return f"{m1}\n{m2}"

    def get_last_message(self):
        last_message_entity = self.table.query_for_entity(self.callsign)
        if self.is_entity_recent(last_message_entity):
            messageId = last_message_entity['MessageId']
            existing_message = self.discord_http.get_message_from_id(messageId)
            return existing_message.replace("~", ""), messageId
        return "", None

    def is_entity_recent(self, entity):
        if entity is None:
            return False
        ent_time = entity.metadata['timestamp']
        cur_time = datetime.datetime.now(datetime.timezone.utc)
        lookback_seconds = int(os.getenv('LOOKBACK_SECONDS', 7200))
        return (cur_time - ent_time).total_seconds() < lookback_seconds