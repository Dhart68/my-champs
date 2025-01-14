### Function do get info an NBA player

import pandas as pd

from datetime import datetime, timezone
from dateutil import parser

from nba_api.stats.endpoints import commonplayerinfo
from nba_api.live.nba.endpoints import scoreboard
from nba_api.live.nba.endpoints import boxscore

def player_day_stats(player_picked = 'victor wembanyama'):

    # Get info about the player
    player_id = players.find_players_by_full_name(player_picked)[0]['id']
    player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
    player_team_name = player_info.get_data_frames()[0]['TEAM_NAME'][0]
    player_family_name = player_info.get_data_frames()[0]['LAST_NAME'][0]

    # Get today scoreboard
    f = "{gameId}: {awayTeam} vs. {homeTeam} @ {gameTimeLTZ}"
    board = scoreboard.ScoreBoard()
    #print("ScoreBoardDate: " + board.score_board_date)
    games = board.games.get_dict()
    for game in games:
        gameTimeLTZ = parser.parse(game["gameTimeUTC"]).replace(tzinfo=timezone.utc).astimezone(tz=None)
        #print(f.format(gameId=game['gameId'], awayTeam=game['awayTeam']['teamName'], homeTeam=game['homeTeam']['teamName'], gameTimeLTZ=gameTimeLTZ))


    # Check if the team of the player picked played today and get the game_id
    for game in games:
        if player_team_name.lower() in game['awayTeam']['teamName'].lower():
            print(f"Found {player_team_name} game! They played away! gameId: {game['gameId']}")
            game_id = game['gameId']
            game_location = 'away'
        if player_team_name.lower() in game['homeTeam']['teamName'].lower():
            print(f"Found {player_team_name} game! They played home! gameId: {game['gameId']}")
            game_id = game['gameId']
            game_location = 'home'
        if game_id is None:
            return print(f'No {player_team_name} found today')


    # Getting Box Scores of the team for this game
    box = boxscore.BoxScore(game_id)

    if game_location == 'away':
        players = box.away_team.get_dict()['players']
    if game_location == 'home':
        players = box.home_team.get_dict()['players']

    # Display Team boxscore
    #f = "{player_id}: {name}: {points} PTS"
    #for player in players:
    #    print(f.format(player_id=player['personId'],name=player['name'],points=player['statistics']['points']))

    # build the team dataframe
    players_df = pd.DataFrame(players)

    # build the dataframe of the picked player
    player_df = pd.DataFrame(players_df[players_df['personId']==player_id]['statistics'].to_list())

    # select the columns
    player_df_selection = player_df[['minutes','points','twoPointersPercentage', 'threePointersAttempted','threePointersPercentage','reboundsDefensive', 'reboundsOffensive','assists','steals','blocks','blocksReceived','turnovers','foulsPersonal']]
    player_df_selection['familyName'] = player_family_name

    # Rename and reorder the columns
    player_df_selection = player_df_selection[['familyName','minutes','points','twoPointersPercentage','threePointersAttempted','threePointersPercentage','reboundsDefensive', 'reboundsOffensive','assists','steals','blocks','blocksReceived','turnovers','foulsPersonal']]
    player_df_selection = player_df_selection.rename(columns={
        'minutes': 'MIN',
        'points': 'PTS',
        'twoPointersPercentage': '2P%',
        'threePointersAttempted': '3PA',
        'threePointersPercentage': '3P%',
        'reboundsDefensive': 'DRB',
        'reboundsOffensive': 'ORB',
        'assists': 'AST',
        'steals': 'STL',
        'blocks': 'BLK',
        'blocksReceived': 'BLKED',
        'turnovers': 'TOV',
        'foulsPersonal': 'PF'
    })

    return player_df_selection
