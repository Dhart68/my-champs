# Main program

import pandas as pd

from datetime import datetime, timezone
from dateutil import parser

from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.live.nba.endpoints import scoreboard
from nba_api.live.nba.endpoints import boxscore

from player_last_stats import player_last_stats
from get_mp4_urls import get_mp4_urls

# Prompt to choose a player
player_picked = input('Write the name of your favorit active nba player (Victor Wembanyama):')

# Function to get the stats of the day for the player
[last_3_games, player_id, last_game_id, last_game_location] = player_last_stats(player_picked) # give the stats of the day, the player_id and the game_id

# Display df of the day
print('Here are the stats of the last 3 games')
print(last_3_games)

# Function to get the stats of the day for the player
video_event_df = get_mp4_urls(player_id, last_game_id, last_game_location)

print('Here is the list of the best video of the last game')
print(video_event_df)
