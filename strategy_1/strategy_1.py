import pandas as pd
import MetaTrader5 as mt5
import pandas_ta as ta
from datetime import datetime, timedelta
import numpy as np
from sklearn.linear_model import LinearRegression
from scipy import stats
import pytz
#import time

# Inicializar conexión con MT5
nombre_cuenta = 67093873
clave = 'Clave01*'
servidor = 'RoboForex-ECN'
path = r'C:\Program Files\MetaTrader 5\terminal64.exe'

if not mt5.initialize(login=nombre_cuenta, password=clave, server=servidor, path=path):
    print("Initialize() failed, error code =", mt5.last_error())
    quit()


# Obtener datos históricos
def obtener_datos(simbolo,num_velas):
    rates = mt5.copy_rates_from_pos(simbolo, mt5.TIMEFRAME_M1, 0, num_velas)
    datos = pd.DataFrame(rates)
    datos['time'] = pd.to_datetime(datos['time'], unit='s')
    return datos

# Función calcular_indicadores para incluir ATR_X
def calcular_indicadores(datos):
    datos['ATR'] = ta.atr(datos['high'], datos['low'], datos['close'])
    bbands_result = ta.bbands(datos['close'])
    # Asignar solo las columnas de interés a tu DataFrame 'datos'
    datos['BOLU'] = bbands_result['BBU_5_2.0']  # Banda superior de Bollinger
    datos['BOLD'] = bbands_result['BBL_5_2.0']  # Banda inferior de Bollinger
    datos['BOLM'] = bbands_result['BBM_5_2.0']  # Banda media de Bollinger
    return datos

def detectar_outliers_volatilidad(datos):
    # Calculamos el umbral de volatilidad alta como el 20% superior de los valores de ATR
    datos['ATR_X'] = datos['ATR'].rolling(window=5*30*24).quantile(0.80)
    datos['ATR_outlier'] = datos['ATR'] < datos['ATR_X']
    return datos




print("1. obteniendo los datos") 

data= obtener_datos('EURUSD',99999)

print("2. calculando indicadores")

atr_1 = calcular_indicadores(data)

print('3. detectando outliers vol')

outli_detec = detectar_outliers_volatilidad(atr_1)

print(outli_detec)
outli_detec.to_csv('outlier_detect.csv')



# Definir función para calcular regresión lineal
def calcular_pendiente_y_p_valor(datos):
    datos_ultima_semana = datos.tail(7*24*60)  # Datos de la última semana
    Y = datos_ultima_semana['close'].values.reshape(-1, 1)
    X = np.arange(len(Y)).reshape(-1, 1)
    
    modelo = LinearRegression().fit(X, Y)
    pendiente = modelo.coef_[0][0]
    
    # Calculamos p-value
    predictions = modelo.predict(X)
    nuevoX = np.append(np.ones((len(X), 1)), X, axis=1)
    MSE = np.sum((Y-predictions)**2) / (len(nuevoX) - len(nuevoX[0]))
    var_b = MSE * (np.linalg.inv(np.dot(nuevoX.T, nuevoX)).diagonal())
    sd_b = np.sqrt(var_b)
    ts_b = pendiente / sd_b
    p_value = 2 * (1 - stats.t.cdf(np.abs(ts_b), len(nuevoX) - 2))
    
    return pendiente, p_value


def abrir_operacion(datos, simbolo):
    # Asume que datos ya tiene calculados ATR, ATR_X%, Bandas de Bollinger, y ATR_outlier
    pendiente, p_value = calcular_pendiente_y_p_valor(datos)
    
    # Verificar si el último ATR es considerado un outlier
    es_outlier = datos.iloc[-1]['ATR_outlier']
    
    # Obtener el último precio de cierre y las bandas de Bollinger
    precio_actual = datos['close'].iloc[-1]
    bolu = datos['BOLU'].iloc[-1]
    bold = datos['BOLD'].iloc[-1]
    
    # Condiciones para abrir operaciones
    if es_outlier and pendiente > 0 and p_value < 0.2 and precio_actual < bold:
        enviar_orden(mt5.ORDER_TYPE_BUY, simbolo, precio_actual)
    elif es_outlier and pendiente < 0 and p_value < 0.2 and precio_actual > bolu:
        enviar_orden(mt5.ORDER_TYPE_SELL, simbolo, precio_actual)



# Enviar órdenes a MT5
def enviar_orden(tipo, simbolo, precio):
    order = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": simbolo,
        "volume": 0.1,
        "type": tipo,
        "price": precio,
        "magic": 123456,
        "comment": 'Operación automática',
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC
    }
    mt5.order_send(order)


def cerrar_operaciones(simbolo):
    umbral_pendiente = 0.05
    posiciones = mt5.positions_get(symbol=simbolo)
    if posiciones is None or len(posiciones) == 0:
        print("No hay posiciones abiertas para", simbolo)
        return

    for posicion in posiciones:
        datos = obtener_datos(simbolo, 7*24*60)  # Datos de la última semana
        pendiente, _ = calcular_pendiente_y_p_valor(datos)

        # Comprobar si la pendiente de la regresión es cercana a cero o si el mercado está a punto de cerrar
        if abs(pendiente) < umbral_pendiente or mercado_cerca_de_cerrar(simbolo):
            # Determinar el tipo de orden de cierre basado en el tipo de la posición abierta
            tipo_orden_cierre = mt5.ORDER_TYPE_SELL if posicion.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY
            enviar_orden_cierre(tipo_orden_cierre, simbolo, posicion.volume, posicion.ticket)

# Comprobar si el mercado está cerca de cerrar
def mercado_cerca_de_cerrar(simbolo):
    tiempo_actual = datetime.now(pytz.utc)
    info_simbolo = mt5.symbol_info(simbolo)
    if info_simbolo is None:
        print("Información no disponible para el símbolo:", simbolo)
        return False
    
    hora_cierre = info_simbolo.session_close[0]  # Asume que session_close es una tupla con horas de cierre
    hora_cierre_dt = datetime(tiempo_actual.year, tiempo_actual.month, tiempo_actual.day, hora_cierre // 60, hora_cierre % 60, tzinfo=pytz.utc)
    
    # Comprobar si el mercado está a 15 minutos o menos de cerrar
    return tiempo_actual >= hora_cierre_dt - timedelta(minutes=15)

# Función adaptada para enviar órdenes de cierre
def enviar_orden_cierre(tipo, simbolo, volumen, ticket):
    order = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": simbolo,
        "volume": volumen,
        "type": tipo,
        "position": ticket,  # Especificar el ticket de la posición que queremos cerrar
        "magic": 123456,
        "comment": 'Cierre automático',
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC
    }
    resultado = mt5.order_send(order)
    if resultado.retcode != mt5.TRADE_RETCODE_DONE:
        print("Error al enviar orden de cierre, código de error:", resultado.retcode)
    else:
        print("Orden de cierre enviada correctamente para", simbolo, ", ticket:", ticket)