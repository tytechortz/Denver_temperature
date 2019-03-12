import pandas as pd
import numpy as np
import datetime

today = datetime.date.today()
start = datetime.date(1948,1,1)
period = today-start
# print(period.days)

todays_date = datetime.datetime.now().date()
# index = pd.date_range(todays_date-datetime.timedelta(period.days), periods=period.days, freq='D')
index = pd.date_range('1948-01-01', periods=period.days)


columns = ['TMAX','TMIN']

df = pd.DataFrame(index=index, columns=columns)



# df = df.fillna(0) # with 0s rather than NaNs

# print(df.loc['2001-08-31'])
# df.drop(pd.to_datetime('1948-01-20'), inplace=True)
# print(len(df))
df.loc[pd.to_datetime('2001-08-31')] = [87,54]

df = df.sort_index()

# print(df.iloc[19580:20000])
# print(df)

url = 'ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/all/USW00023062.dly'
df1 = pd.read_fwf('ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/all/USW00023062.dly', header=None, skiprows = 86 )

# filters for max temps
df_TMAX = df1[df1[0].str.contains("TMAX")]

# filters for min temps
df_TMIN = df1[df1[0].str.contains("TMIN")]

# filters first column 
df_TMAX[0] = df_TMAX[0].str[22:27]
df_TMIN[0] = df_TMIN[0].str[22:27]

#  drops last columns
df_TMAX.drop(df_TMAX.columns[-1], axis=1,inplace=True)
df_TMIN.drop(df_TMIN.columns[-1], axis=1,inplace=True)

#  makes lists of min and max temps
df2 = (df_TMAX.values.reshape(1, -1))
i = 0
max_temps = []
for x in df2[0]:
    max_temps.append(df2[0][i][-4:])
    i = i + 1

df3 = (df_TMIN.values.reshape(1, -1))
i = 0
min_temps = []
for x in df2[0]:
    min_temps.append(df2[0][i][-4:])
    i = i + 1

# removes -9999 values
max_list = list(filter(('9999').__ne__, max_temps))
min_list = list(filter(('9999').__ne__, min_temps))

# print(len(min_list))
# print(len(max_list))
# print(type(max_list))

max_array = np.asarray(max_list)
# df['TMAX'] = max_array
print(len(max_array))

