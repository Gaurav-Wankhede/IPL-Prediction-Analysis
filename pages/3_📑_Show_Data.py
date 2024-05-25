import os
import pandas as pd
import streamlit as st

with open("styles/style.css", "r") as f:
    css_content = f.read()
st.set_page_config(page_title="Show CSV Data", page_icon=":bar_chart:", layout='wide')
# Display the CSS content in Streamlit
st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

def main():
    st.title("Show CSV Data")

    # Define cricket statistics
    statistics = {
        "🏏Runs:": "Represents the total runs scored by a batsman during their innings.",
        "🥎Balls Faced:": "Denotes the total number of balls faced by the batsman.",
        "⏳Minutes Played:": "Usually stands for Minutes, representing the total number of minutes the batsman spent at the crease during their innings.",
        "4️⃣Fours:": "Indicates the number of boundaries (fours) hit by the batsman.",
        "6️⃣Sixes:": "Signifies the number of maximums (sixes) hit by the batsman.",
        "🔥Strike Rate:": "Stands for Strike Rate, which is a measure of how effectively a batsman is scoring runs. It is calculated as (Runs / Balls) * 100, representing the number of runs scored per 100 balls faced."
    }

    # Display cricket statistics descriptions
    st.header("Cricket Statistics Description")
    for stat_name, description in statistics.items():
        st.write(f"**{stat_name}**")
        st.write(description)

    # Path to the directory containing CSV files
    csv_dir = os.path.join(os.path.dirname(__file__), "..\CSV")

    # Check if the directory exists
    if not os.path.exists(csv_dir):
        st.warning("Directory containing CSV files not found.")
        return

    try:
        # List all CSV files in the directory
        csv_files = [file for file in os.listdir(csv_dir) if file.endswith('.csv')]

        # Check if any CSV files are found
        if len(csv_files) == 0:
            st.warning("No CSV files found in the directory.")
            return

        # Iterate over each CSV file
        for filename in csv_files:
            st.write(f"### {filename}")  # Write the filename above the dataframe
            file_path = os.path.join(csv_dir, filename)

            # Read the CSV file using pandas
            df = pd.read_csv(file_path)

            # Show the dataframe using st.dataframe
            st.dataframe(df)

    except FileNotFoundError:
        st.error("Directory containing CSV files not found.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

    st.markdown("""
        <footer class="footer">
            <hr>
            Copyright &#169; 2024 All rights reserved by Gaurav Wankhede.
        </footer>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
