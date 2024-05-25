import streamlit as st
from streamlit_option_menu import option_menu

from Prev_Matches.Batting import batting
from Prev_Matches.toSQL.Batting_toSQL import BattingSQLProcessor
from Prev_Matches.Bowling import bowling
from Prev_Matches.toSQL.Bowling_toSQL import BowlingSQLProcessor
from Prev_Matches.Match_data import match_data
from Prev_Matches.toSQL.Match_Data_toSQL import MatchDataSQLProcessor
from Prev_Matches.MVP_Data import mvp_data
from Prev_Matches.toSQL.MVP_Data_toSQL import MVPDataSQLProcessor
from Prev_Matches.Overs import overs
from Prev_Matches.toSQL.Overs_toSQL import OversSQLProcessor
from Prev_Matches.Stats import stats
from Prev_Matches.toSQL.Stats_toSQL import StatsSQLProcessor

from Latest_Matches.Latest_Batting import latest_batting
from Latest_Matches.toSQL.Latest_Batting_toSQL import LatestBattingSQLProcessor
from Latest_Matches.Latest_Bowling import latest_bowling
from Latest_Matches.toSQL.Latest_Bowling_toSQL import LatestBowlingSQLProcessor
from Latest_Matches.Latest_Match_Data import latest_match_data
from Latest_Matches.toSQL.Latest_Match_Data_toSQL import LatestMatchDataSQLProcessor
from Latest_Matches.Latest_MVP_Data import latest_mvp_data
from Latest_Matches.toSQL.Latest_MVP_toSQL import LatestMVPDataSQLProcessor
from Latest_Matches.Latest_Overs import latest_overs
from Latest_Matches.toSQL.Latest_Overs_toSQL import LatestOversDataSQLProcessor
from Latest_Matches.Latest_Stats import latest_stats
from Latest_Matches.toSQL.Latest_Stats_toSQL import LatestStatsDataSQLProcessor

st.set_page_config(
    page_title="Cricket Match WebScrapping",
    page_icon="./images/web.png",
    layout='wide'
)

with open("styles/style.css", "r") as f:
    css_content = f.read()

# Display the CSS content in Streamlit
st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)


@st.cache_data
def process_batting():
    batting()


@st.cache_resource
def process_batting_sql():
    processor = BattingSQLProcessor()
    processor.run()


@st.cache_data
def process_bowling():
    bowling()


@st.cache_resource
def process_bowling_sql():
    processor = BowlingSQLProcessor()
    processor.run()


@st.cache_data
def process_match_data():
    match_data()


@st.cache_resource
def process_match_data_sql():
    processor = MatchDataSQLProcessor()
    processor.run()


@st.cache_data
def process_mvp_data():
    mvp_data()


@st.cache_resource
def process_mvp_data_sql():
    processor = MVPDataSQLProcessor()
    processor.run()


@st.cache_data
def process_overs():
    overs()


@st.cache_resource
def process_overs_sql():
    processor = OversSQLProcessor()
    processor.run()


@st.cache_data
def process_stats():
    stats()


@st.cache_resource
def process_stats_sql():
    processor = StatsSQLProcessor()
    processor.run()


@st.cache_data
def process_latest_batting():
    latest_batting()


@st.cache_resource
def process_latest_batting_sql():
    processor = LatestBattingSQLProcessor()
    processor.run()


@st.cache_data
def process_latest_bowling():
    latest_bowling()


@st.cache_resource
def process_latest_bowling_sql():
    processor = LatestBowlingSQLProcessor()
    processor.run()


@st.cache_data
def process_latest_match_data():
    latest_match_data()


@st.cache_resource
def process_latest_match_data_sql():
    processor = LatestMatchDataSQLProcessor()
    processor.run()


@st.cache_data
def process_latest_mvp_data():
    latest_mvp_data()


@st.cache_resource
def process_latest_mvp_sql():
    processor = LatestMVPDataSQLProcessor()
    processor.run()


@st.cache_data
def process_latest_overs():
    latest_overs()


@st.cache_resource
def process_latest_overs_sql():
    processor = LatestOversDataSQLProcessor()
    processor.run()


@st.cache_data
def process_latest_stats():
    latest_stats()


@st.cache_resource
def process_latest_stats_sql():
    processor = LatestStatsDataSQLProcessor()
    processor.run()


def main():
    st.title("Cricket Match WebScrapping")
    st.header("Welcome to the WebScrapping App!")
    st.write("This app provides a scrapping tool for cricket matches.")

    st.markdown("---")

    selected = option_menu(
        menu_title="Web Scrapping",
        options=["Batting", "Bowling", "Match", "MVP", "Overs", "Stats"],
        icons=["bootstrap-fill", "0-circle", "table", "trophy", "speedometer", "bar-chart"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "black", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "Goldenrod",
                "color": "white",
                "::first-letter": {"color": "Goldenrod"}
            },
            "nav-link-selected": {
                "background-color": "Goldenrod",
                "color": "white",
                "font-weight": "bold"
            }
        }
    )

    if selected == "Batting":
        st.write("#### Batting Web Scraping")

        # Show button to run batting()
        if st.button("CSV"):
            st.write("Processing Batting CSV data...")
            batting()
            st.write("Batting CSV data processing complete.")

        st.write("#### Transfer SQL Batting")

        # Show button to run batting()
        if st.button("SQL"):
            st.write("Transferring Batting data to SQL...")
            processor = BattingSQLProcessor()
            processor.run()
            st.write("Batting data transfer to SQL complete.")
    elif selected == "Bowling":
        st.write("#### Bowling Web Scrapping")

        # Show button to run bowling()
        if st.button("CSV"):
            st.write("Processing Bowling CSV data...")
            bowling()
            st.write("Bowling CSV data processing complete.")

        st.write("#### Transfer SQL Bowling")

        # Show button to run bowling()
        if st.button("SQL"):
            st.write("Transferring Bowling data to SQL...")
            processor = BowlingSQLProcessor()
            processor.run()
            st.write("Bowling data transfer to SQL complete.")
    elif selected == "Match":
        st.write("#### Match Web Scrapping")

        # Show button to run match_data()
        if st.button("CSV"):
            st.write("Processing Match CSV data...")
            match_data()
            st.write("Match CSV data processing complete.")

        st.write("#### Transfer SQL Match")

        # Show button to run match_data()
        if st.button("SQL"):
            st.write("Transferring Match data to SQL...")
            processor = MatchDataSQLProcessor()
            processor.run()
            st.write("Match data transfer to SQL complete.")

    elif selected == "MVP":
        st.write("#### MVP Web Scrapping")

        # Show button to run mvp_data()
        if st.button("CSV"):
            st.write("Processing MVP CSV data...")
            mvp_data()
            st.write("MVP CSV data processing complete.")

        st.write("#### Transfer SQL MVP")

        # Show button to run mvp_data()
        if st.button("SQL"):
            st.write("Transferring MVP data to SQL...")
            processor = MVPDataSQLProcessor()
            processor.run()
            st.write("MVP data transfer to SQL complete.")
    elif selected == "Overs":
        st.write("#### Overs Web Scrapping")

        # Show button to run overs()
        if st.button("CSV"):
            st.write("Processing Overs CSV data...")
            overs()
            st.write("Overs CSV data processing complete.")

        st.write("#### Transfer SQL Overs")

        # Show button to run overs()
        if st.button("SQL"):
            st.write("Transferring Overs data to SQL...")
            processor = OversSQLProcessor()
            processor.run()
            st.write("Overs data transfer to SQL complete.")

    elif selected == "Stats":
        st.write("#### Stats Web Scrapping")

        # Show button to run stats()
        if st.button("CSV"):
            st.write("Processing Stats CSV data...")
            stats()
            st.write("Stats CSV data processing complete.")

        st.write("#### Transfer SQL Stats")

        # Show button to run stats()
        if st.button("SQL"):
            st.write("Transferring Stats data to SQL...")
            processor = StatsSQLProcessor()
            processor.run()
            st.write("Stats data transfer to SQL complete.")

    st.markdown("---")

    latest = option_menu(
        menu_title="Latest Web Scrappping",
        options=["Batting", "Bowling", "Match", "MVP", "Overs", "Stats"],
        icons=["bootstrap-fill", "0-circle", "table", "trophy", "speedometer", "bar-chart"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "black", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "Goldenrod",
                "color": "white",
                "::first-letter": {"color": "Goldenrod"}
            },
            "nav-link-selected": {
                "background-color": "Goldenrod",
                "color": "white",
                "font-weight": "bold"
            }
        }
    )

    if latest == "Batting":
        st.write("#### Latest Batting Web Scraping")
        if st.button("Latest CSV"):
            st.write("Processing Batting CSV data...")
            latest_batting()
            st.write("Batting CSV data processing complete.")

        st.write("#### Transfer Latest SQL Batting")
        if st.button("Latest SQL"):
            st.write("Transferring Batting data to SQL...")
            process_latest_batting_sql()
            st.write("Batting data transfer to SQL complete.")

    elif latest == "Bowling":
        st.write("#### Latest Bowling Web Scraping")
        if st.button("Latest CSV"):
            st.write("Processing Bowling CSV data...")
            latest_bowling()
            st.write("Bowling CSV data processing complete.")

        st.write("#### Transfer Latest SQL Bowling")
        if st.button("Latest SQL"):
            st.write("Transferring Bowling data to SQL...")
            process_latest_bowling_sql()
            st.write("Bowling data transfer to SQL complete.")

    elif latest == "Match":
        st.write("#### Latest Match Web Scraping")
        if st.button("Latest CSV"):
            st.write("Processing Match CSV data...")
            latest_match_data()
            st.write("Match CSV data processing complete.")

        st.write("#### Transfer Latest SQL Match")
        if st.button("Latest SQL"):
            st.write("Transferring Match data to SQL...")
            process_latest_match_data_sql()
            st.write("Match data transfer to SQL complete.")

    elif latest == "MVP":
        st.write("#### Latest MVP Web Scraping")
        if st.button("Latest CSV"):
            st.write("Processing MVP CSV data...")
            latest_mvp_data()
            st.write("MVP CSV data processing complete.")

        st.write("#### Transfer Latest SQL MVP")
        if st.button("Latest SQL"):
            st.write("Transferring MVP data to SQL...")
            process_latest_mvp_sql()
            st.write("MVP data transfer to SQL complete.")

    elif latest == "Overs":
        st.write("#### Latest Overs Web Scraping")
        if st.button("Latest CSV"):
            st.write("Processing Overs CSV data...")
            latest_overs()
            st.write("Overs CSV data processing complete.")

        st.write("#### Transfer Latest SQL Overs")
        if st.button("Latest SQL"):
            st.write("Transferring Overs data to SQL...")
            process_latest_overs_sql()
            st.write("Overs data transfer to SQL complete.")

    elif latest == "Stats":
        st.write("#### Latest Stats Web Scraping")
        if st.button("Latest CSV"):
            st.write("Processing Stats CSV data...")
            latest_stats()
            st.write("Stats CSV data processing complete.")

        st.write("#### Transfer Latest SQL Stats")
        if st.button("Latest SQL"):
            st.write("Transferring Stats data to SQL...")
            process_latest_stats_sql()
            st.write("Stats data transfer to SQL complete.")

    st.markdown("""
        <footer class="footer">
            <hr>
            Copyright &#169; 2024 All rights reserved by Gaurav Wankhede.
        </footer>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
