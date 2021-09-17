import pandas as pd
from Data.clean_data import combine

pd.set_option('display.max_columns', 2000)
pd.set_option('display.width', 1000)

standard_15_16 = pd.read_csv("Data/Resources/15-16 Standard.csv")
dfs_16_17 = pd.read_csv("Data/Resources/16-17 DFS.csv")
forward_15_16 = pd.read_csv('Data/Resources/15-16 Opp Defense-Forward.csv')
center_15_16 = pd.read_csv('Data/Resources/15-16 Opp Defense-Center.csv')
guard_15_16 = pd.read_csv('Data/Resources/15-16 Opp Defense-Guard.csv')

standard_16_17 = pd.read_csv("Data/Resources/16-17 Standard.csv")
dfs_17_18 = pd.read_csv("Data/Resources/17-18 DFS.csv")
forward_16_17 = pd.read_csv('Data/Resources/16-17 Opp Defense-Forward.csv')
center_16_17 = pd.read_csv('Data/Resources/16-17 Opp Defense-Center.csv')
guard_16_17 = pd.read_csv('Data/Resources/16-17 Opp Defense-Guard.csv')

standard_17_18 = pd.read_csv("Data/Resources/17-18 Standard.csv")
dfs_18_19 = pd.read_csv("Data/Resources/18-19 DFS.csv")
forward_17_18 = pd.read_csv('Data/Resources/17-18 Opp Defense-Forward.csv')
center_17_18 = pd.read_csv('Data/Resources/17-18 Opp Defense-Center.csv')
guard_17_18 = pd.read_csv('Data/Resources/17-18 Opp Defense-Guard.csv')

standard_18_19 = pd.read_csv("Data/Resources/18-19 Standard.csv")
dfs_19_20 = pd.read_csv("Data/Resources/19-20 DFS.csv")
forward_18_19 = pd.read_csv('Data/Resources/18-19 Opp Defense-Forward.csv')
center_18_19 = pd.read_csv('Data/Resources/18-19 Opp Defense-Center.csv')
guard_18_19 = pd.read_csv('Data/Resources/18-19 Opp Defense-Guard.csv')

standard_19_20 = pd.read_csv("Data/Resources/19-20 Standard.csv")
dfs_20_21 = pd.read_csv("Data/Resources/20-21 DFS.csv")
forward_19_20 = pd.read_csv('Data/Resources/19-20 Opp Defense-Forward.csv')
center_19_20 = pd.read_csv('Data/Resources/19-20 Opp Defense-Center.csv')
guard_19_20 = pd.read_csv('Data/Resources/19-20 Opp Defense-Guard.csv')

df = combine(standard_15_16, dfs_16_17, forward_15_16, guard_15_16, center_15_16)
df2 = combine(standard_16_17, dfs_17_18, forward_16_17, guard_16_17, center_16_17)
df3 = combine(standard_17_18, dfs_18_19, forward_17_18, guard_17_18, center_17_18)
df4 = combine(standard_18_19, dfs_19_20, forward_18_19, guard_18_19, center_18_19)
