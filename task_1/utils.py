import MetaTrader5 as mt5
from datetime import datetime
import pytz




def enviar_operaciones(simbolo,tipo_operacion, precio_tp,precio_sl,volumen_op):
    orden_sl = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": simbolo,
        #"price": mt5.symbol_info_tick(simbolo).ask,
        "volume" : volumen_op,
        "type" : tipo_operacion,
        "magic": 202304,
        "comment": 'Reg',
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC
    }
    print('[INFO] sending order - {}'.format(orden_sl))
    response = mt5.order_send(orden_sl)
    print('[INFO] order sent - {}'.format(response))
    return response

def getTimeGMTFormat():
    tiempoGTM = datetime.now(pytz.timezone('GMT'))
    return tiempoGTM.strftime('%H:%M:%S')