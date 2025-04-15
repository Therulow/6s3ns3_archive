from .package_imports import *

# takes in the given dates and return values up to the date if have if not predict
#takes in given date and period, so 'Q' or 'M' for bridge or midas
def quart_pct_chg_pce(given_date = "2020-01-01", period = 'Q'):
    fred = Fred(api_key = os.getenv("API_KEY"))
    df = get_most_recent_series_of_date("PCE", given_date, fred)
    pct_chg_pce = transform_series(df, 5).dropna()*100
    model = ARIMA(pct_chg_pce, order=(4, 0, 3), trend = 'c', freq = 'MS').fit(method_kwargs={'maxiter':300})
    start_date_pred = pct_chg_pce.index[-1]+ pd.offsets.MonthBegin(1)
    end_date_pred = pd.Period(given_date, freq='Q').end_time.to_period(freq='M').start_time
    pred = model.predict(start = start_date_pred, end = end_date_pred)
    pct_chg_pred = pd.concat([pct_chg_pce, pred])
    print("Consumption data Loaded")
    if period == 'M':
        return pct_chg_pred
    elif period == 'Q':
        quarterly_pct_chage = pct_chg_pred.resample('QS').sum()
        return quarterly_pct_chage
    
# takes in the given dates and return values up to the date if have if not predict
#takes in given date and period, so 'Q' or 'M' for bridge or midas
def quart_pct_chg_biz_equip(date = "2020-01-01", period = 'Q'):
    fred = Fred(api_key = os.getenv("API_KEY"))
    if date<"2008-01-01":     
        df = get_most_recent_series_of_date("IPBUSEQ", "2008-01-01", fred)
        df = df[df.index<pd.Timestamp(date).to_period('M').start_time - pd.offsets.MonthBegin(1)]
    else:
        df = get_most_recent_series_of_date("IPBUSEQ", date, fred)
    pct_chg_business_equipment = transform_series(df, 5).dropna()*100
    model = ARIMA(pct_chg_business_equipment, order=(5, 0, 8), trend = 'c', freq = 'MS').fit(method_kwargs={'maxiter':200})
    start_date_pred = pct_chg_business_equipment.index[-1]+ pd.offsets.MonthBegin(1)
    end_date_pred = pd.Period(date, freq='Q').end_time.to_period(freq='M').start_time
    pred = model.predict(start = start_date_pred, end = end_date_pred)
    pct_chg_pred = pd.concat([pct_chg_business_equipment, pred])
    print("Business Equipment data Loaded")
    if period == 'M':
        return pct_chg_pred
    elif period == 'Q':

        quarterly_pct_chage = pct_chg_pred.resample('QS').sum()
        return quarterly_pct_chage

def quart_pct_chg_business_inventories(date = "2020-01-01", period = 'Q'):
    fred = Fred(api_key = os.getenv("API_KEY"))
    df = get_most_recent_series_of_date("BUSINV", date, fred)
    pct_chg_business_inventories = transform_series(df, 5).dropna()*100
    model = ARIMA(pct_chg_business_inventories, order=(5, 0, 8), trend = 'c', freq = 'MS').fit(start_params = np.full(20, .01), method_kwargs={'maxiter':300})
    start_date_pred = pct_chg_business_inventories.index[-1]+ pd.offsets.MonthBegin(1)
    end_date_pred = pd.Period(date, freq='Q').end_time.to_period(freq='M').start_time
    pred = model.predict(start = start_date_pred, end = end_date_pred)
    pct_chg_pred = pd.concat([pct_chg_business_inventories, pred])
    print("Business Inventories data Loaded")
    if period == 'M':
        return pct_chg_pred
    elif period == 'Q':
        quarterly_pct_chage = pct_chg_pred.resample('QS').sum()
        return quarterly_pct_chage
    
# takes in the given dates and return values up to the date if have if not predict
#takes in given date and period, so 'Q' or 'M' for bridge or midas
def quart_pct_chg_comm_loans(date = "2020-01-01", period = 'Q'):
    fred = Fred(api_key = os.getenv("API_KEY"))
    df = get_most_recent_series_of_date("BUSLOANS", date, fred)
    pct_chg_comms_loans = transform_series(df, 5).dropna()*100
    model = ARIMA(pct_chg_comms_loans, order=(2, 0, 12), trend = 'c', freq = 'MS').fit(start_params = np.full(20, .01), method_kwargs={'maxiter':200})
    start_date_pred = pct_chg_comms_loans.index[-1]+ pd.offsets.MonthBegin(1)
    end_date_pred = pd.Period(date, freq='Q').end_time.to_period(freq='M').start_time
    pred = model.predict(start = start_date_pred, end = end_date_pred)
    pct_chg_pred = pd.concat([pct_chg_comms_loans, pred])
    print("Com Loans data Loaded")
    if period == 'M':
        return pct_chg_pred
    elif period == 'Q':
        quarterly_pct_chage = pct_chg_pred.resample('QS').sum()
        return quarterly_pct_chage

# takes in the given dates and return values up to the date if have if not predict
#takes in given date and period, so 'Q' or 'M' for bridge or midas
def quart_pct_chg_exports(date = "2020-01-01", period = 'Q'):
    fred = Fred(api_key = os.getenv("API_KEY"))
    if date<"2010-05-01":
        df = get_most_recent_series_of_date("BOPTEXP", "2010-05-01", fred)
        df = df[df.index<pd.Timestamp(date).to_period('M').start_time - pd.offsets.MonthBegin(1)]
    else:
        df = get_most_recent_series_of_date("BOPTEXP", date, fred)        
    pct_chg_exports = transform_series(df, 5).dropna()*100
    model = ARIMA(pct_chg_exports, order=(5, 0, 5), trend = 'c', freq = 'MS').fit(start_params = np.full(5+5+1+1, .01), method_kwargs={'maxiter':300})
    start_date_pred = pct_chg_exports.index[-1]+ pd.offsets.MonthBegin(1)
    end_date_pred = pd.Period(date, freq='Q').end_time.to_period(freq='M').start_time
    pred = model.predict(start = start_date_pred, end = end_date_pred)
    pct_chg_pred = pd.concat([pct_chg_exports, pred])
    print("Exports data Loaded")
    if period == 'M':
        return pct_chg_pred
    elif period == 'Q':
        quarterly_pct_chage = pct_chg_pred.resample('QS').sum()
        return quarterly_pct_chage

# takes in the given dates and return values up to the date if have if not predict
#takes in given date and period, so 'Q' or 'M' for bridge or midas
def quart_pct_chg_govt_constr(date = "2020-01-01", period = 'Q'):
    fred = Fred(api_key = os.getenv("API_KEY"))
    if date<"2011-07-01":
        df = get_most_recent_series_of_date("TLPBLCONS", "2011-07-01", fred)
        df = df[df.index<pd.Timestamp(date).to_period('M').start_time - pd.offsets.MonthBegin(1)]
    else:
        df = get_most_recent_series_of_date("TLPBLCONS", date, fred)        
    pct_chg_govt_constr = transform_series(df, 5).dropna()*100
    model = ARIMA(pct_chg_govt_constr, order=(1, 0, 1), trend = 'c', freq = 'MS').fit(start_params = np.full(1+1+1+1, .01), method_kwargs={'maxiter':300})
    start_date_pred = pct_chg_govt_constr.index[-1]+ pd.offsets.MonthBegin(1)
    end_date_pred = pd.Period(date, freq='Q').end_time.to_period(freq='M').start_time
    pred = model.predict(start = start_date_pred, end = end_date_pred)
    pct_chg_pred = pd.concat([pct_chg_govt_constr, pred])
    print("Govt Constr data Loaded")
    if period == 'M':
        return pct_chg_pred
    elif period == 'Q':
        quarterly_pct_chage = pct_chg_pred.resample('QS').sum()
        return quarterly_pct_chage

# takes in the given dates and return values up to the date if have if not predict
#takes in given date and period, so 'Q' or 'M' for bridge or midas
def quart_pct_chg_defence(date = "2020-01-01"):
    fred = Fred(api_key = os.getenv("API_KEY"))
    df = get_most_recent_series_of_date("FDEFX", date, fred)
    pct_chg_fed_defence = transform_series(df, 5).dropna()*100
    model = ARIMA(pct_chg_fed_defence, order=(2, 0, 3), trend = 'c', freq = 'QS').fit(start_params = np.full(2+3+1+1, .01))
    start_date_pred = pct_chg_fed_defence.index[-1]+ pd.offsets.QuarterBegin(1)
    end_date_pred = pd.Period(date, freq='Q').start_time
    pred = model.predict(start = start_date_pred, end = end_date_pred)
    quarterly_pct_chage = pd.concat([pct_chg_fed_defence, pred])
    print("Defence data Loaded")
    return quarterly_pct_chage

def quart_pct_chg_housing_units_started(given_date = "2020-01-01", period = 'Q'):
    fred = Fred(api_key = os.getenv("API_KEY"))
    df = get_most_recent_series_of_date("HOUST", given_date, fred)
    df = df[df.index<pd.Timestamp(given_date).to_period('M').start_time - pd.offsets.MonthBegin(1)]
    pct_chg_housing_units_started = transform_series(df, 4)
    model = ARIMA(pct_chg_housing_units_started, order=(3, 0, 16), trend = 'c', freq = 'MS').fit(start_params = np.full(25, .01), method_kwargs={'maxiter':200})
    start_date_pred = pct_chg_housing_units_started.index[-1]+ pd.offsets.MonthBegin(1)
    end_date_pred = pd.Period(given_date, freq='Q').end_time.to_period(freq='M').start_time
    pred = model.predict(start = start_date_pred, end = end_date_pred)
    pct_chg_pred = pd.concat([pct_chg_housing_units_started, pred])
    print("Housing data Loaded")
    if period == 'M':
        return pct_chg_pred
    elif period == 'Q':
        exp = np.exp(pct_chg_pred)
        quarterly_pct_chage = exp.resample('QS').sum()
        quarterly_pct_chage = np.log(quarterly_pct_chage)
        return quarterly_pct_chage
    
def quart_pct_chg_imports(date = "2020-01-01", period = 'Q'):
    fred = Fred(api_key = os.getenv("API_KEY"))
    if date<"2010-05-01":
        df = get_most_recent_series_of_date("BOPTIMP", "2010-05-01", fred)
        df = df[df.index<pd.to_datetime(date).to_period('M').start_time - pd.offsets.MonthBegin(1)]
    else:
        df = get_most_recent_series_of_date("BOPTIMP", date, fred)        
    pct_chg_imports = transform_series(df, 5).dropna()*100
    model = ARIMA(pct_chg_imports, order=(3, 0, 4), trend = 'c', freq = 'MS').fit(start_params = np.full(3+4+1+1, .01))
    start_date_pred = pct_chg_imports.index[-1]+ pd.offsets.MonthBegin(1)
    end_date_pred = pd.Period(date, freq='Q').end_time.to_period(freq='M').start_time
    pred = model.predict(start = start_date_pred, end = end_date_pred)
    pct_chg_pred = pd.concat([pct_chg_imports, pred])
    print("Imports data Loaded")
    if period == 'M':
        return pct_chg_pred
    elif period == 'Q':
        quarterly_pct_chage = pct_chg_pred.resample('QS').sum()
        return quarterly_pct_chage

def quart_pct_cap(date = "2020-01-01", period = 'Q'):
    fred = Fred(api_key = os.getenv("API_KEY"))
    if date<"2011-07-01":
        df = get_most_recent_series_of_date("ANDENO", "2011-07-01", fred)
        df = df[df.index<pd.Timestamp(date).to_period('M').start_time - pd.offsets.MonthBegin(1)]
    else:
        df = get_most_recent_series_of_date("ANDENO", date, fred)
    pct_chg_fed_defence = transform_series(df, 5).dropna()*100
    model = ARIMA(pct_chg_fed_defence, order=(0, 0, 6), trend = 'c', freq = 'MS').fit(start_params = np.full(6+2, .01))
    start_date_pred = pct_chg_fed_defence.index[-1]+ pd.offsets.MonthBegin(1)
    end_date_pred = pd.Period(date, freq='Q').end_time.to_period(freq='M').start_time
    pred = model.predict(start = start_date_pred, end = end_date_pred)
    pct_chg_pred = pd.concat([pct_chg_fed_defence, pred])
    print("Capital Goods data Loaded")
    if period == 'M':
        return pct_chg_pred
    elif period == 'Q':
        quarterly_pct_chage = pct_chg_pred.resample('QS').sum()
        return quarterly_pct_chage
    
def sahms(date = "2020-01-01", period = 'Q'):
    fred = Fred(api_key = os.getenv("API_KEY"))
    un = get_most_recent_series_of_date("UNRATE", date, fred)
    ma3 = un.rolling(window = 3).mean()
    ma12 = un.rolling(window = 12).mean()
    sahm = ma3-ma12
    lag_sahm = sahm.shift()
    indicator = ((sahm>=.5)&(sahm>=lag_sahm)).astype(int)
    quarter_end = pd.to_datetime(date) + pd.offsets.QuarterEnd(1)
    new_dates = pd.date_range(start = indicator.index.max() + pd.offsets.MonthBegin(1), end = quarter_end, freq='MS')
    new_rows = pd.Series(np.nan, index=new_dates)
    indicator = pd.concat([indicator, new_rows])
    indicator = indicator.ffill()
    print('SAHM data Loaded')
    if period == 'M':
        return indicator
    elif period == 'Q':
        weights = np.array([.1, .3, .6])
        weighted = indicator.rolling(window=3, min_periods=3).apply(lambda x: np.dot(x, weights), raw = True)
        quarterly = weighted.resample('QS').last()
        return quarterly


def load_data_bridge(given_date = "2020-01-01"):
    root_dir = os.path.abspath(os.getcwd())
    file = os.path.join(root_dir, "Components", "test_data_bridge", f"data_iteration_{given_date}.pkl")
    # file = f'Components/test_data_bridge/data_iteration_{given_date}.pkl'
    if os.path.exists(file):
        with open(file, 'rb') as f:
            print("Bridge Data Loaded")
            return pickle.load(f)        
    fred = Fred(api_key = os.getenv("API_KEY"))
    df = get_most_recent_series_of_date("GDP", given_date, fred)
    df = pct_chg(df)
    df = df.pct_chg
    if df.index.max() < pd.to_datetime(given_date) - pd.offsets.QuarterBegin(2):
        model = AutoReg(df, lags = 4, trend = 'ct').fit()
        pred = model.predict(start = len(df), end = len(df))
        quarter_end = pd.to_datetime(given_date) - pd.offsets.QuarterEnd(1)
        new_dates = pd.date_range(start = df.index.max() + pd.offsets.MonthBegin(1), end = quarter_end, freq='QS')
        new_rows = pd.Series(pred, index=new_dates)
        df = pd.concat([df, new_rows])
    lag_gdp = df.copy()
    lag_gdp.index = lag_gdp.index + pd.DateOffset(months = 3)
    compiled = pd.concat([quart_pct_chg_pce(given_date), quart_pct_chg_govt_constr(given_date),
                      quart_pct_chg_business_inventories(given_date), quart_pct_chg_comm_loans(given_date),
                      quart_pct_chg_exports(given_date), quart_pct_cap(given_date),
                      quart_pct_chg_biz_equip(given_date), quart_pct_chg_defence(given_date),
                      quart_pct_chg_housing_units_started(given_date), quart_pct_chg_imports(given_date),
                      sahms(given_date),
                      lag_gdp], axis = 1).dropna()
    compiled.columns = ['PCE', 'Govt_Constr',
                        'Biz_Inventory', 'Com_Loans',
                        'Exports', 'Capital_Goods',
                        'Biz_Equip', 'Defence',
                        'Housing_Start', 'Import',
                        'SAHM',
                        'Lag_GDP']
    #diff from midas due to aggregation of data
    df = df[df.index>="1993-01-01"]
    print("Bridge Data Loaded") 
    with open(file, 'wb') as f:
        pickle.dump((compiled, df), f)
    return compiled, df

def load_data_bridge_nohouse(given_date = "2020-01-01"):
    file = f'Components/test_data_bridge_nohouse/data_iteration_{given_date}.pkl'
    if os.path.exists(file):
        with open(file, 'rb') as f:
            return pickle.load(f)        
    fred = Fred(api_key = os.getenv("API_KEY"))
    df = get_most_recent_series_of_date("GDP", given_date, fred)
    df = pct_chg(df)
    df = df.pct_chg
    if df.index.max() < pd.to_datetime(given_date) - pd.offsets.QuarterBegin(2):
        model = AutoReg(df, lags = 4, trend = 'ct').fit()
        pred = model.predict(start = len(df), end = len(df))
        quarter_end = pd.to_datetime(given_date) - pd.offsets.QuarterEnd(1)
        new_dates = pd.date_range(start = df.index.max() + pd.offsets.MonthBegin(1), end = quarter_end, freq='QS')
        new_rows = pd.Series(pred, index=new_dates)
        df = pd.concat([df, new_rows])
    lag_gdp = df.copy()
    lag_gdp.index = lag_gdp.index + pd.DateOffset(months = 3)
    compiled = pd.concat([quart_pct_chg_pce(given_date), quart_pct_chg_govt_constr(given_date),
                      quart_pct_chg_business_inventories(given_date), quart_pct_chg_comm_loans(given_date),
                      quart_pct_chg_exports(given_date), quart_pct_cap(given_date),
                      quart_pct_chg_biz_equip(given_date), quart_pct_chg_defence(given_date),
                      quart_pct_chg_imports(given_date),
                      sahms(given_date),
                      lag_gdp], axis = 1).dropna()
    compiled.columns = ['PCE', 'Govt_Constr',
                        'Biz_Inventory', 'Com_Loans',
                        'Exports', 'Capital_Goods',
                        'Biz_Equip', 'Defence',
                        'Import',
                        'SAHM',
                        'Lag_GDP']
    #diff from midas due to aggregation of data
    df = df[df.index>="1993-01-01"]
    print("Bridge Data Loaded") 
    return compiled, df

def load_data_rf_aggregated(given_date = "2020-01-01"):
    X, y = load_data_bridge(given_date) 
    print("RF agg data Loaded")   
    return X, y 

def load_data_rf_monthly(given_date = "2020-01-01"):
    X, y = load_data_midas(given_date) 
    print("RF monthly data Loaded")   
    return X, y 

def load_data_midas(given_date = "2020-01-01"):
    root_dir = os.path.abspath(os.getcwd())    
    file = os.path.join(root_dir, "Components", "test_data_midas", f"data_iteration_{given_date}.pkl")
    # file = f'Components/test_data_midas/data_iteration_{given_date}.pkl'
    if os.path.exists(file):
        with open(file, 'rb') as f:
            print("MIDAS Data Loaded") 
            return pickle.load(f)   
    fred = Fred(api_key = os.getenv("API_KEY"))
    df = get_most_recent_series_of_date("GDP", given_date, fred)
    df = pct_chg(df)
    df = df.pct_chg
    if df.index.max() < pd.to_datetime(given_date) - pd.offsets.QuarterBegin(2):
        model = AutoReg(df, lags = 4, trend = 'ct').fit()
        pred = model.predict(start = len(df), end = len(df))
        quarter_end = pd.to_datetime(given_date) - pd.offsets.QuarterEnd(1)
        new_dates = pd.date_range(start = df.index.max() + pd.offsets.MonthBegin(1), end = quarter_end, freq='QS')
        new_rows = pd.Series(pred, index=new_dates)
        df = pd.concat([df, new_rows])
    lag_gdp = df.copy()
    lag_gdp.index = lag_gdp.index + pd.DateOffset(months = 3)
    compiled = pd.concat([quart_pct_chg_pce(given_date, 'M'), quart_pct_chg_govt_constr(given_date, 'M'),
                      quart_pct_chg_business_inventories(given_date, 'M'), quart_pct_chg_comm_loans(given_date, 'M'),
                      quart_pct_chg_exports(given_date, 'M'), quart_pct_cap(given_date, 'M'),
                      quart_pct_chg_biz_equip(given_date, 'M'), sahms(given_date, 'M'),
                      quart_pct_chg_housing_units_started(given_date, 'M'), quart_pct_chg_imports(given_date, 'M')], axis = 1).dropna()
    compiled.columns = ['PCE', 'Govt_Constr',
                        'Biz_Inventory', 'Com_Loans',
                        'Exports', 'Capital_Goods',
                        'Biz_Equip', 'SAHM',
                        'Housing_Start', 'Import']
    df_q = compiled.groupby(pd.Grouper(freq='Q')).apply(lambda x: x.values.flatten())
    df_q = pd.DataFrame(df_q.tolist(), index=df_q.index)
    cols = []
    for i in range(1, 4):
        for col in compiled.columns:
            cols.append(f"{col}_m{i}")
    df_q.columns = cols
    df_q = df_q.sort_index(axis = 1)
    df_q.index = df_q.index.to_period('Q').to_timestamp(how='start')
    compiled = pd.concat([df_q, quart_pct_chg_defence(given_date), lag_gdp], axis = 1).dropna()
    compiled.columns.values[-2:] = ['Defence', 'Lag_GDP']
    df = df[df.index>="1993-04-01"]
    print("MIDAS data Loaded")  
    with open(file, 'wb') as f:
        pickle.dump((compiled, df), f)
    return compiled, df

def load_data_midas_nohouse(given_date = "2020-01-01"):
    file = f'Components/test_data_midas/data_iteration_{given_date}.pkl'
    if os.path.exists(file):
        with open(file, 'rb') as f:
            return pickle.load(f)   
    fred = Fred(api_key = os.getenv("API_KEY"))
    df = get_most_recent_series_of_date("GDP", given_date, fred)
    df = pct_chg(df)
    df = df.pct_chg
    if df.index.max() < pd.to_datetime(given_date) - pd.offsets.QuarterBegin(2):
        model = AutoReg(df, lags = 4, trend = 'ct').fit()
        pred = model.predict(start = len(df), end = len(df))
        quarter_end = pd.to_datetime(given_date) - pd.offsets.QuarterEnd(1)
        new_dates = pd.date_range(start = df.index.max() + pd.offsets.MonthBegin(1), end = quarter_end, freq='QS')
        new_rows = pd.Series(pred, index=new_dates)
        df = pd.concat([df, new_rows])
    lag_gdp = df.copy()
    lag_gdp.index = lag_gdp.index + pd.DateOffset(months = 3)
    compiled = pd.concat([quart_pct_chg_pce(given_date, 'M'), quart_pct_chg_govt_constr(given_date, 'M'),
                      quart_pct_chg_business_inventories(given_date, 'M'), quart_pct_chg_comm_loans(given_date, 'M'),
                      quart_pct_chg_exports(given_date, 'M'), quart_pct_cap(given_date, 'M'),
                      quart_pct_chg_biz_equip(given_date, 'M'), sahms(given_date, 'M'),
                      quart_pct_chg_imports(given_date, 'M')], axis = 1).dropna()
    compiled.columns = ['PCE', 'Govt_Constr',
                        'Biz_Inventory', 'Com_Loans',
                        'Exports', 'Capital_Goods',
                        'Biz_Equip', 'SAHM',
                        'Import']
    df_q = compiled.groupby(pd.Grouper(freq='Q')).apply(lambda x: x.values.flatten())
    df_q = pd.DataFrame(df_q.tolist(), index=df_q.index)
    cols = []
    for i in range(1, 4):
        for col in compiled.columns:
            cols.append(f"{col}_m{i}")
    df_q.columns = cols
    df_q = df_q.sort_index(axis = 1)
    df_q.index = df_q.index.to_period('Q').to_timestamp(how='start')
    compiled = pd.concat([df_q, quart_pct_chg_defence(given_date), lag_gdp], axis = 1).dropna()
    compiled.columns.values[-2:] = ['Defence', 'Lag_GDP']
    df = df[df.index>="1993-04-01"]
    print("MIDAS data Loaded")  
    return compiled, df
