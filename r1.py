


from AlgoAPI import AlgoAPIUtil, AlgoAPI_Backtest
from datetime import datetime, timedelta
import talib
import numpy as np

class AlgoEvent:
    def __init__(self):
        self.lasttradetime = datetime(2000, 1, 1)
        self.arr_close = []
        self.arr_high = []
        self.arr_low = []
        self.short_period = 9
        self.medium_period = 13
        self.long_period = 21
        self.extra_long_period = 55
        self.ATR_period = 14
        self.risk_reward_ratio = 3

    def start(self, mEvt):
        self.instrument_1 = 'BTCUSD'
        mEvt['subscribeList'] = [self.instrument_1]
        self.evt = AlgoAPI_Backtest.AlgoEvtHandler(self, mEvt)
        self.evt.start()

    def on_bulkdatafeed(self, isSync, bd, ab):
        if isSync and bd[self.instrument_1]['timestamp'] > self.lasttradetime:
            self.lasttradetime = bd[self.instrument_1]['timestamp']
            lastprice = bd[self.instrument_1]['lastPrice']
            lasthigh = bd[self.instrument_1]['highPrice']
            lastlow = bd[self.instrument_1]['lowPrice']
            self.arr_close.append(lastprice)
            self.arr_high.append(lasthigh)
            self.arr_low.append(lastlow)

            if len(self.arr_close) > self.extra_long_period:
                np_closes = np.array(self.arr_close)
                np_highs = np.array(self.arr_high)
                np_lows = np.array(self.arr_low)
                
                short_ma = talib.SMA(np_closes, self.short_period)[-1]
                medium_ma = talib.SMA(np_closes, self.medium_period)[-1]
                long_ma = talib.SMA(np_closes, self.long_period)[-1]
                extra_long_ma = talib.SMA(np_closes, self.extra_long_period)[-1]
                
                # Calculate ATR
                ATR = talib.ATR(np_highs, np_lows, np_closes, self.ATR_period)[-1]

                # Check for trading signals
                if short_ma > medium_ma > long_ma > extra_long_ma:
                    self.place_order('open', 1, lastprice, ATR)
                elif short_ma < medium_ma < long_ma < extra_long_ma:
                    self.place_order('open', -1, lastprice, ATR)

    def place_order(self, openclose, buysell, lastprice, ATR):
        order = AlgoAPIUtil.OrderObject(
            instrument=self.instrument_1,
            openclose=openclose,
            buysell=buysell,
            ordertype=0,  # Market order
            volume=0.01
        )
        self.evt.sendOrder(order)
        
        # Calculate stop loss and take profit levels
        if buysell == 1:  # For a buy order
            sl = lastprice - ATR
            tp = lastprice + ATR * self.risk_reward_ratio
        else:  # For a sell order
            sl = lastprice + ATR
            tp = lastprice - ATR * self.risk_reward_ratio

        self.update_order(order.tradeID, sl, tp)

    def update_order(self, tradeID, sl, tp):
        res = self.evt.update_opened_order(tradeID=tradeID, sl=sl, tp=tp)
        # Print to console
        self.evt.consoleLog(f"Order update status: {res['status']}, Message: {res['msg']}")



