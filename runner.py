import json
import streamlit as st

from src.get_data import PlayerStats

with open('src/player_info.json') as fp:
    players = json.load(fp)

st.header('Track Player Trends')

l, c, r = st.beta_columns(3)

with l:
    player_list = st.selectbox('Select Player', list(players.keys()))
with c:
    season_picker = st.selectbox('Select Season', ['2018-19', '2019-20', '2020-21'])
with r:
    stat_picker = st.selectbox('Pick Stat', ['PTS', 'REB', 'AST', 'STL', 'BLK', 'PLUS_MINUS'])

l, r = st.beta_columns(2)

with l:
    ma1_slider = st.slider('Moving Avg A', min_value=5, max_value=50, value=20)
with r:
    ma2_slider = st.slider('Moving Avg B', min_value=1, max_value=20, value=5)

ps = PlayerStats(players[player_list], season_picker)
fig = ps.create_trends(stat_picker, ma1_slider, ma2_slider)

st.plotly_chart(fig.to_dict())
