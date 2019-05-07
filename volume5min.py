import bitmex
import time
import pandas as pd
from keys import ID, SECRET, SLACK_TOKEN
from slackclient import SlackClient
from strategy import Strategy
import json


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
    set_time = round(time.time()) + 300
    order_ID = strategy.get_order_ID()
    print(order_ID)
    while True:
        check_filled = client.Order.Order_getOrders(
            symbol='XBTUSD', count=2, reverse=True, filter=json.dumps({"orderID": order_ID[0]})).result()
        print(check_filled)
        print('Order Status {}'.format(check_filled[0][0]['ordStatus']))

        if time.time() <= set_time:
            if check_filled[0][0]['ordStatus'] == 'Filled':
                msg = 'XBTUSD: Order Filled at Price '+str(order_status[0][0]['price'])
                slack_msg(msg)
                time.sleep(5)
                while True:
                    order_status_stop = client.Order.Order_getOrders(
                        symbol='XBTUSD', count=2, reverse=True, filter=json.dumps({"orderID": order_ID[1]})).result()

                    if order_status_stop[0][0]['ordStatus'] == 'Filled':
                        msg = 'Order Filled With Profit and excute price: ' + \
                            str(order_status[0][0]['price'])
                        slack_msg(msg)
                        client.Order.Order_cancelAll().result()
                        return

                    order_status_stop = client.Order.Order_getOrders(
                        symbol='XBTUSD', count=2, reverse=True, filter=json.dumps({"orderID": order_ID[2]})).result()

                    if order_status[0][0]['ordStatus'] == 'Filled':
                        msg = 'Order Filled With Loss and excute price: ' + \
                            str(order_status[0][0]['price'])
                        slack_msg(msg)
                        client.Order.Order_cancelAll().result()
                        return

                    time.sleep(10)
            time.sleep(10)
        else:
            client.Order.Order_cancelAll().result()
            msg = 'XBTUSD: Cancel All Orders'
            slack_msg(msg)
            return


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
        try:
            one_min = round(time.time()) % 300 == 0
            if one_min:
                time.sleep(1)
                dfxbt = get_volume_data(client)
                result = xbt_cond(dfxbt)
                if result == 1:
                    result = check_order_filled()
                else:
                    time.sleep(290)

        except Exception as e:
            msg = 'Exception'+str(e)
            slack_msg(msg)
