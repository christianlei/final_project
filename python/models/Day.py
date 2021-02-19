from . import Bitcoin

class Day:
    def __init__(self, bitcoin):
        self.day = bitcoin.timestamp
        self.bitcoins = [bitcoin]
        self.average_price = float()
        self.label = None
    
    def add_bitcoin(self, bitcoin):
        self.bitcoins.append(bitcoin)

    def calcuate_average_of_bitcoin(self):
        self.average_price = sum(bitcoin.weighted_price for bitcoin in self.bitcoins)/len(self.bitcoins)

    def __str__(self):
        return str(self.day) + "," + str('%.9f' % self.average_price) + "," + str(self.label)

