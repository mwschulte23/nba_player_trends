import pandas as pd
import numpy as np
import plotly.graph_objects as go

from nba_api.stats.endpoints import playergamelog


class PlayerStats:
    def __init__(self, player_id, season):
        self.player = player_id
        self.season = season

    def pull_data(self):
        data = playergamelog.PlayerGameLog(self.player, season=self.season)

        player_df = pd.DataFrame(data.get_normalized_dict()['PlayerGameLog'])
        player_df['GAME_DATE'] = pd.to_datetime(player_df['GAME_DATE'])
        player_df.sort_values(by='GAME_DATE', ascending=True, inplace=True)
        player_df.drop('VIDEO_AVAILABLE', axis=1, inplace=True)

        return player_df

    def create_trends(self, stat, ma1=20, ma2=5):
        df = self.pull_data()

        layout = go.Layout(title=f'{stat} Trends',
                           template='plotly_white'
                           )

        fig = go.Figure(layout=layout)

        fig.add_trace(go.Scatter(x=np.arange(df.shape[0]),
                                 y=df[stat].rolling(ma1).mean(),
                                 mode='lines',
                                 line={'color': 'red', 'dash': 'dash'},
                                 name=f'{ma1} Moving Avg'
                                 )
                      )
        fig.add_trace(go.Scatter(x=np.arange(df.shape[0]),
                                 y=df[stat].rolling(ma2).mean(),
                                 mode='lines',
                                 line={'color': 'blue'},
                                 name=f'{ma2} Moving Avg'
                                 )
                      )

        return fig
