import bitmex
import time
import pandas as pd
from keys import ID, SECRET, SLACK_TOKEN
from slackclient import SlackClient
from strategy import Strategy

sc = SlackClient(SLACK_TOKEN)
client = bitmex.bitmex(test=False, api_key=ID, api_secret=SECRET)

strategy = Strategy(client)


def get_volume_data(client):

    dfxbt = client.Trade.Trade_getBucketed(
        binSize='5m', reverse=True, symbol='XBTUSD', count=10, partial=True).result()[0]

    if len(dfxbt) != 0:
        dfxbt = get_ohlcv(dfxbt)
        return dfxbt
    else:
        msg = 'Exception'
        slack_msg(msg)


def get_ohlcv(df):
    ohlcv = pd.DataFrame(df)
    ohlcv.set_index(['timestamp'], inplace=True)
    ohlcv.sort_values(by=['timestamp'], ascending=True, inplace=True)
    return ohlcv


def xbt_cond(data):
    volume = data['volume'][-2]
    data['volume'][-2]
    close = data['close'][-2]
    open = data['open'][-2]

    print(volume)
    print(close)
    print(open)
    result = strategy.place_order(volume, close, open)
    if result == 1:
        msg = 'XBTUSD: 5 min: Volume is ' + str(data['volume'][-2]) + ': '
        msg = msg + 'Buy Order Place at price '+str(data['close'][-2]-1)
        slack_msg(msg)
        time.sleep(5)
        return 1
    elif result == -1:
        msg = 'XBTUSD: 5 min: Volume is ' + str(data['volume'][-2]) + ':'
        msg = msg + 'Sell Order Place at price '+str(data['close'][-2]+1)
        slack_msg(msg)
        time.sleep(5)
        return 1
    else:
        return 0


def check_order_filled():
    while True:
        # set_time = round(Time.time()) + 300
        order_status = client.Order.Order_getOrders(
            symbol='XBTUSD', count=2, reverse=True).result()

        if order_status[0][0]['ordStatus'] == 'Filled':
            msg = 'XBTUSD: Order Filled at Price '+str(order_status[0][0]['price'])
            slack_msg(msg)

            while True:
                order_status = client.Order.Order_getOrders(
                    symbol='XBTUSD', count=2, reverse=True).result()

                if order_status[0][0]['ordStatus'] == 'Filled':
                    msg = 'Order Filled With Profit and excute price: ' + \
                        str(order_status[0][0]['price'])
                    slack_msg(msg)
                    return

                if order_status[0][1]['ordStatus'] == 'Filled':
                    msg = 'Order Filled With Loss and excute price: ' + \
                        str(order_status[0][0]['price'])
                    slack_msg(msg)
                    return

                time.sleep(10)

        time.sleep(10)


def slack_msg(msg):
    try:
        sc.api_call(
            "chat.postMessage",
            channel="bitmex5min",
            text=msg+":smile:",
            username='My Robot',
            icon_emoji=':robot_face:')
        # return True
    except:
        print('Exception in Slack API')
        # return False


if __name__ == '__main__':
    while True:
        one_min = round(time.time()) % 300 == 0

        if one_min:
            time.sleep(1)
            dfxbt = get_volume_data(client)
            result = xbt_cond(dfxbt)
            if result == 1:
                result = check_order_filled()
            else:
                time.sleep(290)
