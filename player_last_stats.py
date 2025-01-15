### Function do get info an NBA player

from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog

def player_last_stats(player_picked = 'victor wembanyama'):

    # Get info about the player
    player_id = players.find_players_by_full_name(player_picked)[0]['id']

    #Get the player's game logs for the current season
    game_log = playergamelog.PlayerGameLog(player_id=player_id)  # Adjust the season if needed
    games_data = game_log.get_data_frames()[0]  # Retrieve the DataFrame
    last_game_id = games_data.iloc[0]['Game_ID']

    # Reorder the columns
    last_3_games = games_data[['GAME_DATE', 'MATCHUP', 'MIN','PTS', 'REB',
                               'AST', 'STL', 'BLK', 'FGA', 'FG_PCT', 'FG3A',
                               'FG3_PCT', 'FTA','FT_PCT', 'OREB', 'DREB', 'TOV', 'PF', 'PLUS_MINUS']].head(3)

    # last_game_location
    if '@' in last_3_games.iloc[0]['MATCHUP']: last_game_location = "away"
    if 'vs' in last_3_games.iloc[0]['MATCHUP']: last_game_location = "home"

    return [last_3_games, player_id, last_game_id, last_game_location]
