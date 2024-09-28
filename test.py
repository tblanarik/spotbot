import unittest
import spotbot

class TestSpotBot(unittest.TestCase):

    def test_function_app_basic(self):
        req_body = {"callsign":"KI7HSG", "source": "pota", "frequency": "14.074", "mode": "FT8", "wwffRef":"US-0052"}
        content = spotbot.create_content(req_body)
        expected = {'content': 'KI7HSG | [pota](https://api.pota.app/spot/comments/KI7HSG/US-0052) | freq: 14.074 | mode: FT8 | loc: US-0052', 'flags': 4}
        self.assertDictEqual(content, expected)

    def test_function_app(self):
        req_body = {"callsign":"KI7HSG", "source": "sotawatch", "frequency": "14.074", "mode": "FT8", "summitRef": "ABCD"}
        content = spotbot.create_content(req_body)
        expected = {'content': 'KI7HSG | [sotawatch](https://sotl.as/activators/KI7HSG) | freq: 14.074 | mode: FT8 | loc: ABCD', 'flags': 4}
        self.assertDictEqual(content, expected)

if __name__ == '__main__':
    unittest.main()
