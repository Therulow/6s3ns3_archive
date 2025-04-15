from data_load import *

given_date = "2020-03-01"

fred = Fred(api_key = os.getenv("API_KEY"))

df = get_most_recent_series_of_date("GDP", given_date, fred)
df = pct_chg(df)

df = df.pct_chg

_, test = train_test_split(df, test_size=50, shuffle=False)

# #use this date instead for cv
# given_date = "2007-09-01"

# # 30 chosen due to insufficient data
# test, _ = train_test_split(test, train_size=30, shuffle=False)
# pred = np.zeros((20, 30))

# for index in range(1, 31):
#     date = pd.to_datetime(given_date)
#     new_date = date - pd.DateOffset(months=3*index)
#     new_date_str = new_date.strftime('%Y-%m-%d')
#     with open(f'Components/test_data_midas/data_iteration_{new_date_str}.pkl', 'rb') as f:
#         X_train, y_train = pickle.load(f)
#     X_train = X_train.iloc[:-1, :]
#     X_validate = X_train.iloc[-1, :].values.reshape(1, -1) 
#     for trees in range(200, 400, 10):
#         regressor = RandomForestRegressor(n_estimators=trees, n_jobs=-1)
#         regressor.fit(X_train, y_train)
#         prediction = regressor.predict(X_validate)
#         pred[int(trees/10-20)][index-1] = prediction
#     print(f"Iteration {index}")
# rmse = []
# for row in pred:
#     reverse = row[::-1]
#     reverse = pd.Series(reverse, index = test.index)
#     rmse.append(mean_squared_error(reverse, test, squared=False))
# print(pred)
# plt.plot(rmse)
# plt.show()

# Tried values from 100 to 2000 in multiple of 100, then 200 to 400 in multiple of 10

# Evaluation on test set
pred = []
for index in range(1, 51):
    date = pd.to_datetime(given_date)
    new_date = date - pd.DateOffset(months=3*index)
    new_date_str = new_date.strftime('%Y-%m-%d')
    with open(f'Components/test_data_midas/data_iteration_{new_date_str}.pkl', 'rb') as f:
        X_train, y_train = pickle.load(f)
    X_train = X_train.iloc[:-1, :]
    X_validate = X_train.iloc[-1, :].values.reshape(1, -1) 
    regressor = RandomForestRegressor(n_estimators=300, n_jobs=4)
    regressor.fit(X_train, y_train)
    prediction = regressor.predict(X_validate)[0]
    pred.append(prediction)
    print(f"Iteration {index}")

pred.reverse()
pred = pd.Series(pred, index = test.index)

#evaluation
eval(pred, test)

# pred.to_csv('Components/Predictions/rf_midas.csv')
