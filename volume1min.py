import bitmex
import time
import pandas as pd
from keys import ID, SECRET, SLACK_TOKEN
from slackclient import SlackClient

sc = SlackClient(SLACK_TOKEN)
client = bitmex.bitmex(test=False, api_key=ID, api_secret=SECRET)
dfpair = []


def get_volume_data(client):
    dfpair.clear()

    dfxbt = client.Trade.Trade_getBucketed(
        binSize='1m', reverse=True, symbol='XBTUSD', count=10, partial=True).result()[0]

    dfeth = client.Trade.Trade_getBucketed(
        binSize='1m', reverse=True, symbol='ETHUSD', count=10, partial=True).result()[0]

    dftrx = client.Trade.Trade_getBucketed(
        binSize='1m', reverse=True, symbol='TRX', count=10, partial=True).result()[0]

    dfada = client.Trade.Trade_getBucketed(
        binSize='1m', reverse=True, symbol='ADA', count=10, partial=True).result()[0]

    dfbch = client.Trade.Trade_getBucketed(
        binSize='1m', reverse=True, symbol='BCH', count=10, partial=True).result()[0]

    dfeos = client.Trade.Trade_getBucketed(
        binSize='1m', reverse=True, symbol='EOS', count=10, partial=True).result()[0]

    dfltc = client.Trade.Trade_getBucketed(
        binSize='1m', reverse=True, symbol='LTC', count=10, partial=True).result()[0]

    dfxrp = client.Trade.Trade_getBucketed(
        binSize='1m', reverse=True, symbol='XRP', count=10, partial=True).result()[0]

    if len(dfxbt) != 0:
        dfxbt = get_ohlcv(dfxbt)
        dfpair.append(dfxbt)

    else:
        msg = 'Exception'
        slack_msg(msg)

    if len(dfeth) != 0:
        dfeth = get_ohlcv(dfeth)
        dfpair.append(dfeth)

    else:
        msg = 'Exception'
        slack_msg(msg)

    if len(dftrx) != 0:
        dftrx = get_ohlcv(dftrx)
        dfpair.append(dftrx)
    else:
        msg = 'Exception'
        slack_msg(msg)

    if len(dfada) != 0:
        dfada = get_ohlcv(dfada)
        dfpair.append(dfada)
    else:
        msg = 'Exception'
        slack_msg(msg)

    if len(dfbch) != 0:
        dfbch = get_ohlcv(dfbch)
        dfpair.append(dfbch)
    else:
        msg = 'Exception'
        slack_msg(msg)

    if len(dfltc) != 0:
        dfltc = get_ohlcv(dfltc)
        dfpair.append(dfltc)
    else:
        msg = 'Exception'
        slack_msg(msg)

    if len(dfeos) != 0:
        dfeos = get_ohlcv(dfeos)
        dfpair.append(dfeos)
    else:
        msg = 'Exception'
        slack_msg(msg)

    if len(dfxrp) != 0:
        dfxrp = get_ohlcv(dfxrp)
        dfpair.append(dfxrp)
    else:
        msg = 'Exception'
        slack_msg(msg)

    return dfpair


def get_ohlcv(df):
    ohlcv = pd.DataFrame(df)
    ohlcv.set_index(['timestamp'], inplace=True)
    ohlcv.sort_values(by=['timestamp'], ascending=True, inplace=True)
    return ohlcv


def xbt_cond(data):
    if data['volume'][-2] > 20*data['volume'][-3]:
        msg = 'XBTUSD: 1min: Volume 20 times'
        slack_msg(msg)


def eth_cond(data):
    if data['volume'][-2] > 40*data['volume'][-3]:
        msg = 'ETHUSD: 1min: Volume 20 times'
        slack_msg(msg)


# def trx_cond(data):
    # if data['volume'][-2] > 20*data['volume'][-3]:
    #     msg = 'TRX: 1min: Volume 20 times'
    #     slack_msg(msg)


# def eos_cond(data):
    # if data['volume'][-2] > 20*data['volume'][-3]:
    #     msg = 'EOS: 1min: Volume 20 times'
    #     slack_msg(msg)


# def ltc_cond(data):
    # if data['volume'][-2] > 20*data['volume'][-3]:
    #     msg = 'LTC: 1min: Volume 20 times'
    #     slack_msg(msg)


# def bch_cond(data):
    # if data['volume'][-2] > 20*data['volume'][-3]:
    #     msg = 'BCH: 1min: Volume 20 times'
    #     slack_msg(msg)


# def xrp_cond(data):
    # if data['volume'][-2] > 20*data['volume'][-3]:
    #     msg = 'XRP: 1min: Volume 20 times'
    #     slack_msg(msg)


# def ada_cond(data):
    # if data['volume'][-2] > 20*data['volume'][-3]:
    #     msg = 'ADA: 1min: Volume 20 times'
    #     slack_msg(msg)


def slack_msg(msg):
    try:
        sc.api_call(
            "chat.postMessage",
            channel="bitmex1min",
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
            dfpair = get_volume_data(client)
            xbt_cond(dfpair[0])
            eth_cond(dfpair[1])
            # trx_cond(dfpair[2])
            # ada_cond(dfpair[3])
            # bch_cond(dfpair[4])
            # ltc_cond(dfpair[5])
            # eos_cond(dfpair[6])
            # xrp_cond(dfpair[7])

            time.sleep(58)
