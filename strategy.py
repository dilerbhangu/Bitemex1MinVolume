
class Strategy():
    def __init__(self, client):
        self.client = client
        self.amount = 1000

    def place_order(self, volume, close, open):
        if volume > 20000000:
            if close >= open:
                self.execute_trade_buy(close)
                return 1
            else:
                self.execute_trade_sell(close)
                return -1
        else:
            return 0

    def execute_trade_buy(self, close):
        price = close
        response = self.client.Order.Order_new(
            symbol="XBTUSD", side="Buy", orderQty=self.amount, price=price-1).result()

        self.set_stop_limit_buy(price)
        self.set_take_profit_buy(price)

    def execute_trade_sell(self, close):
        price = close
        response = self.client.Order.Order_new(
            symbol="XBTUSD", side="Sell", orderQty=self.amount, price=price+1).result()

        self.set_stop_limit_sell(price)
        self.set_take_profit_sell(price)

    def set_stop_limit_buy(self, price):
        stop_order_response = self.client.Order.Order_new(
            symbol="XBTUSD", side="Sell", orderQty=self.amount, stopPx=price-20, price=price-20, execInst="LastPrice,ReduceOnly").result()

    def set_stop_limit_sell(self, price):
        stop_order_response = self.client.Order.Order_new(
            symbol="XBTUSD", side="Buy", orderQty=self.amount, stopPx=price+20, price=price+20, execInst="LastPrice,ReduceOnly").result()

    def set_take_profit_buy(self, price):
        take_profit_order_response = self.client.Order.Order_new(
            symbol="XBTUSD", side="Sell", orderQty=self.amount, stopPx=price+10, price=price+20, ordType='LimitIfTouched', execInst="LastPrice,ReduceOnly").result()

    def set_take_profit_sell(self, price):
        take_profit_order_response = self.client.Order.Order_new(
            symbol="XBTUSD", side="Buy", orderQty=self.amount, stopPx=price-10, price=price-20, ordType='LimitIfTouched', execInst="LastPrice,ReduceOnly").result()
