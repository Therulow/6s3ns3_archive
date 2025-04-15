from data_load import *

given_date = "2020-03-01"

fred = Fred(api_key = os.getenv("API_KEY"))

df = get_most_recent_series_of_date("GDP", given_date, fred)
df = pct_chg(df)

df = df.pct_chg

_, test = train_test_split(df, test_size=50, shuffle=False)

# X, y = load_data_midas(given_date=given_date)

# vif_data = pd.DataFrame()
# vif_data["Feature"] = X.columns
# vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
# print(vif_data)

# # Even though govt construction is not correlated w GDP, when adding model performance is better and condition number is similar so include
# combined = pd.concat([X, y], axis = 1)
# corr_matrix = combined.corr()
# sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
# plt.show()

# condition_number = np.linalg.cond(X.values)
# print(f"Condition number: {condition_number}")

# # use this date instead for cv
# given_date = "2007-09-01"

# # 30 chosen due to insufficient data
# test, _ = train_test_split(test, train_size=30, shuffle=False)

# rmse = []
# for alpha in [0.0001, 0.001, 0.01, 0.1]:
#     for l1_ratio in [0.1, 0.25, 0.5, 0.75, .9]:
#         pred = []
#         for index in range(1, 31):
#             date = pd.to_datetime(given_date)
#             new_date = date - pd.DateOffset(months=3*index)
#             new_date_str = new_date.strftime('%Y-%m-%d')
#             with open(f'Components/test_data_midas/data_iteration_{new_date_str}.pkl', 'rb') as f:
#                 X_train, y_train = pickle.load(f)        
#             X_train = sm.add_constant(X_train)    
#             X_test = X_train.iloc[-1, :]
#             X_train = X_train.iloc[:-1, :]
#             model = sm.OLS(y_train, X_train).fit_regularized(alpha=alpha, L1_wt=l1_ratio)
#             pred.append(model.predict(X_test)[0])
#         rmse.append(mean_squared_error(pred, test, squared=False))
#         print(f'Alpha {alpha} L1_wt {l1_ratio} {mean_squared_error(pred, test, squared=False)}')
# rmse = np.array(rmse).reshape(4, 5)
# print(rmse)
# Best is alpha = .1, L1_wt = .9

# Evaluation on test set
pred = []
for index in range(1, 51):
    date = pd.to_datetime(given_date)
    new_date = date - pd.DateOffset(months=3*index)
    new_date_str = new_date.strftime('%Y-%m-%d')
    with open(f'Components/test_data_midas/data_iteration_{new_date_str}.pkl', 'rb') as f:
        X_train, y_train = pickle.load(f)
    X_train = sm.add_constant(X_train)    
    X_test = X_train.iloc[-1, :]
    X_train = X_train.iloc[:-1, :]
    model = sm.OLS(y_train, X_train).fit_regularized(alpha = .1, L1_wt=.9)
    pred.append(model.predict(X_test)[0])
    print(f"Iteration {index}")

pred.reverse()

pred = pd.Series(pred, index = test.index)

#evaluation
eval(pred, test)

# pred.to_csv('Components/Predictions/midas_EN.csv')

# model = ElasticNet(alpha=.1, l1_ratio=.9)
# model.fit(X.iloc[:-1, :], y)
# coef_df = pd.DataFrame({
#     "Feature": X.iloc[:-1, :].columns,  # Get feature names
#     "Coefficient": model.coef_   # Get coefficients
# })
# print(coef_df)
