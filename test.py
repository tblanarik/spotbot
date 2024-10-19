import unittest
import spotbot
from datetime import datetime
from pytz import timezone

class TestSpotBot(unittest.TestCase):

    def test_spotbot(self):
        sb = spotbot.SpotBot(FakeHttpRequest(), table=FakeHamAlertTable(FakeEntity("1234", "KI7HSG")), discord_http=FakeDiscordHttp())
        sb.process()
        self.assertEqual(sb.table.saved_callsign, "KI7HSG")
        self.assertEqual(sb.table.saved_messageId, "9876")
        dt = sb.ham.received_time_pt.strftime("%H:%M")
        self.assertEqual(sb.discord_http.posted_message, f"~~01:05 | KI7HSG | [pota](https://api.pota.app/spot/comments/KI7HSG/US-0052) | freq: 14.074 | mode: FT8 | loc: US-0052~~\n{dt} | KI7HSG | [sotawatch](https://sotl.as/activators/KI7HSG) | freq: 14.074 | mode: FT8 | loc: ABCD")

    def test_spotbot_2(self):
        sb = spotbot.SpotBot(FakeHttpRequest(), table=FakeHamAlertTable(None), discord_http=FakeDiscordHttp())
        sb.process()
        self.assertEqual(sb.table.saved_callsign, "KI7HSG")
        self.assertEqual(sb.table.saved_messageId, "9876")
        dt = sb.ham.received_time_pt.strftime("%H:%M")
        self.assertEqual(sb.discord_http.posted_message, f"{dt} | KI7HSG | [sotawatch](https://sotl.as/activators/KI7HSG) | freq: 14.074 | mode: FT8 | loc: ABCD")


'''
Fake classes for testing
'''

class FakeHttpRequest:
    def get_json(self):
        return {"callsign":"KI7HSG", "source": "sotawatch", "frequency": "14.074", "mode": "FT8", "summitRef": "ABCD"}

class FakeHamAlertTable:
    def __init__(self, fake_entity):
        self.saved_callsign = None
        self.saved_messageId = None
        self.fake_entity = fake_entity
    def query_for_entity(self, callsign):
        return self.fake_entity
    def upsert_entity(self, callsign, messageId):
        self.saved_callsign = callsign
        self.saved_messageId = messageId

class FakeEntity(dict):
    def __init__(self, messageId, callsign):
        self['MessageId'] = messageId
        self['PartitionKey'] = callsign
        self['RowKey'] = callsign
        self.metadata = {"timestamp": datetime.now(timezone('US/Pacific'))}

class FakeDiscordHttp:
    def __init__(self):
        self.posted_message = None
    def post_message(self, content, messageId=None):
        self.posted_message = content
        return "9876"
    def get_message_from_id(self, messageId):
        return '01:05 | KI7HSG | [pota](https://api.pota.app/spot/comments/KI7HSG/US-0052) | freq: 14.074 | mode: FT8 | loc: US-0052'


if __name__ == '__main__':
    unittest.main()
