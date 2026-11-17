import numpy as np
import pandas as pd

# Load and clean beach volleyball data
path = 'volley.csv'
data = pd.read_csv(path, header=0)

data = data[data['gender'] == "W"]
data = data[data['circuit'] == 'FIVB']
data = data[(data['year'] >= 2007) & (data['year'] <= 2015)]

col_name = ['winner1_name', 'winner2_name', 'loser1_name', 'loser2_name']

# Split into Whole, Train (< 2015), and Test (>= 2015)
Whole = data[col_name]
Train = data[data['year'] < 2015][col_name]
Test = data[data['year'] >= 2015][col_name]

def get_players_and_teams(df):
    players = df[['winner1_name', 'winner2_name', 'loser1_name', 'loser2_name']].values.flatten().astype(str)
    w_teams = df['winner1_name'].astype(str) + ', ' + df['winner2_name'].astype(str)
    l_teams = df['loser1_name'].astype(str) + ', ' + df['loser2_name'].astype(str)
    teams = np.concatenate([w_teams.values, l_teams.values])
    return players, teams

playerAll, teamAll = get_players_and_teams(Whole)
playerTr, teamTr = get_players_and_teams(Train)
playerTe, teamTe = get_players_and_teams(Test)

# Unique counts
_, counts_p_all = np.unique(playerAll, return_counts=True)
_, counts_t_all = np.unique(teamAll, return_counts=True)

_, counts_p_tr = np.unique(playerTr, return_counts=True)
_, counts_t_tr = np.unique(teamTr, return_counts=True)

_, counts_p_te = np.unique(playerTe, return_counts=True)
_, counts_t_te = np.unique(teamTe, return_counts=True)

# Set differences (new in test compared to train)
new_teams_te = np.setdiff1d(teamTe, teamTr).shape[0]
new_players_te = np.setdiff1d(playerTe, playerTr).shape[0]

# Summary metrics
n_matches_all, n_matches_tr, n_matches_te = len(Whole), len(Train), len(Test)
n_teams_all, n_teams_once = len(counts_t_all), np.sum(counts_t_all == 1)
n_teams_tr, n_teams_te = len(counts_t_tr), len(counts_t_te)

n_players_all, n_players_once = len(counts_p_all), np.sum(counts_p_all == 1)
n_players_tr, n_players_te = len(counts_p_tr), len(counts_p_te)

# Print Table 2 format to terminal screen
print("\nTable 2: Data statistics (Beach volleyball)")
print("=" * 60)
print(f"{'':<18} {'whole (once)':<16} {'training':<12} {'test (new)':<12}")
print("-" * 60)
print(f"{'# matches':<18} {n_matches_all:<16,d} {n_matches_tr:<12d} {n_matches_te:<12d}")
print(f"{'# teams':<18} {f'{n_teams_all} ({n_teams_once})':<16} {n_teams_tr:<12d} {f'{n_teams_te} ({new_teams_te})':<12}")
print(f"{'# players':<18} {f'{n_players_all} ({n_players_once})':<16} {n_players_tr:<12d} {f'{n_players_te} ({new_players_te})':<12}")
print(f"{'team-to-player':<18} {n_teams_all}/{n_players_all} ≈ {n_teams_all/n_players_all:.2f}")
print(f"{'one-appear-team':<18} {n_teams_once}/{n_teams_all} ≈ {n_teams_once/n_teams_all:.2f}")
print("=" * 60)