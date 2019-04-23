import bitmex
import time
import pandas as pd
from keys import ID, SECRET, SLACK_TOKEN
from slackclient import SlackClient

sc = SlackClient(SLACK_TOKEN)
client = bitmex.bitmex(test=False, api_key=ID, api_secret=SECRET)


def get_volume_data(client, timeframe):
    df = client.Trade.Trade_getBucketed(
        binSize=timeframe, reverse=True, symbol='XBTUSD', count=10, partial=True).result()[0]
    ohlcv_candles = pd.DataFrame(df)
    ohlcv_candles.set_index(['timestamp'], inplace=True)
    ohlcv_candles.sort_values(by=['timestamp'], ascending=True, inplace=True)
    return ohlcv_candles
    # print('voulume previous {}'.format(ohlcv_candles['volume'][-3]))
    # print('volume current {}'.format(ohlcv_candles['volume'][-2]))


def condition_1min(data):
    print('voulume previous {}'.format(data['volume'][-3]))
    print('volume current {}'.format(data['volume'][-2]))
    if data['volume'][-2] > 20*data['volume'][-3]:
        return True
    else:
        return False


def condition_5min(data):
    if data['volume'][-2] > 10*data['volume'][-3]:
        return True
    else:
        return False


def condition_1hour(data):
    if data['volume'][-2] > 4*data['volume'][-3]:
        return True
    else:
        return False


def slack_msg(msg):
    try:
        sc.api_call(
            "chat.postMessage",
            channel="bitmexbot",
            text=msg+":smile:",
            username='My Robot',
            icon_emoji=':robot_face:')
        # return True
    except:
        print('Exception in Slack API')
        # return False


if __name__ == '__main__':
    while True:
        one_min = round(time.time()) % 60 == 0
        five_min = round(time.time()) % 300 == 0
        one_hour = round(time.time()) % 3600 == 0
        if one_min:
            time.sleep(1)
            data = get_volume_data(client, '1m')
            if condition_1min(data):
                msg = 'Pair:XBTUSD, TimeFrame:1 Min, Signal: 20 Times Volume'
                slack_msg(msg)
            if five_min:
                data = get_volume_data(client, '5m')
                if condition_5min(data):
                    msg = 'Pair:XBTUSD, TimeFrame:5 Min, Signal: 10 Times Volume'
                    slack_msg(msg)
                if one_hour:
                    data = get_volume_data(client, '1h')
                    if condition_1hour(data):
                        msg = 'Pair:XBTUSD, TimeFrame:1 hour, Signal: 4 Times Volume'
                        slack_msg(msg)

            time.sleep(58)

    # get_volume_data(client, '5m')
