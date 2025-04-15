from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

given_date = "2020-03-01"

df = get_most_recent_series_of_date("GDP", given_date, fred)
df = pct_chg(df)

df = df.pct_chg

_, test = train_test_split(df, test_size=50, shuffle=False)

df.index = pd.to_datetime(df.index).to_period('Q')

print(df.shape)

pred = []

for index in range(1, 51):
    date = pd.to_datetime(given_date)
    new_date = date - pd.DateOffset(months=3*index)
    new_date_str = new_date.strftime('%Y-%m-%d')
    with open(f'Components/test_data_bridge/data_iteration_{new_date_str}.pkl', 'rb') as f:
        _, train = pickle.load(f)   
    train.index = pd.to_datetime(train.index).to_period('Q')
    model = AutoReg(train, lags = 4, trend = 'ct').fit()
    pred.append(model.predict(start = len(train), end = len(train)))

# print(model.params)

pred.reverse()
pred = pd.concat(pred)
pred.index = pred.index.to_timestamp()

eval(test, pred, plot=True)

# pred.to_csv('Components/Predictions/arft04.csv')