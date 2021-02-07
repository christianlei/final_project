import pandas as pd
import math


df = pd.read_csv("bitcoin_raw.csv")

# Drop all days before 01-01-2012
df.drop(df.index[:968], inplace=True)
df.drop(df.index[-1], inplace=True)

df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit="s").dt.date

df = df.groupby(['Timestamp'], as_index=False).agg({'Open':'first',
    'High':'max', 'Low':'min', 'Close':'last', 'Volume_(BTC)':'sum',
    'Volume_(Currency)':'sum', 'Weighted_Price':'mean'})

#add labels
labels = []
open_list = list(df['Open'])
for i in range(len(df)-30):
    if open_list[i+30] >= open_list[i]:
        labels.append(1)
    else:
        labels.append(0)
for i in range(30):
    labels.append(math.nan)
df['labels'] = labels

df.to_csv("bitcoin.csv")