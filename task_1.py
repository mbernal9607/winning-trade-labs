import os
import MetaTrader5 as mt5
from dotenv import load_dotenv
load_dotenv()

# Credentials
user = int(os.getenv('MT5_USER'))
password = os.getenv('MT5_PASSWORD')
server = os.getenv('MT5_SERVER')


#In the first task, we need to test whether given conditions will close the opened position
# 1. Open position using MT5

if not mt5.initialize(login=user, server=server, password=password):
    print("[ERROR] - Error to establishing connection - ", mt5.last_error())
    quit()
else:
    print('-----------------------------------------------------------------------------------------------------------------------------------------------------------------')
    print('Connection success...')
    print(mt5.account_info())
    print("MetaTrader5 package version: ", mt5.__version__)
    print('-----------------------------------------------------------------------------------------------------------------------------------------------------------------')


# Order variables
symbol = "USDJPY"
lot = 0.1
point = mt5.symbol_info(symbol).point
price = mt5.symbol_info_tick(symbol).ask
deviation = 20

print('Open positions  = {}'.format(mt5.positions_get()))

request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot,
    "type": mt5.ORDER_TYPE_BUY,
    "price": price,
    "deviation": 0,
    "magic": 0,
    "comment": "Python Script Open Buy",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_IOC,
}
print(request)
# send a trading request
result = mt5.order_send(request=request)
if result.retcode != mt5.TRADE_RETCODE_DONE:
    print("Order failed: {} - {}".format(result.retcode, result.comment)) 
else:
    print("[order_send] - {}".format(result.order))
