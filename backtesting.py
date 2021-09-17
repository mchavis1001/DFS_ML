from Optimizer.lineup_optimizer import optimizer
from Data.data import dfs_20_21
from Data.clean_data import combine
import pandas as pd

pd.set_option('display.max_columns', 2000)
pd.set_option('display.width', 1000)

dates = dfs_20_21.Date.unique()

lineups = []
d = []
try:
    for date in dates:
        standard_19_20 = pd.read_csv("Data/Resources/19-20 Standard.csv")
        dfs_20_21 = pd.read_csv("Data/Resources/20-21 DFS.csv")
        forward_19_20 = pd.read_csv('Data/Resources/19-20 Opp Defense-Forward.csv')
        center_19_20 = pd.read_csv('Data/Resources/19-20 Opp Defense-Center.csv')
        guard_19_20 = pd.read_csv('Data/Resources/19-20 Opp Defense-Guard.csv')
        testing = dfs_20_21[(dfs_20_21['Date'] == date)]
        test_combined = combine(standard_19_20, testing, forward_19_20, guard_19_20, center_19_20)

        d.append(date)
        lineups.append(optimizer(test_combined, testing).values.flatten().tolist())
except Exception as error:
    print(error)

cols = ['C', 'F', 'G', 'PF', 'PG', 'SF', 'SG', 'Util', 'Predicted', 'Actual', 'Salary']
total = pd.DataFrame(lineups, columns=cols)
total['Date'] = d[:len(lineups)]
results = pd.read_csv('Web_Scraping/resultsDB.csv')
df = pd.merge(total, results, on='Date', how='left').dropna()

for index, row in df.iterrows():
    if float(row['Actual']) > float(row['Cash Lines']):
        df.loc[index, 'Win/Loss'] = 1
    else:
        df.loc[index, 'Win/Loss'] = 0

print(df)
print(f"Win Percentage: {(df['Win/Loss'].value_counts()[1]/len(df['Win/Loss']))*100}")
