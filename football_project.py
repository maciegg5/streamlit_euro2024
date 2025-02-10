import streamlit as st
import pandas as pd
from statsbombpy import sb
from mplsoccer import VerticalPitch

st.title("Euros 2024 Shot Map")
st.subheader("Filter to any team/player to see all of their shots taken!")

df = pd.read_csv('euro_2024.csv')

team = st.selectbox(
    'Select a team', df['team'].sort_values().unique(), index=None)
player = st.selectbox('Select a player', df[df['team'] == team]['player'].dropna(
).sort_values().unique(), index=None)


def filetered_data(df, team, player):
    if team:
        df = df[df['team'] == team]
    if player:
        df = df[df['player'] == player]
    return df


filter_df = filetered_data(df, team, player)

pitch = VerticalPitch(pitch_type='statsbomb', half=True)

fig, ax = pitch.draw(figsize=(10,10))

def plot_shots(df, ax, pitch):
    for x in df.to_dict(orient='records'):
        pitch.scatter(
            x = x['x'],
            y = x['y'],
            ax = ax,
            s = 1000*x['shot_statsbomb_xg'],
            color = 'green' if x['shot_outcome'] == "Goal" else 'white',
            edgecolors='black',
            alpha = 1 if x['type'] == "goal" else .5,
            zorder = 2 if x['type'] == "goal" else 1
        )

plot_shots(filter_df, ax, pitch)

st.pyplot(fig)