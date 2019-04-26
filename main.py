import bitmex
import time
import pandas as pd
from keys import ID, SECRET, SLACK_TOKEN
from slackclient import SlackClient

sc = SlackClient(SLACK_TOKEN)
client = bitmex.bitmex(test=False, api_key=ID, api_secret=SECRET)
dfpair=[]


def get_volume_data(client):
    dfxbt = client.Trade.Trade_getBucketed(
        binSize='1m', reverse=True, symbol='XBTUSD', count=10, partial=True).result()[0]

    dfeth = client.Trade.Trade_getBucketed(
        binSize='1m', reverse=True, symbol='ETHUSD', count=10, partial=True).result()[0]

    dfxtb = get_ohlcv(dfxbt)
    dfeth = get_ohlcv(dfeth)

    dfpair.append(dfxbt)
    dfpair.append(dfeth)

    return dfpair


def get_ohlcv(df):
    ohlcv = pd.DataFrame(df)
    ohlcv.set_index(['timestamp'], inplace=True)
    ohlcv.sort_values(by=['timestamp'], ascending=True, inplace=True)
    return ohlcv

def print_vol_xbt(data):
    print('Volume for current XBTUSD {}'.format(data[-1]))
    print('Volume for previous XBTUSD {}'.format(data[-2]))

def print_vol_eth(data):
    print('Volume for current ETHUSD {}'.format(data[-1]))
    print('Volume for previous ETHUSD {}'.format(data[-2]))




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

        if one_min:
            time.sleep(1)
            dfpair=get_volume_data(client)
            print_vol_xbt(dfpair[0])
            print('-----------------------')
            print_vol_eth(dfpair[1])
            time.sleep(58)
