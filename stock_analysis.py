import stocks

Loader = stocks.Loader
TradingData = stocks.TradingData
Stock = stocks.Stock
Analyser = stocks.Analyser
all_stocks = stocks.StockCollection()


class LoadCSV(Loader):

    def __init__(self, filename, stocks):
        Loader.__init__(self, filename, stocks)
        self._filename = filename
        self.file_validate(self._filename)

    def _process(self, file):
        for data in file:
            datalist = data.split(",")
            if len(datalist) == 7 and len(datalist[0]) >= 3:
                stock = all_stocks.get_stock(datalist[0])
                try:
                    int(datalist[1])
                    try:
                        day_data = TradingData(str(datalist[1]),
                                               float(datalist[2]),
                                               float(datalist[3]),
                                               float(datalist[4]),
                                               float(datalist[5]),
                                               int(datalist[6]))
                    except ValueError:
                        raise RuntimeError
                    stock.add_day_data(day_data)
                except ValueError:
                    raise RuntimeError
            else:
                raise RuntimeError

    @staticmethod
    def file_validate(filename):
        extension = filename.split(".")
        if extension[-1] != "csv":
            raise RuntimeError
        else:
            pass


class LoadTriplet(Loader):

    def __init__(self, filename, stocks):
        Loader.__init__(self, filename, stocks)
        self._filename = filename
        self.file_validate(self._filename)

    def _process(self, file):
        datalist = []
        datalist_split = []
        stocklist = []
        codelist = []
        codelist_split = []
        valuelist = []

        for data in file:
            datalist.append(data)

        if len(datalist) % 6 == 0:

            for x in range(0, len(datalist), 6):
                datalist_split.append(datalist[x:x+6])

            for data in datalist_split:
                for string in data:
                    x = string.split(":")
                    valuelist.append(x[2])
                    codelist.append(x[0])

            for code in codelist:
                if len(code) < 3:
                    raise RuntimeError

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
                try:
                    int(data[0])
                    try:
                        day_data = TradingData(str(data[0]),
                                               float(data[1]),
                                               float(data[2]),
                                               float(data[3]),
                                               float(data[4]),
                                               int(data[5]))
                    except ValueError:
                        raise RuntimeError
                except ValueError:
                    raise RuntimeError
                stock.add_day_data(day_data)
        else:
            raise RuntimeError

    @staticmethod
    def file_validate(filename):
        extension = filename.split(".")
        if extension[-1] != "trp":
            raise RuntimeError
        else:
            pass


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
        return self._total_high[-1], self._total_low[0]


class MovingAverage(Analyser):

    def __init__(self, num_days):
        self._num_days = num_days
        self._closing_total = 0
        self._data = []

    def process(self, day):
        self._data.append(day.get_close())

        if len(self._data) >= self._num_days:
            while len(self._data) > self._num_days:
                del self._data[0]
                self._closing_total = sum(self._data)

    def reset(self):
        self._closing_total = 0
        self._data = []

    def result(self):
        return self._closing_total / self._num_days


class GapUp(Analyser):

    def __init__(self, delta):
        self._delta = delta
        self._opening = []
        self._closing = []
        self._date = 0

    def process(self, day):
        self._opening.append(day.get_open())
        self._closing.append(day.get_close())

        if len(self._closing) > 1:
            if self._opening[-1] - self._closing[-2] > self._delta:
                self._date = day
        else:
            self._date = None

    def reset(self):
        self._opening = []
        self._closing = []
        self._date = 0

    def result(self):
        return self._date


LoadCSV("data_files/march1.csv", all_stocks)
LoadCSV("data_files/march2.csv", all_stocks)
LoadCSV("data_files/march3.csv", all_stocks)
LoadCSV("data_files/march4.csv", all_stocks)
LoadCSV("data_files/march5.csv", all_stocks)
LoadTriplet("data_files/feb1.trp", all_stocks)
LoadTriplet("data_files/feb2.trp", all_stocks)
LoadTriplet("data_files/feb3.trp", all_stocks)
LoadTriplet("data_files/feb4.trp", all_stocks)

volume = stocks.AverageVolume()
code = "ADV"
stock = all_stocks.get_stock(code)
stock.analyse(volume)
print("Average Volume of", code ,"is", volume.result())
high_low = HighLow()
stock.analyse(high_low)
print("Highest & Lowest trading price of", code ,"is", high_low.result())
moving_average = MovingAverage(4)
stock.analyse(moving_average)
print("Moving average of", code ,"over last 4 days is {0:.2f}"
      .format(moving_average.result()), moving_average.result())
gap_up = GapUp(0.0009)
stock.analyse(gap_up)
print("Last gap up date of", code,"is", gap_up.result().get_date())
