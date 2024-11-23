import streamlit as st
from jamaibase import JamAI, protocol as p
import requests
import os
from dotenv import load_dotenv

load_dotenv()
jamai = JamAI(api_key=st.secrets["JAM_API_KEY"], project_id=st.secrets["JAM_PROJECT_ID"])
UNSPLASH_ACCESS_KEY = st.secrets["UNSPLASH_ACCESS_KEY"]

# Helper function to fetch photos from Unsplash
def fetch_photo(query):
    url = f"https://api.unsplash.com/search/photos?query={query}&client_id={UNSPLASH_ACCESS_KEY}&per_page=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            return data["results"][0]["urls"]["small"]  # Return the first photo URL
    return None

st.set_page_config(page_title="Your Dream Life", page_icon="🌳")
# Multi-tab interface
tabs = st.tabs(["Discover Your Dream", "Explore"])
discover_tab, explore_tab = tabs

# Custom CSS to style the UI
st.markdown(
    """
    <style>
    body {
        background-color: #1e1e1e;
        color: #f0f0f0;
    }
    .generated-output {
        background-color: #444;
        padding: 15px;
        border-radius: 10px;
        margin-top: 20px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5);
        color: #f0f0f0;
    }
    .generated-output h4 {
        color: #FFA500;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True
)

with discover_tab:
    st.title("Discover Your Dream Life")
    st.write("Answer a few questions to find your ideal life dream and learn how to achieve it.")

    # Collect user inputs
    age = st.slider("What's your age?", 7, 99)
    hobbies = st.text_area("What are your hobbies or passions?")
    skills = st.text_input("List your top skills:")
    dream_themes = st.multiselect("Choose your top values:", 
                        ["Family", "Freedom", "Creativity", "Helping Others", "Adventure", "Success", "Financial Freedom", "Knowledge"])

    if st.button("Discover My Dream"):
        if age and hobbies and skills and dream_themes:      
            try:
        # Send user inputs to the Jam AI base table
                completion = jamai.add_table_rows("action",
            p.RowAddRequest(
                table_id="dream-discovery-table",  # Replace with your table ID
                data=[{
                        "age": age,
                        "hobbies": hobbies,
                        "skills": skills,
                        "dream_themes": dream_themes,
                    }],
                stream=False
                ))
                if completion.rows:
                    output_row = completion.rows[0].columns
                    dream_summary = output_row.get("dream_summary")
                    roadmap = output_row.get("roadmap")
                    motivational_quote = output_row.get("motivational_quote")

                    st.subheader("🌟 Your Dream Life Revealed")
                    st.markdown(
                        f"""
                        <div class="generated-output">
                            <h4>✨ Dream Summary:</h4> <p>{dream_summary.text if dream_summary else 'N/A'}</p>
                            <h4>📍 Roadmap to Achieve Your Dream:</h4> <p>{roadmap.text if roadmap else 'N/A'}</p>
                            <h4>💬 Motivational Quote:</h4> <p>{motivational_quote.text if motivational_quote else 'N/A'}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.error("Something went wrong. Please try again later.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please fill in all fields.")

with explore_tab:
    st.title("🌟 Explore Inspiring Life Stories")
    st.write("Discover stories of people who followed their dreams and achieved remarkable things!")


