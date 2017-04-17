import stocks

Loader = stocks.Loader
TradingData = stocks.TradingData
Stock = stocks.Stock
Analyser = stocks.Analyser
all_stocks = stocks.StockCollection()
volume = stocks.AverageVolume()

class LoadCSV(Loader):

    def _process(self, file):
        for data in file:
            datalist = data.split(",")

            stock = all_stocks.get_stock(datalist[0])
            day_data = TradingData(str(datalist[1]),
                                   float(datalist[2]),
                                   float(datalist[3]),
                                   float(datalist[4]),
                                   float(datalist[5]),
                                   int(datalist[6]))

            stock.add_day_data(day_data)


class LoadTriplet(Loader):

    def _process(self, file):
        datalist = []
        datalist_split = []
        stocklist = []
        codelist = []
        codelist_split = []
        valuelist = []

        for data in file:
            datalist.append(data)

        for x in range(0, len(datalist), 6):
            datalist_split.append(datalist[x:x+6])

        for data in datalist_split:
            for string in data:
                x = string.split(":")
                valuelist.append(x[2])
                codelist.append(x[0])

        for x in range(0, len(valuelist), 6):
            stocklist.append(valuelist[x:x+6])

        for x in range(0, len(codelist), 6):
            codelist_split.append(codelist[x:x+6])

        c = 0
        for x in codelist_split:
            stocklist[c].append(x[0])
            c += 1

        for data in stocklist:
            stock = all_stocks.get_stock(data[6])
            day_data = TradingData(str(data[0]),
                                   float(data[1]),
                                   float(data[2]),
                                   float(data[3]),
                                   float(data[4]),
                                   int(data[5]))
            stock.add_day_data(day_data)


class HighLow(Analyser):

    def __init__(self):
        self._total_high = []
        self._total_low = []

    def process(self, day):
        self._total_high.append(day.get_high())
        self._total_low.append(day.get_low())

    def reset(self):
        self._total_high = []
        self._total_low = []

    def result(self):
        self._total_high.sort()
        self._total_low.sort()
        return (self._total_high[-1], self._total_low[0])


class MovingAverage(Analyser):
    def __init__(self):
        pass


class GapUp(Analyser):
    def __init__(self):
        pass


LoadCSV("data_files/march1.csv", all_stocks)
LoadCSV("data_files/march2.csv", all_stocks)
LoadCSV("data_files/march3.csv", all_stocks)
LoadCSV("data_files/march4.csv", all_stocks)
LoadCSV("data_files/march5.csv", all_stocks)
LoadTriplet("data_files/feb1.trp", all_stocks)
LoadTriplet("data_files/feb2.trp", all_stocks)
LoadTriplet("data_files/feb3.trp", all_stocks)
LoadTriplet("data_files/feb4.trp", all_stocks)
LoadTriplet("data_files/march5.trp", all_stocks)

"""
#debug
print(code, 'date is:', stock.get_day_data(date).get_date(), 'type is', type(stock.get_day_data(date).get_date()))
print(code, 'open is:',stock.get_day_data(date).get_open(), 'type is', type(stock.get_day_data(date).get_open()))
print(code, 'high is:',stock.get_day_data(date).get_high(), 'type is', type(stock.get_day_data(date).get_high()))
print(code, 'low is:',stock.get_day_data(date).get_low(), 'type is', type(stock.get_day_data(date).get_low()))
print(code, 'close is:',stock.get_day_data(date).get_close(), 'type is', type(stock.get_day_data(date).get_close()))
print(code, 'volume is:',stock.get_day_data(date).get_volume(),'type is', type(stock.get_day_data(date).get_volume()))
#stocks_loaded = all_stocks._all_stocks.keys()
#print(stocks_loaded)
#print(len(stocks_loaded))

date = '20170227'
code = "ADV"
stock = all_stocks.get_stock(code)

highlow = HighLow()
stock.analyse(highlow)
print("HighLow of", code, "is", highlow.result())

#stock.analyse(volume)
#print("Average Volume of", code, "is", volume.result())
"""

