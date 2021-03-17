import pandas as pd
import numpy as np
from datetime import datetime
# import matplotlib.pyplot as plt
import math


pd.set_option("display.max_rows", 100)
df = pd.read_csv("bitcoin_raw.csv")
# df = df.Timestamp.astype(str)
df['Open'].replace('', np.nan, inplace=True)
df.dropna(how='any', inplace=True)
# df.drop(df.index[:968], inplace=True)
df.drop(df.index[:4], inplace=True)

# df.tz_localize('UTC')

df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit="s").dt.date
# df = df.groupby(['Timestamp'], as_index=False).agg({'Open':'first',
#     'High':'max', 'Low':'min', 'Close':'last', 'Volume_(BTC)':'sum',
#     'Volume_(Currency)':'sum', 'Weighted_Price':'mean'})

df_group_by_day = df.groupby(df["Timestamp"]).count()
df.to_csv("bitcoin_timestamps_as_dates.csv")
df_group_by_day.to_csv("bitcoin_groupby.csv")
# print(df_group_by_day[df_group_by_day["Timestamp"] == "2012-09-16"])


#df["time"] = (
#    pd.to_datetime(df["Timestamp"]).dt.hour * 3600 + pd.to_datetime(df["Timestamp"]).dt.minute * 60)

#print(df)

# BEGIN TODAY
#df.drop('Weighted_Price', axis=1, inplace=True)


#add labels
# labels = []
# open_list = list(df['Open'])
# for i in range(len(df)-30):
#     if open_list[i+30] >= open_list[i]:
#         labels.append(1)
#     else:
#         labels.append(0)
# for i in range(30):
#     labels.append(math.nan)
# df['labels'] = labels


# print(df[100:200])



# END TODAY

# SCRATCH

#print(df[2625370: 2625380])

"""
Days = [set() for x in range(1460)]
offset = 2625376
print('before')
print(df.iloc[offset])
print('after')
seconds_with_nan = [set() for x in range(1460)]

open_list = list(df["Open"])
time_list = list(df["time"])
for day in range(1460):
    for minute in range(1440):
        row = day * 1440 + minute * 60
        value = open_list[day * 1440 + minute]
        curr_second = time_list[day * 1440 + minute]
        if not math.isnan(value):
            Days[day].add(curr_second)
        else:
            seconds_with_nan[day].add(curr_second)
"""

# max = 0
# max_day = 0
# for x in range(len(seconds_with_nan)):
#     if len(seconds_with_nan[x]) > max:
#         max = len(seconds_with_nan[x])
#         max_day = x
# print("max", max)
# print("max_day", max_day)


# I = Days[0]
# for i in range(1, 1460):
#     I = I.intersection(Days[i])
# print('I has length: '+str(len(I)))
# print(I)

# print(df.head)
# print(df.loc[df["Timestamp"] == "2017-01-01 00:00:00"])
# print(df["Timestamp"].get_loc("2017-01-01 00:00:00"))
#df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit="s").dt.date
# df["Timestamp"] = pd.Timestamp(df.index.Timestamp).date()

# print(df.groupby(df["Timestamp"]).count())

#df_group_by_day = df.groupby(df["Timestamp"]).count()
# print(df_group_by_day)
# print("count: \n", df_group_by_day.count())

# print(df_group_by_day)
# print(df)
# print(df.iloc[0])
# print(df.iloc[1459])
# # print(df_group_by_day.head())
# df_group_by_day.plot(y=["Open", "High", "Low", "Close", "Volume_(BTC)"])
#df_group_by_day.plot(y=["Open"])
#df.plot(y=["time"])
#plt.show()
# print(df.head(5))
# print(pd.to_datetime(df["Timestamp"]).date.count())
# df.dropna()

# print(df.head(100))

# df_group_by_day.to_csv("bitcoin.csv")
# df.Timestamp.strftime('%Y-%m-%d')

# if you encounter a "year is out of range" error the timestamp
# may be in milliseconds, try `ts /= 1000` in that case
