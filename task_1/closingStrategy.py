from utils import getTimeGMTFormat
from datetime import datetime

closeTimeByAsset = {
    'EURUSD': "11:40:00",
    "USDJPY": "09:15:00"
}

class ClosingStrategy():

    currentTime = None
    close = False

    def __init__(self, symbol) -> None:
        self.currentTime = getTimeGMTFormat()
        self.close = self.timeValidation(symbol)

    def timeValidation(self, symbol):
        current = datetime.strptime(self.currentTime, "%H:%M:%S").time()
        closeTime = datetime.strptime(closeTimeByAsset[symbol], "%H:%M:%S").time()

        if current > closeTime or current == closeTime: return True
        
        return False