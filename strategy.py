import time


class Strategy():
    def __init__(self, client):
        self.client = client
        self.amount = 100
        self.order_ID = []

    def place_order(self, volume, close, open):
        if volume > 1000000:
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
        while True:
            try:
                response = self.client.Order.Order_new(
                    symbol="XBTUSD", side="Buy", orderQty=self.amount, price=price-1).result()
            except Exception as e:
                time.sleep(1)
                continue
            else:
                break

        self.order_ID = []
        self.order_ID.append(response[0]['orderID'])

        response = self.set_stop_limit_buy(price)
        self.order_ID.append(response[0]['orderID'])

        response = self.set_take_profit_buy(price)
        self.order_ID.append(response[0]['orderID'])

    def execute_trade_sell(self, close):
        price = close
        while True:
            try:
                response = self.client.Order.Order_new(
                    symbol="XBTUSD", side="Sell", orderQty=self.amount, price=price+1).result()
            except Exception as e:
                time.sleep(1)
                continue
            else:
                break

        self.order_ID = []
        self.order_ID.append(response[0]['orderID'])

        response = self.set_stop_limit_sell(price)
        self.order_ID.append(response[0]['orderID'])

        response = self.set_take_profit_sell(price)
        self.order_ID.append(response[0]['orderID'])

    def set_stop_limit_buy(self, price):
        while True:
            try:
                stop_order_response = self.client.Order.Order_new(
                    symbol="XBTUSD", side="Sell", orderQty=self.amount, stopPx=price-20, price=price-20, execInst="LastPrice,ReduceOnly").result()
            except Exception as e:
                time.sleep(1)
                continue
            else:
                break
        return stop_order_response

    def set_stop_limit_sell(self, price):
        while True:
            try:
                stop_order_response = self.client.Order.Order_new(
                    symbol="XBTUSD", side="Buy", orderQty=self.amount, stopPx=price+20, price=price+20, execInst="LastPrice,ReduceOnly").result()
            except Exception as e:
                time.sleep(1)
                continue
            else:
                break
        return stop_order_response

    def set_take_profit_buy(self, price):
        while True:
            try:
                take_profit_order_response = self.client.Order.Order_new(
                    symbol="XBTUSD", side="Sell", orderQty=self.amount, stopPx=price+10, price=price+20, ordType='LimitIfTouched', execInst="LastPrice,ReduceOnly").result()
            except Exception as e:
                time.sleep(1)
                continue
            else:
                break
        return take_profit_order_response

    def set_take_profit_sell(self, price):
        while True:
            try:
                take_profit_order_response = self.client.Order.Order_new(
                    symbol="XBTUSD", side="Buy", orderQty=self.amount, stopPx=price-10, price=price-20, ordType='LimitIfTouched', execInst="LastPrice,ReduceOnly").result()
            except Exception as e:
                time.sleep(1)
                continue
            else:
                break
        return take_profit_order_response

    def get_order_ID(self):
        return self.order_ID
