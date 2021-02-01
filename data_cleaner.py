import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt


pd.set_option("display.max_rows", 100)
df = pd.read_csv("bitcoin_raw.csv")
# df = df.Timestamp.astype(str)
df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit="s").dt.date
# df["Timestamp"] = pd.Timestamp(df.index.Timestamp).date()

# print(df.groupby(df["Timestamp"]).count())

df_group_by_day = df.groupby(df["Timestamp"]).count()
df_of_1440 = df_group_by_day[df_group_by_day["Open"] == 1440]
ts = pd.DataFrame(
    np.random.randn(1000, 4),
    index=df_of_1440["Timestamp"],
    columns=df_of_1440["High"],
)
print(df_of_1440)

# print(df.head(5))
# print(pd.to_datetime(df["Timestamp"]).date.count())
# df.dropna()

# print(df.head(100))

# df_group_by_day.to_csv("bitcoin.csv")
# df.Timestamp.strftime('%Y-%m-%d')

# if you encounter a "year is out of range" error the timestamp
# may be in milliseconds, try `ts /= 1000` in that case
