import pandas as pd
from pulp import *

from Model.load_model import load_model


def optimizer(test_df, testing):
    players = load_model(test_df)
    g = players[players.Pos.isin(['PG', 'SG'])].copy()
    g.Pos = 'G'
    f = players[players.Pos.isin(['PF', 'SF'])].copy()
    f.Pos = 'F'
    util = players[players.Pos.isin(['PF', 'SF', 'SG', 'PG', 'C'])].copy()
    util.Pos = 'Util'
    players = pd.concat([players, g, f, util])

    availables = players.groupby(["Pos", "Player ID", "predicted", "Draftkings Salary", 'Opponent']).agg(
        'count')  # Switch opp to team
    availables = availables.reset_index()

    salaries = {}
    points = {}

    for pos in availables.Pos.unique():
        available_pos = availables[availables.Pos == pos]
        salary = list(available_pos[['Player ID', 'Draftkings Salary']].set_index("Player ID").to_dict().values())[0]
        point = list(available_pos[['Player ID', 'predicted']].set_index("Player ID").to_dict().values())[0]

        salaries[pos] = salary
        points[pos] = point

    pos_num_available = {
        "PG": 1,
        "SG": 1,
        "SF": 1,
        "PF": 1,
        "C": 1,
        "G": 1,
        "F": 1,
        "Util": 1
    }

    salary_cap = 50000
    data = []
    for lineup in range(1, 2):
        _vars = {k: LpVariable.dict(k, v, cat='Binary') for k, v in points.items()}

        prob = LpProblem("Fantasy", LpMaximize)
        rewards = []
        costs = []

        for x in _vars['PG']:
            prob += lpSum([_vars['PG'][x], _vars['G'][x], _vars['Util'][x]]) <= 1
        for x in _vars['SG']:
            prob += lpSum([_vars['SG'][x], _vars['G'][x], _vars['Util'][x]]) <= 1
        for x in _vars['PF']:
            prob += lpSum([_vars['PF'][x], _vars['F'][x], _vars['Util'][x]]) <= 1
        for x in _vars['SF']:
            prob += lpSum([_vars['SF'][x], _vars['F'][x], _vars['Util'][x]]) <= 1
        for x in _vars['C']:
            prob += lpSum([_vars['C'][x], _vars['Util'][x]]) <= 1

        for k, v in _vars.items():
            costs += lpSum([salaries[k][i] * _vars[k][i] for i in v])
            rewards += lpSum([points[k][i] * _vars[k][i] for i in v])
            prob += lpSum([_vars[k][i] for i in v]) == pos_num_available[k]

        prob += lpSum(rewards)
        prob += lpSum(costs) <= salary_cap

        if not lineup == 1:
            prob += (lpSum(rewards) <= total_score - 0.01)

        prob.solve()
        a = []
        score = str(prob.objective)
        for v in prob.variables():
            score = score.replace(v.name, str(v.varValue))
            if v.varValue != 0:
                a.append(v.name)
        new_score = re.sub('[PS]', '', score)
        total_score = eval(new_score)
        a.append(total_score)
        data.append(a)
    pos_columns = ['C', 'F', 'G', 'PF', 'PG', 'SF', 'SG', 'Util', 'Predicted']
    df = pd.DataFrame(data, columns=pos_columns)
    final = df
    pos = ['C', 'F', 'G', 'PF', 'PG', 'SF', 'SG', 'Util']
    actual_fp = []
    total_salary = []
    for p in pos:
        final[p] = final[p].str.extract('(\d+)', expand=False)
        actual_scored = testing.loc[testing['Player ID'] == int(final[p].values[0]), 'Draftkings Fantasy Points Scored']
        salary_today = testing.loc[testing['Player ID'] == int(final[p].values[0]), 'Draftkings Salary']
        final[p] = actual_scored.index.item()
        actual_fp.append(actual_scored.item())
        total_salary.append(salary_today.item())
    final['Actual'] = sum(actual_fp)
    final['Total Salary'] = sum(total_salary)

    return final
