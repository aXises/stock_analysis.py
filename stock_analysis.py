import stocks

Loader = stocks.Loader
TradingData = stocks.TradingData
StockDict = {}

class LoadCSV(Loader):

    def __init__(self, filename, stocks):
        super().__init__(filename, stocks)

    def _process(self, file):
        for data in file:
            datalist = data.split(",")
            StockDict[datalist[0]] = TradingData(datalist[1],
                                                 datalist[2],
                                                 datalist[3],
                                                 datalist[4],
                                                 datalist[5],
                                                 datalist[6])
        return StockDict


class LoadTriplet(Loader):
    def __init__(self, filename, stocks):
        super().__init__(filename, stocks)

    def _process(self, file):
        for data in file:
            print(data)
        return StockDict


"""Debug
test = LoadTriplet('feb1.trp', stocks)
#print(StockDict)
print(StockDict['EDE'].get_date())
test2 = TradingData(1,2,3,4,5,6)
print(test2.get_date())
#print(test._process('march1.csv'))
"""