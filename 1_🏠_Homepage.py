import streamlit as st
from streamlit_lottie import st_lottie
import requests

# Set an awesome background image (replace with your preferred image URL)
st.set_page_config(page_title="IPL Prediction Analysis", page_icon="./images/ipl.png", layout="wide")
# Create a CSS style to set the background image
# Open and read the CSS file
with open("styles/style.css", "r") as f:
    css_content = f.read()

# Display the CSS content in Streamlit
st.markdown(f"<style>{css_content}</style>",
            unsafe_allow_html=True)
# Function to load Lottie animations
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
# Define the HTML content
html_content = """
<div style="display: flex; justify-content: center; align-items: center; height: 100%;">
    <div style="width: 100%; height: 100%;">
        <script src="https://unpkg.com/@dotlottie/player-component@latest/dist/dotlottie-player.mjs" type="module"></script>
        <dotlottie-player src="https://lottie.host/1d763ded-9739-4b6a-bfce-efed70f50444/95WucJn0LJ.json" background="transparent" speed="1" style="width: 100%; height: 100%;" loop autoplay></dotlottie-player>
    </div>
</div>
"""
# Create a visually appealing title and subheading
st.title("🏆 IPL Prediction Analysis")

l, r = st.columns([3, 1])
with l:
    st.subheader("Unleash Your Inner Cricket Analyst")

    # Craft a compelling and informative description about IPL
    st.markdown(
        """
        The Indian Premier League (IPL) is the biggest cricket tournament in the world,
        renowned for its high-octane action, explosive batting displays, and nail-biting finishes.
        This platform empowers you to become your own IPL prediction guru by harnessing
        the power of data analysis and machine learning models.

        **What can you expect here?**

        * **Insightful Match Predictions:** Leverage advanced models to gain a statistical edge
          in predicting match outcomes. Understand the factors that influence the game's course.
        * **Data-Driven Analysis:** Explore comprehensive visualizations that delve into team
          performance, player statistics, and historical trends. Gain a deeper understanding of
          the IPL landscape.
        * **Interactive Features:** Engage with interactive elements to personalize your
          experience. Fine-tune predictions based on your own insights and preferences.

        **Stay tuned!** We're constantly refining our models and incorporating the latest IPL
        data to deliver the most accurate and insightful predictions.
        """
    )

with r:
    # Embed the Lottie animation using an iframe
    st.components.v1.html(html_content, height=300)
    # Render the Lottie animation

# Add a call to action button to pique user interest (replace with your internal route)
st.button("Explore IPL Predictions Now!", on_click=lambda: st.snow())

# Optionally, include a brief explainer on how your prediction models work
st.markdown(
    """
    **Behind the Predictions:**

    Our models are trained on a vast dataset of historical IPL matches, incorporating
    factors like team performance, player statistics, venue history, and weather
    conditions. These models then learn to identify patterns and correlations that
    can influence the outcome of a match.

    **Important Disclaimer:** Remember that cricket is a dynamic sport with a
    significant element of human influence. While our predictions offer valuable
    insights, they should not be considered a guaranteed outcome. Use them as a tool
    to enhance your IPL analysis and enjoyment.
    """
)

st.markdown("""
    <footer class="footer">
        <hr>
        Copyright &#169; 2024 All rights reserved by Gaurav Wankhede.
    </footer>
    """, unsafe_allow_html=True)