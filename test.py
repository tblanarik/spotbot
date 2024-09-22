import unittest
import function_app

class TestSpotBot(unittest.TestCase):

    def test_function_app_basic(self):
        req_body = {"fullCallsign": "KI7HSG/P", "callsign":"KI7HSG", "source": "pota", "frequency": "14.074", "mode": "FT8", "wwffRef":"US-0052"}
        content = function_app.create_content(req_body)
        expected = {'content': 'KI7HSG/P | pota | freq: 14.074 | mode: FT8 | loc: US-0052 | [See their latest spot](https://api.pota.app/spot/comments/KI7HSG/US-0052)', 'flags': 4}
        self.assertDictEqual(content, expected)

    def test_function_app(self):
        req_body = {"fullCallsign": "KI7HSG/P", "callsign":"KI7HSG", "source": "sotawatch", "frequency": "14.074", "mode": "FT8", "summitRef": "ABCD"}
        content = function_app.create_content(req_body)
        expected = {'content': 'KI7HSG/P | sotawatch | freq: 14.074 | mode: FT8 | loc: ABCD | [See their latest spot](https://sotl.as/activators/KI7HSG)', 'flags': 4}
        self.assertDictEqual(content, expected)

if __name__ == '__main__':
    unittest.main()
