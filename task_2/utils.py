import pandas as pd
import MetaTrader5 as mt5
from datetime import datetime, timedelta
import yfinance as yf

export_file = False
def calcularATR(close_prices, timeperiod=0):
    """
    Calcula el Average True Range (ATR) para una serie de precios de cierre.

    Args:
        close_prices (pandas.Series): Serie de precios de cierre.
        timeperiod (int): Número de períodos para el cálculo del ATR (por defecto: 14).

    Returns:
        pandas.Series: Serie con los valores del ATR.
    """

    tr = pd.DataFrame(index=close_prices.index)
    tr['h-l'] = close_prices.diff().abs()
    tr['h-pc'] = (close_prices - close_prices.shift()).abs()
    tr['l-pc'] = (close_prices.shift() - close_prices).abs()

    tr['tr'] = tr[['h-l', 'h-pc', 'l-pc']].max(axis=1)

    atr = tr['tr'].rolling(timeperiod).mean()
    print("tr['tr'].rolling(timeperiod).mean() ...", tr['tr'].rolling(timeperiod).mean())
    return atr


def fechasUltimosNMeses(n):
    # Obtener la fecha actual
    fecha_actual = datetime.now().date()

    fechas = []

    # Iterar sobre los últimos N meses
    for i in range(n):
        # Restar i meses a la fecha actual
        fecha = fecha_actual - timedelta(days=30 * i)
        fechas.append(fecha.strftime('%Y-%m-%d'))

    return fechas


def obtenerPreciosCierre(divisa, count):

    if not mt5.initialize():
        print("[ERROR] [utils.obtenerPreciosCierre] - Error al inicializar MetaTrader 5")
        return None
    rates = mt5.copy_rates_from_pos(divisa, mt5.TIMEFRAME_D1, 0, count)
    mt5.shutdown()

    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
#    df.set_index('time', inplace=True)
    if export_file: df.to_csv(f"rates_{(datetime.now()).strftime('%Y_%m_%d_%H_%M_%S')[:-3]}.csv")
    return df

def fechasUltimasNSemanas(n):
    # Obtener la fecha actual
    fecha_actual = datetime.now().date()

    fechas = []

    # Iterar sobre las últimas N semanas
    for i in range(n):
        # Restar i semanas a la fecha actual
        fecha = fecha_actual - timedelta(weeks=i)
        # Ajustar la fecha al primer día de la semana (lunes)
        fecha_inicio_semana = fecha - timedelta(days=fecha.weekday())
        fechas.append(fecha_inicio_semana.strftime('%Y-%m-%d'))

    return fechas