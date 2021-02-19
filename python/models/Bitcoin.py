import datetime

class Bitcoin:
    
    def __init__(self, unix_timestamp, weighted_price):
        self.original_timestamp = unix_timestamp
        self.timestamp = datetime.datetime.fromtimestamp(float(unix_timestamp)).strftime('%Y-%m-%d')
        self.weighted_price = float(weighted_price)

