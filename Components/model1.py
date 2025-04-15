from data_load import *

given_date = "2020-03-01"

fred = Fred(api_key = os.getenv("API_KEY"))

df = get_most_recent_series_of_date("GDP", given_date, fred)
df = pct_chg(df)

df = df.pct_chg
print(df)

_, test = train_test_split(df, test_size=50, shuffle=False)

X, y = load_data_bridge(given_date=given_date)
# X, _, y, _ = train_test_split(X.iloc[:-1, :], y, test_size=50, shuffle=False)

# vif_data = pd.DataFrame()
# vif_data["Feature"] = X.columns
# vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
# print(vif_data)
# # suggest to remove housing start

# # Even though govt construction is not correlated w GDP, when adding model performance is better and condition number is similar so include
# combined = pd.concat([X, y], axis = 1)
# corr_matrix = combined.corr()
# sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
# plt.show()

# condition_number = np.linalg.cond(X.values)
# print(f"Condition number: {condition_number}")

# Evaluation on test set
pred = []
for index in range(1, 51):
    date = pd.to_datetime(given_date)
    new_date = date - pd.DateOffset(months=3*index)
    new_date_str = new_date.strftime('%Y-%m-%d')
    with open(f'Components/test_data_bridge/data_iteration_{new_date_str}.pkl', 'rb') as f:
        X_train, y_train = pickle.load(f)
    # X_train = X_train.drop("SAHM", axis = 1)
    X_train = sm.add_constant(X_train)    
    X_test = X_train.iloc[-1, :]
    X_train = X_train.iloc[:-1, :]
    model = sm.OLS(y_train, X_train).fit()
    pred.append(model.predict(X_test)[0])
    print(f"Iteration {index}")

pred.reverse()

pred = pd.Series(pred, index = test.index)

#evaluation
eval(pred, test)

# pred.to_csv('Components/Predictions/model1.csv')


# model = sm.OLS(y, X.iloc[:-1, :]).fit()
# print(model.summary())
# print(model.predict(X.iloc[:-1, :])[0])
# residuals = model.resid
# print(X.iloc[:-1, :].apply(lambda x: x.corr(residuals)))

