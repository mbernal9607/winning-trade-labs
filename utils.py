import MetaTrader5 as mt5


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



def _orderPayloadBuilder(self,par:str,volumen: float,tipo_operacion:mt5,nombre_bot:str,sl:float= None,tp:float = None,type_fill= mt5.ORDER_FILLING_FOK) -> None:
        '''
        Función para abrir operaciones en mt5. Esta funciónpuede abrir operaciones sin Stop Loss y sin Take Profit, solo con stop loss, solo con 
        take profit o con ámbos parámetros.

        # Parámetros

        - par: Símbolo a extraer
        - volumen: Lotaje de la operación
        - tipo_operacion: mt5.ORDER_TYPE_BUY o mt5.ORDER_TYPE_BUY
        - nombre_bot: Nombre de la estrategia que abre la operación
        - type_fill: Política de ejecución de las órdenes FILLING_FOK o FILLING_IOC

        '''

        orden = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": par,
            "volume": volumen,
            "type": tipo_operacion,
            "magic": 202204,
            "comment": nombre_bot,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": type_fill
        }

        if (tp != None): order["tp"] = tp

        elif (sl != None) and (tp == None):
            orden = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": par,
                "sl": sl,
                "volume": volumen,
                "type": tipo_operacion,
                "magic": 202204,
                "comment": nombre_bot,
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": type_fill
            }

            result  = mt5.order_send(orden)
            
        
        elif (sl != None) and (tp != None):
            orden = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": par,
            "sl": sl,
            "tp": tp,
            "volume": volumen,
            "type": tipo_operacion,
            "magic": 202204,
            "comment": nombre_bot,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": type_fill

            }

            result  = mt5.order_send(orden)
        
        return result
        result  = mt5.order_send(orden)
        print('Se ejecutó una',tipo_operacion, 'con un volumen de', volumen)