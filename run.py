from Data.data import dfs_20_21, standard_19_20, forward_19_20, guard_19_20, center_19_20
from Data.clean_data import combine
import pandas as pd
from Optimizer.lineup_optimizer import optimizer

pd.set_option('display.max_columns', 2000)
pd.set_option('display.width', 1000)

date = '12/30/2020'

testing = dfs_20_21[(dfs_20_21['Date'] == date)]
test_combined = combine(standard_19_20, testing, forward_19_20, guard_19_20, center_19_20)

df = optimizer(test_combined, testing)
print(df)
