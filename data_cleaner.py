import pandas as pd
from datetime import datetime

df = pd.read_csv("bitcoin.csv")
# df = df.Timestamp.astype(str)
# df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit="s")
df.dropna()

print(df.head(100))

# df.to_csv("bitcoin.csv")
# df.Timestamp.strftime('%Y-%m-%d')

# if you encounter a "year is out of range" error the timestamp
# may be in milliseconds, try `ts /= 1000` in that case
