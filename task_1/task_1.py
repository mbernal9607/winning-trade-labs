import os
from dotenv import load_dotenv
from order import Order
from closingStrategy import ClosingStrategy

load_dotenv()

def main():
    # Order variables
    symbol = os.getenv('CURRENT_SYMBOL')
    closePositions = os.getenv("CLOSE_POSITIONS", False) == "True"
    openPosition = os.getenv("OPEN_POSITION", False) == "True"
    order = Order()

    if closePositions:
        openPositions = order.getOpenPositionsInfo()
        for position in openPositions:
            closeStrategy = ClosingStrategy(position['symbol'])
            continue
            closed = order.closePosition(position['symbol'], position["ticket"])
            message = "Ups !, Can't close the position {}".format(position["ticket"]) if not closed else f'Great !, The position with number {position["ticket"]} has been closed.'
            print(message)

    if openPosition:
        order.enviar_operaciones(symbol,order.broker.ORDER_TYPE_BUY, 0,0,0.5)


if __name__ == "__main__":
    main()