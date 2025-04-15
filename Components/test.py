from package_imports import *
from data_load import *

fred = Fred(api_key = os.getenv("API_KEY"))

given_date = "2020-03-01"

# date = pd.to_datetime(given_date)

# df = get_most_recent_series_of_date("GDP", given_date, fred)
# df = pct_chg(df)

# df = df.pct_chg

# _, test = train_test_split(df, test_size=50, shuffle=False)

# X, y = load_data_midas_nohouse(given_date=given_date)

# X, _, y, _ = train_test_split(X.iloc[:-1, :], y, test_size=50, shuffle=False)

# vif_data = pd.DataFrame()
# vif_data["Feature"] = X.columns
# vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
# print(vif_data)

# combined = pd.concat([X, y], axis = 1)
# corr_matrix = combined.corr()
# sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
# plt.show()

# condition_number = np.linalg.cond(X.values)
# print(f"Condition number: {condition_number}")

# while True:
#     date = date - pd.offsets.MonthBegin(1)
#     df = get_most_recent_series_of_date("UNRATE", date, fred)
#     if df.empty:
#         print(date)
#         break
#     else: print(f'{date} OK')

# df = get_most_recent_series_of_date("IPBUSEQ", date, fred)
# print(df)
# X, y = load_data_midas(given_date=given_date)
# print(X.Import_m1)
# for i in X.values:
#     print(i)

# df = get_most_recent_series_of_date("BOPTIMP", "2010-05-01", fred)
# pct_chg_fed_defence = transform_series(df, 5).dropna()*100
# pct_chg_fed_defence = pct_chg_fed_defence[pct_chg_fed_defence.index<pd.to_datetime(given_date) - pd.offsets.MonthBegin(1)]
# print(pct_chg_fed_defence.tail(20))

# print(quart_pct_chg_biz_equip("2001-01-01", 'M').tail(30))
# print(load_data_midas(given_date))
# print(load_data_bridge(given_date))
# 2000-01-01
# 2000-03-01 
# 2019-10-01
# 2019-12-01

load_data_midas("2025-04-01")