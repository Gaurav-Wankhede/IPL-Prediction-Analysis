import streamlit as st
from streamlit_option_menu import option_menu
from Prev_Matches.Match_Link import match_link
from Latest_Matches.Latest_Match_Link import latest_match_link

st.set_page_config(page_title="Link Scraper", page_icon="./images/link.png", layout='wide')
with open("styles/style.css", "r") as f:
    css_content = f.read()

# Display the CSS content in Streamlit
st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
def main():
    st.title("ESPNcricinfo Link Scraper")

    selected = option_menu(
        menu_title="Select",
        options=["Previous Match Links", "Latest Match Links"],
        icons=["table", "table"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "black"},
            "icon": {"color": "black", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "Goldenrod",
                "color": "white",
                "::first-letter": {"color": "Goldenrod"},
            },
            "nav-link-selected": {
                "background-color": "Goldenrod",
                "color": "white",
                "font-weight": "bold",
            }
        }
    )

    if selected == "Previous Match Links":
        if st.button("Links"):
            st.write("Processing Previous Match CSV data...")
            match_link()
            st.write("Previous Match CSV data processing complete.")

    elif selected == "Latest Match Links":
        if st.button("Latest Links"):
            st.write("Processing Latest Match CSV data...")
            latest_match_link()
            st.write("Latest Match CSV data processing complete.")

    st.markdown("""
        <footer class="footer">
            <hr>
            Copyright &#169; 2024 All rights reserved by Gaurav Wankhede.
        </footer>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
