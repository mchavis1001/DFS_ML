import pandas as pd


def clean_standard(df):
    columns_to_drop_standard = ['Rk', 'GS', 'MP', 'FG', 'FG%', 'FGA', '3PA', '2PA', 'FT', 'FTA', 'PTS', 'TOV', 'TRB',
                                'Tm', 'G▼']
    df.drop(columns=columns_to_drop_standard, inplace=True)
    df.set_index('Player', inplace=True)


def clean_dfs(df):
    columns_to_drop_dfs = ['Season', 'GAME ID', 'Minutes', 'Team', 'Days Rest', 'Date', 'GAME ID', 'Season',
                           'Minutes', 'Usage Rate', 'FANDUEL Position', 'Yahoo Position', 'Fanduel Salary',
                           'Yahoo Salary',
                           'Fanduel Fantasy Points Scored', 'Yahoo Points Scored']
    df.drop(columns=columns_to_drop_dfs, inplace=True)
    df.dropna(inplace=True)
    df.set_index('Player', inplace=True)


def format_teams_nba(df):
    df['Opponent'] = df.TEAM.str.rsplit(' ', 1).str[0]
    df['Opponent'].loc[df['Opponent'] == 'Portland Trail'] = 'Portland'
    df['Opponent'].loc[df['Opponent'] == 'LA'] = 'LA Clippers'
    df['Opponent'].loc[df['Opponent'] == 'Los Angeles'] = 'LA Lakers'
    df.drop(columns='TEAM', inplace=True)


def combine(standard, dfs, forward, guard, center):
    format_teams_nba(forward)
    format_teams_nba(center)
    format_teams_nba(guard)
    clean_standard(standard)
    clean_dfs(dfs)

    combined_dfs_std = pd.merge(dfs, standard, on='Player', how='left')

    guard_df = combined_dfs_std[(combined_dfs_std['Pos'] == 'SG') | (combined_dfs_std['Pos'] == 'PG')]
    forward_df = combined_dfs_std[(combined_dfs_std['Pos'] == 'SF') | (combined_dfs_std['Pos'] == 'PF')]
    center_df = combined_dfs_std[combined_dfs_std['Pos'] == 'C']
    guard_combined = pd.merge(guard_df, guard, on='Opponent', how='left')
    forward_combined = pd.merge(forward_df, forward, on='Opponent', how='left')
    center_combined = pd.merge(center_df, center, on='Opponent', how='left')

    combined = pd.concat([guard_combined, forward_combined, center_combined], join="inner")
    combined.drop(columns=['GP', 'W', 'L', 'MIN', 'DEF RTG', 'DREB'], inplace=True)

    return combined
