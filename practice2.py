import pandas as pd
import numpy as np
import datetime

today = datetime.date.today()
start = datetime.date(1948,1,1)
period = today-start
print(period.days)

todays_date = datetime.datetime.now().date()
index = pd.date_range(todays_date-datetime.timedelta(period.days), periods=period.days, freq='D')

columns = ['TMAX','TMIN']

df = pd.DataFrame(index=index, columns=columns)
df = df.fillna(0) # with 0s rather than NaNs
    
url = 'ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/all/USW00023062.dly'
df1 = pd.read_fwf('ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/all/USW00023062.dly', header=None, skiprows = 86 )

# filters for max temps
df_TMAX = df1[df1[0].str.contains("TMAX")]

# filters for min temps
df_TMIN = df1[df1[0].str.contains("TMIN")]

# filters first column 
df_TMAX[0] = df_TMAX[0].str[22:27]
df_TMIN[0] = df_TMIN[0].str[22:27]

df_TMAX.drop(df_TMAX.columns[-1], axis=1,inplace=True)
df_TMIN.drop(df_TMIN.columns[-1], axis=1,inplace=True)

