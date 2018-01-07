
import pandas as pd
import time
import datetime as dt


class TimeFormat():
    TRADES_TIME_FORMAT = "%Y-%m-%dT%H:%M"



def datetimeToTimeStamp(d):
    d= [dt.datetime.strptime(i,TimeFormat.TRADES_TIME_FORMAT) for i in d]

    t = [i.timetuple() for i in d]

    timeStamp = [ int(time.mktime(i)) for i in t]
    return timeStamp




def parse(data):

    if type(data) is not pd.DataFrame:
        raise Exception("Data should be type dataframe")

    return


def parsePrice( data):

    parse(data)

    if ('interval' in data):
        d = dict((data.groupby('interval').mean())['price'])
    else:
        d = dict((data.groupby('time').mean())['price'])

    x = []
    y = []

    for k, v in d.items():
        x.append(k)
        y.append(v)

        # if('interval' not in tradesDF):
        #   x= [dt.datetime.strptime(i, TRADES_TIME_FORMAT) for i in x]
    x = datetimeToTimeStamp(x)

    return x, y



def parseStdDev( data):
    parse(data)
    if ('interval' in data):
        s = dict((data.groupby('interval').std())['price'])
    else:
        s = dict((data.groupby('time').std())['price'])

    sx = []
    sy = []

    for k, v in s.items():
        sx.append(k)
        sy.append(v)

        # if('interval' not in tradesDF):
        #   x= [dt.datetime.strptime(i, TRADES_TIME_FORMAT) for i in x]
    sx = datetimeToTimeStamp(sx)
    return sx, sy

def parseVolume(data):
    parse(data)
    if ('interval' in data):
        d = dict((data.groupby('interval').sum())['volume'])
    else:
        d = dict((data.groupby('time').sum())['volume'])
    print(d)

    x = []
    y = []
    for k, v in d.items():
        x.append(k)
        y.append(v)

        # if('interval' not in tradesDF):
        #   x= [dt.datetime.strptime(i, TRADES_TIME_FORMAT) for i in x]
    x = datetimeToTimeStamp(x)

    return x, y

def parseCash(data):
    parse(data)

    ids = data.groupby('time')['AbsoluteCash'].idxmax()
    print(ids.values)
    netcash = data.loc[ids]['NetCashInMarket'].values
    time = data.loc[ids]['time'].values

    time = datetimeToTimeStamp(time)
    print(dt.datetime.fromtimestamp(time[0]))
    return time, netcash

def parseTradeCount(data):
    if ('interval' in data):
        #count = dict((tradesDF.groupby('interval').sum())['cash'])
        count = dict((data.groupby('interval').size()))
    else:
        #count = dict((tradesDF.groupby('time').sum())['cash'])
        count = dict(data.groupby('time').size())

    x=[]
    y=[]
    for k,v in count.items():
        x.append(k)
        y.append(v)
    x = datetimeToTimeStamp(x)
    return x,y



def txtParserAvgPrice(data):
    volume = data['volume'].sum()
    cash = data['cash'].sum()

    return cash/volume

def txtParserVolumeSum(data):
    volume = data['volume'].sum()
    return volume

def txtParserCashSum(data):
    volume = data['cash'].sum()
    return volume

def txtParserLatestPrice(data):
    price = data['price'].values[-1]
    return price
def txtParserPriceVolumeProduct(data):
    totalVolume = txtParserVolumeSum(data)
    currPrice = txtParserLatestPrice(data)
    return currPrice*totalVolume

def txtParserCashDifference(data):
    proposedAmount = txtParserPriceVolumeProduct(data)
    actualAmount = txtParserCashSum(data)

    return proposedAmount-actualAmount


def countDigits(num):
    n = 0
    while num >0:
        num = num//10
        n+=1
    return n

def priceIntervalVolumePercentage(data):
    min = data['price'].min()
    max = data['price'].max()

    totalVolume = txtParserVolumeSum(data)


    digits = countDigits(max)
    digits -=1
    interval = 0.1
    for i in range(digits):
        interval*=10

    interval *=0.3
    min = (min//interval)*interval
    max = (max//interval)*interval

    prices = data['price'].values
    cats =[]
    for p in prices:
        diff = p-min
        cat = min+ (diff//interval)*interval
        cats.append(cat)
    data['PriceInterval'] = cats
    d = dict(data.groupby('PriceInterval').sum()['volume'])

    x= []
    y=[]
    for k,v in d.items():
        x.append(k)
        y.append(v*100/totalVolume)
    return x,y

def priceIntervalGainLoss(data):
    x,y = priceIntervalVolumePercentage(data)
    totalVolume = txtParserVolumeSum(data)
    currPrice = txtParserLatestPrice(data)
    for i in range(len(y)):
        y[i] = totalVolume*y[i]

    for i in range(len(y)):
        diff = currPrice- x[i]
        y[i] = y[i]*diff
    return x,y





