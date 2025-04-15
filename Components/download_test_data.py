from package_imports import *
from data_load import *

given_date = "2025-04-01"

for index in range(1, 304):
    date = pd.to_datetime(given_date)
    new_date = date - pd.DateOffset(months=index)
    new_date_str = new_date.strftime('%Y-%m-%d')
    X_train, y_train = load_data_midas(new_date_str)

# for index in range(1, 51):
#     date = pd.to_datetime(given_date)
#     new_date = date - pd.DateOffset(months=3*index)
#     new_date_str = new_date.strftime('%Y-%m-%d')
#     X_train, y_train = load_data_bridge_nohouse(new_date_str)
#     with open(f'Components/test_data_bridge_nohouse/data_iteration_{new_date_str}.pkl', 'wb') as f:
#         pickle.dump((X_train, y_train), f)


# with open('Components/test_data_midas/data_iteration_2019-09-01.pkl', 'rb') as f:
#     df, series = pickle.load(f)
# print(df, series)

# with open('Components/test_data_midas_nohouse/data_iteration_2019-12-01.pkl', 'rb') as f:
#     df, series = pickle.load(f)
# print(df.columns)

# folder_path = 'Components/test_data_midas'
# new_path = 'Components/test_data_midas_nohouse'

# for filename in os.listdir(folder_path):
#     filepath = os.path.join(folder_path, filename)
#     with open(filepath, 'rb') as f:
#         df, series = pickle.load(f)
#         df = df.drop("Housing_Start_m1", axis = 1)
#         df = df.drop("Housing_Start_m2", axis = 1)
#         df = df.drop("Housing_Start_m3", axis = 1)
#     filepath = os.path.join(new_path, filename)
#     with open(filepath, 'wb') as f:
#         pickle.dump((df, series), f)