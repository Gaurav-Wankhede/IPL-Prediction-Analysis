import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

# Hide the sidebar
st.set_page_config(layout="centered")

# Load the data from SQLite
def load_data(table_name):
    conn = sqlite3.connect("./database/IPL_Prediction_Analysis.db")
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df

# Load the tables
batting_df = load_data("Batting")
bowling_df = load_data("Bowling")
match_data_df = load_data("Match_Data")
mvp_data_df = load_data("MVP_Data")
overs_data_df = load_data("Overs_Data")
stats_data_df = load_data("Stats_Data")

# Combine the data from different tables
players_df = pd.concat([batting_df[["Player_name"]],
                         bowling_df[["Player_name"]],
                         mvp_data_df[["Player_name"]]]
                        )

players_df = players_df.drop_duplicates().reset_index(drop=True)

# Create a filter for players
player_filter = st.multiselect("Select players", players_df["Player_name"].unique())

# Create a dropdown for years
years_df = match_data_df[["Start_Date"]]
years_df["Start_Date"] = pd.to_datetime(years_df["Start_Date"], format="%d-%B-%Y")

years_df["Year"] = years_df["Start_Date"].dt.year
year_filter = st.selectbox("Select year", years_df["Year"].unique())

# Filter the data based on player and year
filtered_batting_df = batting_df[batting_df["Player_name"].isin(player_filter) &
                                   pd.to_datetime(batting_df["Start_Date"], format="%d-%B-%Y").dt.year == year_filter]

filtered_bowling_df = bowling_df[bowling_df["Player_name"].isin(player_filter) &
                                   pd.to_datetime(bowling_df["Start_Date"], format="%d-%B-%Y").dt.year == year_filter]

filtered_mvp_data_df = mvp_data_df[mvp_data_df["Player_name"].isin(player_filter) &
                                     pd.to_datetime(mvp_data_df["Start_Date"], format="%d-%B-%Y").dt.year == year_filter]


# Create the analysis
st.header("Batting Analysis")
st.write(filtered_batting_df)

st.header("Bowling Analysis")
st.write(filtered_bowling_df)

st.header("MVP Analysis")
st.write(filtered_mvp_data_df)
