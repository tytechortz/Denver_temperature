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

df1 = pd.DataFrame(index=index, columns=columns)
df1 = df1.fillna(0) # with 0s rather than NaNs
    
print(df1)