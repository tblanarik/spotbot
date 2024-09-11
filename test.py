import unittest
import function_app

class TestSpotBot(unittest.TestCase):

    def test_function_app_basic(self):
        req_body = {"fullCallsign": "KI7HSG", "source": "POTA", "frequency": "14.074", "mode": "FT8", "wwffRef":"US-0052"}
        content = function_app.create_content(req_body)
        expected = {'content': 'KI7HSG | POTA | freq: 14.074 | mode: FT8 | loc: US-0052'}
        self.assertDictEqual(content, expected)

    def test_function_app(self):
        req_body = {"fullCallsign": "KI7HSG", "source": "sotawatch", "frequency": "14.074", "mode": "FT8", "summitRef": "ABCD"}
        content = function_app.create_content(req_body)
        expected = {'content': 'KI7HSG | sotawatch | freq: 14.074 | mode: FT8 | loc: ABCD'}
        self.assertDictEqual(content, expected)

if __name__ == '__main__':
    unittest.main()
