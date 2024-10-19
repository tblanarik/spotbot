import unittest
import spotbot
from datetime import datetime
from pytz import timezone

import requests
import requests_mock

class TestSpotBot(unittest.TestCase):

    def test_function_app_basic(self):
        dd = datetime.strptime("2024-10-13T01:05:03", "%Y-%m-%dT%H:%M:%S")
        req_body = {"callsign":"KI7HSG", "source": "pota", "frequency": "14.074", "mode": "FT8", "wwffRef":"US-0052"}
        content = spotbot.create_content(req_body, dd)
        expected = '01:05 | KI7HSG | [pota](https://api.pota.app/spot/comments/KI7HSG/US-0052) | freq: 14.074 | mode: FT8 | loc: US-0052'
        self.assertEqual(content, expected)

    def test_function_app(self):
        dd = datetime.strptime("2024-10-13T01:05:03", "%Y-%m-%dT%H:%M:%S")
        req_body = {"callsign":"KI7HSG", "source": "sotawatch", "frequency": "14.074", "mode": "FT8", "summitRef": "ABCD"}
        content = spotbot.create_content(req_body, dd)
        expected = '01:05 | KI7HSG | [sotawatch](https://sotl.as/activators/KI7HSG) | freq: 14.074 | mode: FT8 | loc: ABCD'
        self.assertEqual(content, expected)

if __name__ == '__main__':
    unittest.main()
