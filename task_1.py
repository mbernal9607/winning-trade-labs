import os
import MetaTrader5 as mt5
from dotenv import load_dotenv
load_dotenv()
from utils import enviar_operaciones

# Credentials
user = int(os.getenv('MT5_USER'))
password = os.getenv('MT5_PASSWORD')
server = os.getenv('MT5_SERVER')
path = r'C:\Program Files\MetaTrader 5\terminal64.exe'

#In the first task, we need to test whether given conditions will close the opened position
# 1. Open position using MT5

if not mt5.initialize(login=user, server=server, password=password, path=path):
    print("[ERROR] - Error to establishing connection - ", mt5.last_error())
    quit()
else:
    print('-----------------------------------------------------------------------------------------------------------------------------------------------------------------')
    print('Connection success...')
    account_info = mt5.account_info() 
    print('Balance: {}'.format(account_info.balance))
    print('Account ID: {}'.format(account_info.login))
    print('Name: {}'.format(account_info.name))
    print('-----------------------------------------------------------------------------------------------------------------------------------------------------------------')
    print('OPEN POSITIONS:')
    for position in mt5.positions_get():
        print('Ticket: {} \n Symbol: {}'.format(position.ticket, position.symbol))
    print('-----------------------------------------------------------------------------------------------------------------------------------------------------------------')
# Order variables
symbol = "EURUSD"
result = enviar_operaciones(symbol,mt5.ORDER_TYPE_BUY, 0,0,0.5)

# send a trading request
if result.retcode != mt5.TRADE_RETCODE_DONE:
    print("Order failed: {} - {}".format(result.retcode, result.comment)) 
else:
    print("[order_info] - {}".format(result.order))
