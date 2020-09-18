import os
from pyrh import Robinhood
import sched
import time

USERNAME = os.environ('USERNAME')
PASSWORD = os.environ('PASSWORD')
# Log in to Robinhood app (will prompt for two-factor)
rh = Robinhood()
rh.login(username=USERNAME, password=PASSWORD)
#Setup our variables
traded = False
s = sched.scheduler(time.time, time.sleep)
def run(sc):
    global traded

    # Get historical close price data for the past year
    close_prices = []
    print("Getting historical quotes")
    historical_quotes = rh.get_historical_quotes("F", "day", "year")
    for key in historical_quotes["results"][0]["historicals"]:
        close_prices.append(float(key['close_price']))
    close_prices.reverse()

    # Calculate Simple Moving Average for 50 and 200 days
    sma50 = 0
    sma200 = 0
    for i in range(200):
        print(i)
        if i < 50:
            sma50 += close_prices[i]
        sma200 += close_prices[i]
    sma50 = sma50/50
    sma200 = sma200/200

    instrument = rh.instruments("F")[0]
    if not traded and sma50 > sma200:
        print("Buying sma50 is crossing above sma200")
        #rh.place_buy_order(instrument, 1)
        traded = True
    if traded and sma50 < sma200:
        print("Selling sma50 is crossing below sma200")
        #rh.place_sell_order(instrument, 1)
        traded = False

    s.enter(86400, 1, run, (sc,))

s.enter(1, 1, run, (s,))
s.run()