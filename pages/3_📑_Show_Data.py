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

    # Path to the directory containing CSV files
    csv_dir = os.path.join(os.path.dirname(__file__), "..")

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
        &#169; All rights reserved by Gaurav Wankhede.
    </footer>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
