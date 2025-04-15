from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

df = get_most_recent_series_of_date("GDP", "2020-01-01", fred)
df = pct_chg(df)

df.pct_chg.plot()
plt.show()

#looks like white noise but need to demean
df_demean = df.pct_chg-df.pct_chg.mean()
df_demean.plot()
plt.show()

# testing for stationarity may be stationary as power is low
print("ADF Test Result: ", adfuller(df.pct_chg))
# First diff shows significant improvement thus can conclude that first diff is stationary
df = difference_df(df, 1)
# print("ADF Test Result: ", adfuller(df['Diff_Value']))
diff_df = df['Diff_Value']

#might want to take first difference of gdp
sahm = get_most_recent_series_of_date("SAHMREALTIME", "2020-01-01", fred)

