from package_imports import *


test = pd.read_csv('Components/Predictions/test.csv', index_col=0)
pred1 = pd.read_csv('Components/Predictions/rf_midas.csv', index_col=0)
pred2 = pd.read_csv('Components/Predictions/benchmark1.csv', index_col=0)
stat, p, se, mean = dm_test(test, pred1, pred2)
print(f"DM stat: {stat}")
print(f"p-value: {p}")
print(f"HAC SE: {se}")
print(f"Mean Loss Differential: {mean}")