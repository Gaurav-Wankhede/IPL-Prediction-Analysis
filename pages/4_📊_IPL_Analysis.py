import streamlit as st

st.set_page_config(page_title="IPL Analysis", page_icon="./images/analysis.png", layout='wide')
with open("styles/style.css", "r") as f:
    css_content = f.read()

# Display the CSS content in Streamlit
st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

st.markdown("""
    <footer class="footer">
        <hr>
        Copyright &#169; 2024 All rights reserved by Gaurav Wankhede.
    </footer>
    """, unsafe_allow_html=True)