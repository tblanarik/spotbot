import datetime
from pytz import timezone

class HamAlertMessage:
    def __init__(self, req_body):
        self.callsign = req_body.get('callsign', 'Unknown')
        self.source = req_body.get('source', 'Unknown')
        self.frequency = req_body.get('frequency', 'Unknown')
        self.mode = req_body.get('mode', 'Unknown')
        self.summitRef = req_body.get('summitRef', '')
        self.wwffRef = req_body.get('wwffRef', '')
        self.received_time_pt = datetime.datetime.now(timezone('US/Pacific'))

    def spot_deeplink(self):
        match self.source:
            case "sotawatch":
                return f"[{self.source}](https://sotl.as/activators/{self.callsign})"
            case "pota":
                return f"[{self.source}](https://api.pota.app/spot/comments/{self.callsign}/{self.wwffRef})"
            case _:
                return ""

    def __str__(self):
        return f"{self.received_time_pt.strftime("%H:%M")} | {self.callsign} | {self.spot_deeplink} | freq: {self.frequency} | mode: {self.mode} | loc: {self.summitRef}{self.wwffRef}"