import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

def find_thresholds(df):
    # Define thresholds for various statistics
    thresholds = {
        'ts_pct_threshold': df['ts_pct'].quantile(0.25),
        'pace_threshold': df['pace'].quantile(0.25),
        'def_rtg_threshold': df['def_rtg'].quantile(0.25),
        'ft_rate_threshold': df['ft_rate'].quantile(0.25),
        'tov_pct_threshold': df['tov_pct'].quantile(0.75),
        'fg3a_per_fga_pct_threshold': df['fg3a_per_fga_pct'].quantile(0.25),
        'fta_per_fga_pct_threshold': df['fta_per_fga_pct'].quantile(0.25),
        'ast_pct_threshold': df['ast_pct'].quantile(0.25),
        'trb_pct_threshold': df['trb_pct'].quantile(0.25),
        'off_rtg_threshold': df['off_rtg'].quantile(0.25),
        'stl_pct_threshold': df['stl_pct'].quantile(0.25),
        'efg_pct_threshold': df['efg_pct'].quantile(0.25)
    }
    
    return thresholds

def classify_games(df):
    thresholds = find_thresholds(df)
    for stat, threshold in thresholds.items():
        stat = stat.replace('_threshold', '')
        if stat == 'tov_pct':
            df[f'{stat}_weak'] = np.where(df[stat.split('_threshold')[0]] < threshold, 1, -1)
        else:
            df[f'{stat}_weak'] = np.where(df[stat.split('_threshold')[0]] < threshold, -1, 1)
    
    return df


def main():
    # Load data
    df_game = pd.read_csv('./game_stats.csv')

    # Store unique team IDs for later reference
    team_ids = df_game['team_id'].unique()

    # Drops unneeded columns for analysis
    df_game.drop(['game_location', 'date_game', 'game_result', 'game_season', 'x'], axis=1, inplace=True)


    # Creates labels for all games, if a team is weak in a certain stat (-1) if a team is strong in a certain stat (1)
    classify_games(df_game)

    print(df_game.head())
    print(df_game['tov_pct'])
    print(df_game['tov_pct_weak'])

    # Next steps would be to create a machine learning model either using neural networks or random forest for this data
    # Since we now have labeled data we can get multi outputs for understandinf whether a certain team is weak in stats
    # We can split the data up for training and testing for this, and then give the model just a certain team's games

if __name__ == "__main__":
    main()
