"""This program will load stock data from the stock market and perform simple
analysis on the data. 
    
    __author__ = Xinyi Li
    student number = 
    __email__ = xinyi.li4@uqconnect.edu.au
"""

import stocks

Loader = stocks.Loader
TradingData = stocks.TradingData
Stock = stocks.Stock
Analyser = stocks.Analyser


class LoadCSV(Loader):
    """Subclass of stocks.Loader, handles the processing and loading of .csv 
    files. LoadCSV also handles invalid data types/structures and exceptions from 
    the data.
    """

    def __init__(self, filename, stocks):
        """Inherited parameters from stocks.Loader.
        
        Parameters:
            filename (str): Name of the file from which to load data.
            stocks (StockCollection): Collection of existing stock market 
            data to which the new data will be added.
        """
        super().__init__(filename, stocks)
        self._file_validate(filename)
        

    def _process(self, file):
        """Processes and extracts data from .csv files and determines whether
        if the data is valid before adding the data to the appropriate 
        stock object.
       
        Parameters:
            file (TextIOWrapper): Object of filename opened.
            
        Raises:
            RuntimeError: If the data structure is invalid.
        """
        for data in file:
            datalist = data.split(",")
            if len(datalist) == 7 and len(datalist[0]) >= 3:
                stock = self._stocks.get_stock(datalist[0])
                try:
                    int(datalist[1])
                    stock.add_day_data(TradingData(str(datalist[1]),
                                                 float(datalist[2]),
                                                 float(datalist[3]),
                                                 float(datalist[4]),
                                                 float(datalist[5]),
                                                 int(datalist[6])))

                except ValueError:
                    raise RuntimeError
            else:
                raise RuntimeError

    @staticmethod
    def _file_validate(filename):
        """Validates whether if the file has the correct extension.
        
        Raises:
            RuntimeError: If the filename does not have the correct extension
        """
        extension = filename.split(".")
        if extension[-1] != "csv":
            raise RuntimeError
        

class LoadTriplet(Loader):
    """Subclass of stocks.Loader, handles the processing and loading of .trp 
    files. LoadTriplet also handles invalid data types/structures and exceptions 
    from the data.
    """

    def __init__(self, filename, stocks):
        """Inherited parameters from stocks.Loader.
        
        Parameters:
            filename (str): Name of the file from which to load data.
            stocks (StockCollection): Collection of existing stock market data
                                      to which the new data will be added.
        """
        super().__init__(filename, stocks)
        self._file_validate(filename)
        

    def _process(self, file):
        """Processes and extracts data from .trp files and determines whether
        if the data is valid before adding the data to the appropriate 
        stock object. 

        Parameters:
            file (TextIOWrapper): Object of filename opened.

        Raises:
            RuntimeError: If the data structure is invalid.
        """
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
                    try:
                        valuelist.append(x[2])
                        codelist.append(x[0])
                    except IndexError:
                        raise RuntimeError
                            
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
                stock = self._stocks.get_stock(data[6])
                try:
                    int(data[0])
                    stock.add_day_data(TradingData(str(data[0]),
                                                 float(data[1]),
                                                 float(data[2]),
                                                 float(data[3]),
                                                 float(data[4]),
                                                 int(data[5])))
                except ValueError:
                    raise RuntimeError
        else:
            raise RuntimeError

    @staticmethod
    def _file_validate(filename):
        """Validates whether if the file has the correct extension.

        Raises:
            RuntimeError: If the filename does not have the correct extension
        """
        extension = filename.split(".")
        if extension[-1] != "trp":
            raise RuntimeError


class HighLow(Analyser):
    """Subclass of Analyser. Provides access to high low analysis of stock data
    """

    def __init__(self):
        """Initialise lists which will contain data for processing.
        """
        self._total_high = []
        self._total_low = []

    def process(self, day):
        """Retrieves and processes the data to analyse stock's highest and 
        lowest trades.
        
        Parameters:
            day (TradingData): Trading data for one stock on one day.
        """
        self._total_high.append(day.get_high())
        self._total_high.sort()
        self._total_low.append(day.get_low())
        self._total_low.sort()

    def reset(self):
        """Reset the analysis process in order to perform a new analysis."""
        self._total_high = []
        self._total_low = []

    def result(self):
        """Returns the result of the high low analysis and checks for 
        exception from the data.
        
        Returns:
             tuple: Containing the highest trade and lowest trade of the stock.
             
        Raises:
            ValueError: If an IndexError occurs while returning the results.
        """
        try:
            return self._total_high[-1], self._total_low[0]
        except IndexError:
            raise ValueError


class MovingAverage(Analyser):
    """Subclass of Analyser. Provides access to moving average analysis of 
       stock data
    """

    def __init__(self, num_days):
        """Initialise the variables and list which will contain data 
        for processing.
        
        Parameters
            num_days(int): The number of days over to process
            
        Preconditions
            num_days > 0
        """
        self._num_days = num_days
        self._closing_total = 0
        self._data = []

    def process(self, day):
        """Retrieves and processes the data to analyse stock's moving average.

        Parameters:
            day (TradingData): Trading data for one stock on one day.
        
        Raises:
            ValueError: If the parameter num_days is less or equal to 0
        """
        self._data.append(day.get_close())
        if self._num_days <= 0 or type(self._num_days) == float:
            raise ValueError

        if len(self._data) >= self._num_days:
            while len(self._data) > self._num_days:
                del self._data[0]
                self._closing_total = sum(self._data)


    def reset(self):
        """Reset the analysis process in order to perform a new analysis."""
        self._closing_total = 0
        self._data = []

    def result(self):
        """Returns the result of the moving average analysis
        
        Returns:
            int: Moving average of the stock across the specified number of 
            days.
        """
        return self._closing_total / self._num_days


class GapUp(Analyser):
    """Subclass of Analyser. Provides access to gap up analysis of 
       stock data
    """
    def __init__(self, delta):
        """Initialise the variables and lists which will contain data 
        for processing.

        Parameters
            delta(int): Determine whether if the price difference is significant
            or not.
        """
        self._delta = delta
        self._opening = []
        self._closing = []
        self._date = 0

    def process(self, day):
        """Retrieves and processes the data to analyse and determine the
        stock's latest gap up date according to the delta value.

        Parameters:
            day (TradingData): Trading data for one stock on one day.

        Raises:
            ValueError: If the parameter num_days is 0
        """
        self._opening.append(day.get_open())
        self._closing.append(day.get_close())

        if len(self._closing) > 1:
            if self._opening[-1] - self._closing[-2] > self._delta:
                self._date = day
        else:
            self._date = None

    def reset(self):
        """Reset the analysis process in order to perform a new analysis."""
        self._opening = []
        self._closing = []
        self._date = 0

    def result(self):
        """Returns the result of the gap up analysis.
        
        Returns:
            TradingData: The trading data object containing all trading data
            of a particular day.
        """
        return self._date


def example_usage () :
    all_stocks = stocks.StockCollection()
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
    stock = all_stocks.get_stock("ADV")
    stock.analyse(volume)
    print("Average Volume of ADV is", volume.result())
    high_low = HighLow()
    stock.analyse(high_low)
    print("Highest & Lowest trading price of ADV is", high_low.result())
    moving_average = MovingAverage(10)
    stock.analyse(moving_average)
    print("Moving average of ADV over last 10 days is {0:.2f}"
          .format(moving_average.result()))
    gap_up = GapUp(0.011)
    stock = all_stocks.get_stock("YOW")
    stock.analyse(gap_up)
    print("Last gap up date of YOW is", gap_up.result().get_date())

    
if __name__ == "__main__" :
    example_usage()
