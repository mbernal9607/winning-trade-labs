from indicators import Indicators
COUNT = 4*7  # Obtener datos de las últimas 4 semanas (4 * 7 días)
def main():
    # Order variables
    conditions = Indicators('EURUSD')
    conditions.ATR(COUNT)
    print(conditions.atr)


if __name__ == "__main__":
    main()