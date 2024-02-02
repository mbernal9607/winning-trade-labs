import os
import MetaTrader5 as mt5
from dotenv import load_dotenv
load_dotenv()


class Order():
    broker = mt5
    # Credentials
    user = int(os.getenv('BROKER_USER'))
    password = os.getenv('BROKER_PASSWORD')
    server = os.getenv('BROKER__SERVER')
    path = r'C:\Program Files\MetaTrader 5\terminal64.exe'

    def __init__(self) -> None:
        if not self.broker.initialize(login=self.user, server=self.server, password=self.password, path=self.path):
            print("[ERROR] - Error to establishing connection - ", self.broker.last_error())
            quit()
        else:
            print('-----------------------------------------------------------------------------------------------------------------------------------------------------------------')
            print('Connection success...')
            account_info = self.broker.account_info() 
            print('Balance: {}'.format(account_info.balance))
            print('Account ID: {}'.format(account_info.login))
            print('Name: {}'.format(account_info.name))
            print('-----------------------------------------------------------------------------------------------------------------------------------------------------------------')
            print('OPEN POSITIONS: {}'.format(len(self.getOpenPositionsInfo())))
            print('-----------------------------------------------------------------------------------------------------------------------------------------------------------------')


    def enviar_operaciones(self, simbolo,tipo_operacion, precio_tp,precio_sl,volumen_op):
        try:
            orderRequest = {
                "action": self.broker.TRADE_ACTION_DEAL,
                "symbol": simbolo,
                #"price": self.broker.symbol_info_tick(simbolo).ask,
                "volume" : volumen_op,
                "type" : tipo_operacion,
                "magic": 202304,
                "comment": 'Reg',
                "type_time": self.broker.ORDER_TIME_GTC,
                "type_filling": self.broker.ORDER_FILLING_IOC
            }
            print('[INFO] sending order - {}'.format(orderRequest))
            response = self.broker.order_send(orderRequest)
            print('[INFO] order sent - {}'.format(response))
            print("[INFO] - order_id: {}".format(response.order))
            return response
        except Exception as err:
            print('[ERROR][OrderClass] - enviar_operaciones function - {}'.format(err))


    def getOpenPositionsInfo(self):
        response = []
        for position in self.broker.positions_get(): 
            response.append({'ticket': position.ticket, 'symbol':position.symbol})
        return response
    
    def closePosition(self, symbol,  ticket_number):
        response = self.broker.Close(symbol, ticket=ticket_number)
        return response