








from AlgoAPI import AlgoAPIUtil, AlgoAPI_Livetest
from datetime import datetime, timedelta
import talib
import numpy as np

class AlgoEvent:
    def __init__(self):
        self.lasttradetime = datetime(2000, 1, 1)
        self.arr_close = []
        self.arr_close_EMA = []
        self.arr_high = []
        self.arr_low = []
        self.short_period = 9
        self.medium_period = 13
        self.long_period = 21
        self.extra_long_period = 55
        self.ATR_period = 14
        self.risk_reward_ratio = 2
        self.leverage_ratio = 5
        self.position_opened = False  # To track if there is an open position
        self.last_crossover = None  # To track the last crossover status
        self.trade_ID = 1
        self.last_buysell = 1
        self.startTrade_ID = 1
        self.open_trades_long = []
        self.open_trades_short = []
        self.open_trades_longMACD = []
        self.open_trades_shortMACD = []
        self.ATR_multiplier = 2
        self.macd_fast_period = 12
        self.macd_slow_period = 26
        self.macd_signal_period = 9
        self.arr_close_MACD = []
        self.arr_high_MACD = []
        self.arr_low_MACD = []
        self.BBands_period = 20
        self.day_check = 23
        

    def start(self, mEvt):
        self.instrument_1 = 'BTCUSD'
        mEvt['subscribeList'] = [self.instrument_1]
        self.evt = AlgoAPI_Livetest.AlgoEvtHandler(self, mEvt)
        self.evt.consoleLog(self.day_check)
    
        # Specify the contract for which you want to get historical data
        contract = {
            "instrument": self.instrument_1
        }
        
        # Set the number of bars you want to retrieve and the interval
        numOfBar = max(self.extra_long_period, self.ATR_period)  # Fetch enough bars for the longest EMA and ATR
        interval = 'D'  # Daily bars
        
        numOfBar2 = max(self.macd_slow_period, self.macd_signal_period)
        interval2 = 'H'
    
        # Fetch historical data for the instrument
        historical_data = self.evt.getHistoricalBar(contract, numOfBar, interval)
        
        historical_data2 = self.evt.getHistoricalBar(contract, numOfBar2, interval2)
    
        # Process historical data to fill your price arrays
        for timestamp in sorted(historical_data.keys()):
            bar = historical_data[timestamp]
            self.arr_close_EMA.append(bar['c'])
            self.arr_high.append(bar['h'])
            self.arr_low.append(bar['l'])
        #self.evt.consoleLog("array close hist", self.arr_close_EMA)
        #self.evt.consoleLog("array close length", len(self.arr_close_EMA))
            
            
         # Process historical data to fill your price arrays
        for timestamp2 in sorted(historical_data2.keys()):
            bar2 = historical_data2[timestamp2]
            self.arr_close_MACD.append(bar2['c'])
            self.arr_high_MACD.append(bar2['h'])
            self.arr_low_MACD.append(bar2['l'])
        
        #self.evt.consoleLog("array close length mid", len(self.arr_close))
    
    
        # Start the event handler
        self.evt.start()

    def on_bulkdatafeed(self, isSync, bd, ab):
        if isSync:
            self.evt.consoleLog(self.day_check, self.lasttradetime)
            if bd[self.instrument_1]['timestamp'] > self.lasttradetime:
                self.day_check = self.day_check + 1
                self.evt.consoleLog("New day check", self.day_check)
                self.lasttradetime = bd[self.instrument_1]['timestamp']
                lastprice2 = bd[self.instrument_1]['lastPrice']
                lasthigh2 = bd[self.instrument_1]['highPrice']
                lastlow2 = bd[self.instrument_1]['lowPrice']
                self.arr_high_MACD.append(lasthigh2)
                self.arr_low_MACD.append(lastlow2)
                self.arr_close_MACD.append(lastprice2)
                np_closes2 = np.array(self.arr_close_MACD)
                np_highs2 = np.array(self.arr_high_MACD)
                np_lows2 = np.array(self.arr_low_MACD)
                #self.close_all_trades(1)
                
                #self.evt.consoleLog("array close mid2", self.arr_close_EMA)
                #.evt.consoleLog("array close MACD mid2", self.arr_close_MACD)
                #self.evt.consoleLog("array close MACD length mid2", len(self.arr_close_MACD))
                #self.evt.consoleLog("array close length mid2", len(self.arr_close_EMA))
                self.evt.consoleLog("short", self.open_trades_short)
                self.evt.consoleLog("long", self.open_trades_long)
                self.evt.consoleLog("shortMACD", self.open_trades_shortMACD)
                self.evt.consoleLog("longMACD", self.open_trades_longMACD)
    
                
                        
                MACD, MACDSignal, _ = talib.MACD(np_closes2, fastperiod=self.macd_fast_period, slowperiod=self.macd_slow_period, signalperiod=self.macd_signal_period)
                upperband, middleband, lowerband = talib.BBANDS(np_closes2, timeperiod=self.BBands_period, nbdevup=2, nbdevdn=2, matype=0)
    
                if len(MACD) > 0 and len(upperband) > 0:
                    latest_MACD = MACD[-1]
                    latest_MACDSignal = MACDSignal[-1]
                    latest_upperband = upperband[-1]
                    latest_middleband = middleband[-1]
                    latest_lowerband = lowerband[-1]
                    ATR2 = talib.ATR(np_highs2, np_lows2, np_closes2, self.ATR_period)[-1]
                    
                    self.evt.consoleLog("latest_MACD", latest_MACD)
                    self.evt.consoleLog("latest_MACDSignal", latest_MACDSignal)
    
                
                        
                    if latest_MACD > latest_MACDSignal and (lastprice2 >= latest_middleband or lastprice2 <= latest_upperband):
                        self.close_all_tradesMACD(-1)
                        self.place_order('open', 1, 0.05, lastprice2, ATR2, self.trade_ID, -1)
                        self.open_trades_longMACD.append(self.trade_ID)
                        self.trade_ID = self.trade_ID + 1
                    elif latest_MACD < latest_MACDSignal and (lastprice2 <= latest_middleband or lastprice2 >= latest_lowerband):
                        self.close_all_tradesMACD(1)
                        self.place_order('open', -1, 0.05, lastprice2, ATR2, self.trade_ID, -1)
                        self.open_trades_shortMACD.append(self.trade_ID)
                        self.trade_ID = self.trade_ID + 1
                    
        
            # Check if the current timestamp is at least a day ahead of the last trade time
            if self.day_check == 24:
                self.day_check = 0
                # Update the last trade time to the current timestamp
    
                # Extract the last price, high, and low from the bulk data
                lastprice = bd[self.instrument_1]['lastPrice']
                lasthigh = bd[self.instrument_1]['highPrice']
                lastlow = bd[self.instrument_1]['lowPrice']
    
                # Append the new daily data to the arrays
                self.arr_close_EMA.append(lastprice)
                self.arr_high.append(lasthigh)
                self.arr_low.append(lastlow)
    
                # Convert the arrays to numpy arrays for EMA calculations
                np_closes = np.array(self.arr_close_EMA)
                np_highs = np.array(self.arr_high)
                np_lows = np.array(self.arr_low)
                self.evt.consoleLog("array close final", self.arr_close_EMA)
                self.evt.consoleLog("array close length", len(self.arr_close_EMA))
                self.evt.consoleLog("extralongPeriod", self.extra_long_period)
                #self.evt.consoleLog("np_closes", np_closes)
                
                
                    
                if len(self.arr_close_EMA) > self.extra_long_period:
                    
                    
                    short_ma = talib.EMA(np_closes, self.short_period)[-1]
                    medium_ma = talib.EMA(np_closes, self.medium_period)[-1]
                    long_ma = talib.EMA(np_closes, self.long_period)[-1]
                    extra_long_ma = talib.EMA(np_closes, self.extra_long_period)[-1]
                    
                    self.evt.consoleLog("short_ma", short_ma)
                    self.evt.consoleLog("medium_ma", medium_ma)
                    self.evt.consoleLog("long_ma", long_ma)
                    self.evt.consoleLog("extra_long_ma", extra_long_ma)
                    # Calculate ATR
                    #ATR = talib.ATR(np_highs, np_lows, np_closes, self.ATR_period)[-1]
    
                    current_crossover = short_ma > medium_ma > long_ma > extra_long_ma
                    opposite_crossover = short_ma < medium_ma < long_ma < extra_long_ma
                    
                    if current_crossover:
                        self.close_all_trades(-1)
                        self.place_order('open', 1, 0.25, lastprice, 0, self.trade_ID, 1)
                        self.evt.consoleLog("lastprice", lastprice)
                        self.open_trades_long.append(self.trade_ID)
                        self.trade_ID = self.trade_ID + 1
                        self.evt.consoleLog(self.open_trades_short)
                        self.evt.consoleLog(self.open_trades_long)
                    elif opposite_crossover:
                        self.close_all_trades(1)
                        self.place_order('open', -1, 0.25, lastprice, 0, self.trade_ID, 1)
                        self.evt.consoleLog("lastprice", lastprice)
                        self.open_trades_short.append(self.trade_ID)
                        self.trade_ID = self.trade_ID + 1
                        self.evt.consoleLog(self.open_trades_short)
                        self.evt.consoleLog(self.open_trades_long)
                
                
    
                    
    def close_all_trades(self, longshort):
        # Close all trades that are currently open
        if self.open_trades_long and longshort == 1:
            for tradeID in self.open_trades_long:
                self.place_order('close', None, None, None, None, tradeID, None)
            # Clear the list of open trades
            self.open_trades_long.clear()
        
        if self.open_trades_short and longshort == -1:
            for tradeID in self.open_trades_short:
                self.place_order('close', None, None, None, None, tradeID, None)
            # Clear the list of open trades
            self.open_trades_short.clear()
            
    def close_all_tradesMACD(self, longshort):
        # Close all trades that are currently open
        if self.open_trades_longMACD and longshort == 1:
            for tradeID in self.open_trades_longMACD:
                self.place_order('close', None, None, None, None, tradeID, None)
            # Clear the list of open trades
            self.open_trades_longMACD.clear()
        
        if self.open_trades_shortMACD and longshort == -1:
            for tradeID in self.open_trades_shortMACD:
                self.place_order('close', None, None, None, None, tradeID, None)
            # Clear the list of open trades
            self.open_trades_shortMACD.clear()
                

    def place_order(self, openclose, buysell, volume, lastprice, ATR, tradeID, EmaMacD):
        if openclose == 'close':
            # For closing orders, we do not need to specify buysell, volume, lastprice, or ATR
            order = AlgoAPIUtil.OrderObject(
                instrument=self.instrument_1,
                tradeID=tradeID,
                openclose=openclose,
                ordertype=0  # Market order
            )
        elif EmaMacD == -1:
            # For opening orders, we calculate stop_loss_level and take_profit_level
            stop_loss_level = lastprice + (0.05*lastprice) if buysell == -1 else lastprice - (0.05*lastprice)
            take_profit_level = lastprice - (0.05*lastprice) if buysell == -1 else lastprice + (0.05*lastprice)
            order = AlgoAPIUtil.OrderObject(
                instrument=self.instrument_1,
                tradeID=tradeID,
                openclose=openclose,
                buysell=buysell,
                ordertype=1,
                price=lastprice,# Market order
                volume=volume,
                #stopLossLevel=stop_loss_level,  # Set the stop loss level
                #takeProfitLevel=take_profit_level,  # Set the take profit level
            )
            
        elif EmaMacD == 1:
            # For opening orders, we calculate stop_loss_level and take_profit_level
            stop_loss_level = lastprice + (0.10*lastprice) if buysell == -1 else lastprice - (0.10*lastprice)
            take_profit_level = lastprice - (0.20*lastprice) if buysell == -1 else lastprice + (0.20*lastprice)
            order = AlgoAPIUtil.OrderObject(
                instrument=self.instrument_1,
                tradeID=tradeID,
                openclose=openclose,
                buysell=buysell,
                ordertype=1,
                price = lastprice,# Market order
                volume=volume,
                #stopLossLevel=stop_loss_level,  # Set the stop loss level
                #takeProfitLevel=take_profit_level,  # Set the take profit level
            )
        # Send the order
        self.evt.sendOrder(order)
        
    


















































