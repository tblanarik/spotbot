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
                return f"[{self.source}](https://pota.app/#/park/{self.wwffRef})"
            case "dxwatch":
                return f"[{self.source}](https://dxwatch.com/dxsd1/dxsd1.php?f=0&t=dx&c={self.callsign})"
            case "pskreporter":
                return f"[{self.source}](https://pskreporter.info/pskmap?callsign={self.callsign}&search=Find)"
            case "rbn":
                return f"[{self.source}](https://www.reversebeacon.net/main.php?rows=10&max_age=10,hours&spotted_call={self.callsign}&hide=distance_km)"
            case _:
                return f"[{self.source}](https://dxwatch.com/dxsd1/dxsd1.php?f=0&t=dx&c={self.callsign})"

    def __str__(self):
        return f'{self.received_time_pt.strftime("%H:%M")} | [{self.callsign}](https://www.qrz.com/db/{self.callsign}) | {self.spot_deeplink()} | freq: {self.frequency} | mode: {self.mode} | loc: {self.summitRef}{self.wwffRef}'