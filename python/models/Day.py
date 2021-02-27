from . import Bitcoin

class Day:
    def __init__(self, bitcoin):
        self.day = bitcoin.timestamp
        self.bitcoins = []
        self.average_price = float()
        self.number_of_bitcoin = 0
        self.label = None

    def add_bitcoin(self, bitcoin):
        self.bitcoins.append(bitcoin)
        self.number_of_bitcoin = len(self.bitcoins)

    def calculate_average_of_bitcoin(self):
        self.average_price = sum(bitcoin.weighted_price for bitcoin in self.bitcoins)/len(self.bitcoins)

    def __str__(self):
        return_string =  str(self.day) + "," + str('%.15f' % self.average_price).strip("0") + "," 
        if self.label is not None:
            return_string += str(self.label)
        return return_string

