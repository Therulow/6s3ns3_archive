from .imports import *

# differences a dataframe by adding a lag
# takes in a series with a time index and value
# returns a df with time index, value and lag value but w 1 less obs
def difference_df(df, col = 0):
    if isinstance(df, pd.Series):
        df = df.to_frame()
        df = df.rename(columns = {df.columns[0]: "Value"})
        df["Diff_Value"] = df["Value"].diff()
        df = df.dropna()
        return df
    else:
        df["Diff_Value"] = df.iloc[:, col].diff()
        df = df.dropna()
        return df

#gets the most recent df of a series
# takes in the series key and end date
#returns a series whos index is date and value
def get_most_recent_series_of_date(series_key, end_date, fred):
    df = fred.get_series_as_of_date(series_key, end_date).drop_duplicates(subset = ["date"], keep = "last")
    df = pd.Series(df["value"].to_list(), index = df["date"].to_list())
    df.index = pd.to_datetime(df.index)
    df = df.dropna()
    df = df.astype("float")
    return df

#chooses the best arma model by using oos forecasting
#inputs df a time series stationary, max p and q to test and test size
def best_arma(df, start_p = 0, start_q = 0, max_p = 5, max_q = 5, test_size = 50, trend = None, freq = 'MS', exog = None, seasonal_order = (0, 0, 0, 0)):

    df = df.asfreq(freq)

    p_range = range(start_p, max_p+1) 
    q_range = range(start_q, max_q+1)  

    results = np.full((max_p-start_p+1, max_q-start_q+1),np.inf)

    for index in range(1, test_size+1):
        train = df.iloc[:-index-1]
        test = df.iloc[-index]
        for p in p_range:
            for q in q_range:
                
                try:
                    model = ARIMA(train, order=(p, 0, q), trend = trend, freq=freq, enforce_stationarity=False, enforce_invertibility=False, seasonal_order=seasonal_order)
                    model = model.fit(method_kwargs={'maxiter':100})
                    pred = model.get_forecast(steps = 1).predicted_mean
                    if results[p-start_p-1][q-start_q-1] == np.inf:
                        results[p-start_p-1][q-start_q-1] = 0
                    results[p-start_p-1][q-start_q-1] += (pred-test)**2                
                except TypeError:
                    print(f'Try other params for{(p, 0, q)}')
    print(results)
    flat_index = np.argmin(results)
    p, q = np.unravel_index(flat_index, results.shape)

    print(f'Best ARIMA model order: p={p+start_p} and q={q+start_q}')
    return p, q


# takes the rough percent change in a df
# takes in a df with a time index and value
# returns a series with time index, value and lag value but w 1 less obs
def pct_chg(df, col = 0):
    if isinstance(df, pd.Series):
        df = np.log(df)
        df = df.to_frame()
        df = df.rename(columns = {0: "Value"})
        df["pct_chg"] = df["Value"].diff()*100
        df = df.dropna()
        return df
    else:
        df["pct_chg"] = np.log(df.iloc[:, col]).diff()*100
        df= df.dropna()
        return df
    
# Function to plot ACF and PACF
#takes in a time series then plots the acf and pacf
def plot_acf_pacf(timeseries):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7))
    plot_acf(timeseries, ax=ax1, lags=75)
    plot_pacf(timeseries, ax=ax2, lags=75)
    plt.show()

# prints various eval metrics
#takes in test and pred as series, does not return, prints out required metrics
def eval(test, pred, plot = True):
    # #plotting of resid
    if plot:
        fig, ax = plt.subplots()
        ax.plot(test)
        ax.plot(pred)
        plt.show()
    rmse = mean_squared_error(test, pred, squared=False)
    print(f'Root Mean Squared Error: {rmse}')

    mae = mean_absolute_error(test, pred)
    print(f'Mean Absolute Error: {mae}')
    
    directional_pred = (pred.apply(lambda x: 1 if x > 0 else -1) == test.apply(lambda x: 1 if x > 0 else -1)).sum() / len(test)

    print(f'Directional Accuracy: {directional_pred}')

# obtained from https://fg-research.com/blog/general/posts/fred-md-overview.html
def transform_series(x, tcode):
    '''
    Transform the time series.

    Parameters:
    ______________________________
    x: pandas.Series
        Time series.

    tcode: int.
        Transformation code.
    '''

    if tcode == 1:
        return x
    elif tcode == 2:
        return x.diff()
    elif tcode == 3:
        return x.diff().diff()
    elif tcode == 4:
        return np.log(x)
    elif tcode == 5:
        return np.log(x).diff()
    elif tcode == 6:
        return np.log(x).diff().diff()
    elif tcode == 7:
        return x.pct_change()
    else:
        raise ValueError(f"unknown `tcode` {tcode}")
    


# takes in multiple data frames contating the test data, predictions from the first model and second model
# returns the dmstat, pvalue HAC SE and the mean loss diff
def dm_test(test, pred1, pred2):
    test = np.asarray(test).flatten()
    pred1 = np.asarray(pred1).flatten()
    pred2 = np.asarray(pred2).flatten()
    e1 = pred1-test
    e2= pred2-test
    d = e1**2 - e2**2

    lags = int(50**.33)
    mean = np.mean(d)
    
    resid = d-mean
    model = sm.OLS(resid, np.ones(50))
    model = model.fit(cov_tyoe = 'HAC', cov_kwds={'maxlags':lags, 'kernel':'newey-west'})
    se = model.bse[0]

    dm_stat = mean/se
    p_value = 2 * (1 - scipy.stats.norm.cdf(abs(dm_stat)))

    return dm_stat, p_value, se, mean