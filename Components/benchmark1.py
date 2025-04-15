from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

given_date = "2020-03-01"

df = get_most_recent_series_of_date("GDP", given_date, fred)
df = pct_chg(df)
# df.plot(y = "pct_chg")
# plt.show()

df = df.pct_chg
_, test = train_test_split(df, test_size=50, shuffle=False)

pred = []

for index in range(1, 51):
    date = pd.to_datetime(given_date)
    new_date = date - pd.DateOffset(months=3*index)
    new_date_str = new_date.strftime('%Y-%m-%d')
    with open(f'Components/test_data_bridge/data_iteration_{new_date_str}.pkl', 'rb') as f:
        _, y_train = pickle.load(f)    
    pred.append(y_train.iloc[:-index].mean())

pred.reverse()
pred = pd.Series(pred, index = test.index)

#evaluation
eval(pred, test, plot=True)

# pred.to_csv('Components/Predictions/benchmark1.csv')
# test.to_csv('Components/Predictions/test.csv')