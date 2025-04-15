from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

given_date = "2020-03-01"

df = get_most_recent_series_of_date("GDP", given_date, fred)
df = pct_chg(df)

df = df.pct_chg

_, test = train_test_split(df, test_size=50, shuffle=False)

pred = []

for index in range(1, 51):
    date = pd.to_datetime(given_date)
    new_date = date - pd.DateOffset(months=3*index)
    new_date_str = new_date.strftime('%Y-%m-%d')
    with open(f'Components/test_data_bridge/data_iteration_{new_date_str}.pkl', 'rb') as f:
        X_train, y_train = pickle.load(f)
    df = X_train.iloc[:-1, :].copy()
    df['y'] = y_train
    df.reset_index(inplace = True)
    df.rename(columns = {'index':'ds'}, inplace = True)
    model = Prophet()
    for col in X_train.columns:
        model.add_regressor(col)
    model.fit(df)
    future = model.make_future_dataframe(periods=1, freq='QS')
    future = future.merge(X_train, how = 'left', left_on='ds', right_index=True)
    forecast = model.predict(future).iloc[-1, :]
    array = forecast.iloc[[0,-1]]
    pred.append(array)

pred = pd.DataFrame(pred)
pred['ds'] = pd.to_datetime(pred['ds'])
pred = pred.set_index('ds')
pred.sort_index(inplace=True)
pred = pred.squeeze()

eval(test, pred, plot=False)

# pred.to_csv('Components/Predictions/Prophet.csv')

