from . import Bitcoin

class Day:
    def __init__(self, bitcoin):
        self.day = bitcoin.timestamp
        self.bitcoins = [bitcoin]
        self.average_price = None
        self.label = None
    
    def add_bitcoin(self, bitcoin):
        self.bitcoin.append(bitcoin)

    def calcuate_average_of_bitcoin(self):
        self.average_price = sum(bitcoin.weighted_price for bitcoin in self.bitcoins)/len(self.bitcoin)
    

    def __str__(self):
        return str(self.day) + "," + str(self.average_price) + "," + str(self.label)

