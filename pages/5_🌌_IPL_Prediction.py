import streamlit as st

st.set_page_config(page_title="IPL Prediction", page_icon=":bar_chart:", layout='wide')
with open("styles/style.css", "r") as f:
    css_content = f.read()
    # Display the CSS content in Streamlit
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

st.markdown("""
<footer class="footer">
    <hr>
    &#169; All rights reserved by Gaurav Wankhede.
</footer>
""", unsafe_allow_html=True)