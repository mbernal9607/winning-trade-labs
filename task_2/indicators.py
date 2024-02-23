NAMESPACE = "INDICATORS"

import datetime
import utils
import pandas as pd
import pandas_ta as ta
import traceback
from logger import Logger

class Indicators():
    divisa=''
    export_file = False
    atr = None

    def __init__(self, divisa) -> None:
        self.divisa = divisa
    
    def ATR(self, semanas):
        logger = Logger()
        try:
            close_price_res = utils.obtenerPreciosCierre(self.divisa, semanas)            
            logger.info(
                f"{NAMESPACE} - ATR",
                f"Data frame from pandas is already"
            )
            if self.export_file: close_price_res.to_csv(f"./files/close_price_res_{(datetime.datetime.now()).strftime('%Y_%m_%d_%H_%M_%S')[:-3]}.csv")
            self.atr = ta.atr(close_price_res['high'], close_price_res['low'], close_price_res['close'], length=14)
            return
        except Exception  as error:
            logger.error(
                f"{NAMESPACE} - ATRValidation",
                f"{traceback.format_exc().splitlines()[-1]}"
            )
            return None
