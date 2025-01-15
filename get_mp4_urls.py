# Function to get the URL of the video of the player picked

import requests
import pandas as pd

from nba_api.stats.endpoints import playbyplayv2


def get_mp4_urls(player_id = '203999', game_id = '0022400559', game_location = 'away'):
    ### Function to get the URL of the video of the player picked, need the game_id and the player_id
    ### get the list of URLs of the video part of interest, could be improve with the EVENTMSGACTIONTYPE
    ### to select only some type of actions

    # get all the pbp of the game
    pbp = playbyplayv2.PlayByPlayV2(game_id)
    pbp = pbp.get_data_frames()[0]
    #pbp.shape

    # select rows in pbp_player containing Name of the player
    # I choose to select only the 2 players involved to limit the number of actions
    pbp_player = pbp[(pbp['PLAYER1_ID'] == int(player_id)) |
                     (pbp['PLAYER2_ID'] == int(player_id)) ]
    #pbp_player.shape

    # select video_event_pd where desc does not contain remove terms
    # list of sequences to avoid
    Remove_terms = ['REBOUND', 'MISS', 'Free Throw', 'FOUL']

    if game_location == 'away':
        pbp_player = pbp_player[(pbp_player['VISITORDESCRIPTION'].str.contains('|'.join(Remove_terms), na=False) == False) ]
    if game_location == 'home':
        pbp_player = pbp_player[(pbp_player['HOMEDESCRIPTION'].str.contains('|'.join(Remove_terms), na=False) == False) ]

    #pbp_player.shape

    # event num list with video flag
    event_id_list = pbp_player[pbp_player['VIDEO_AVAILABLE_FLAG']==1]['EVENTNUM'].tolist()

    # for loop to get all the video url

    headers = {
        'Host': 'stats.nba.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'x-nba-stats-origin': 'stats',
        'x-nba-stats-token': 'true',
        'Connection': 'keep-alive',
        'Referer': 'https://stats.nba.com/',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'
    }

    video_event_list = []

    for event_id in event_id_list:
        url = 'https://stats.nba.com/stats/videoeventsasset?GameEventID={}&GameID={}'.format(event_id, game_id)
        r = requests.get(url, headers=headers)
        json = r.json()
        video_urls = json['resultSets']['Meta']['videoUrls']
        playlist = json['resultSets']['playlist']
        video_event_list.append({'video': video_urls[0]['lurl'], 'desc': playlist[0]['dsc']})

    #print(video_event_list)

    video_event_df = pd.DataFrame(video_event_list)

    return video_event_df
