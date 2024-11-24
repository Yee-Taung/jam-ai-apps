import streamlit as st
from jamaibase import JamAI, protocol as p
import requests
import os
from dotenv import load_dotenv

## The Dreamer app receives input about the users' dreams. Then, the clues of the dreams are analysed to 
## understand the hidden meanings in each dreams. 
## [Extra] Analyse the user's sleep patterns. 
## [Extra] Explore page to learn about some fun facts about humans' dreams. 

load_dotenv()
jamai = JamAI(api_key=os.getenv("JAM_API_KEY"), project_id=os.getenv("JAM_PROJECT_ID"))

st.set_page_config(page_title="Dreamer", page_icon="😴")
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
st.title("🧠 Learn from Your Dream")
st.write("Answer a few questions to understand your dream and its hidden meaning.")
age = st.text_input("What's your age?", value=None,placeholder="Type your age...")
occupation = st.text_input("What's your occupation?", value=None, placeholder="Job Role...",help="Type in 'student' if you're studying, or 'unemployed' if you're not working at the moment.")
sleeping_hours = st.text_input("What's your average sleep hours per day?", value=None, placeholder="Type your sleeping hours...")
stress_levels = st.slider("Rate your stress level:", 0,10)
dream_tendency = st.slider("How often do you dream per week?", 0,7,help="Choose 7 if you dream more than 7 times per week.")
dream_types = st.multiselect("Which terms best describe your dream?",
                             ("Adventure", "Romantic", "Mystical", "Conflict", "Transformation", "Exploration", "Resolution"), 
                             help="Adventure - A dream that involves exploration, quests, or daring journeys.\n\nRomantic - A dream centered on love, affection, or emotional intimacy.\n\nMystical - A dream with elements of spirituality, magic, or otherworldly experiences.\n\nConflict - A dream involving struggles, arguments, or battles, either physical or emotional.\n\nTransformation - A dream about change, growth, or metamorphosis, either literal or symbolic.\n\nExploration - A dream that focuses on discovering new places, ideas, or aspects of oneself.\n\nResolution - A dream where unresolved issues or problems are addressed or solved.")
dream_objects = st.text_area("What are the objects you remember in your dream?", help="Any objects or even people.")
dream_stories = st.text_area("Write your dream ✍", help="Type in the dream objects if you don't remember much.")

if st.button("Discover My Dream"):
    if age and occupation and sleeping_hours and dream_types and dream_objects and dream_stories: 
        with st.spinner("Processing... Please wait."):
            with st.expander("🌙 What Are Dreams?"):
                st.write("""
                Dreams are a series of thoughts, images, sensations, or emotions that occur during sleep. 
                They typically happen during the Rapid Eye Movement (REM) stage of sleep, 
                when brain activity is high and resembles that of wakefulness.
                """)

            with st.expander("💤 Types of Dreams"):
                st.write("""
                Dreams can be categorized into various types, such as:
                - **Lucid Dreams**: Dreams where you are aware you're dreaming.
                - **Nightmares**: Distressing dreams that cause fear or anxiety.
                - **Recurring Dreams**: Dreams that repeat over time, often with similar themes.
                - **Day-to-Day Dreams**: Reflecting mundane daily experiences.
                """)
            with st.expander("❓ Why Do We Dream?"):
                st.write("""
                Theories about why we dream include:
                - **Memory Consolidation**: Processing and storing daily memories.
                - **Emotional Regulation**: Coping with emotions and stress.
                - **Problem Solving**: Generating creative solutions to waking issues.
                """)

            with st.expander("🎉 Fun Facts About Dreams"):
                st.write("""
                - Most people dream 4-6 times per night, but only remember a fraction.
                - Blind individuals experience dreams involving their other senses.
                - Some inventions, like the periodic table, were inspired by dreams!
                """)     
            try:
                completion = jamai.add_table_rows(
                    "action",
                    p.RowAddRequest(
                        table_id="dreamerv2", 
                        data=[{
                            "age": age,
                            "occupation": occupation,
                            "sleeping_hours": sleeping_hours,
                            "stress_levels": str(stress_levels),
                            "dream_tendency": str(dream_tendency),
                            "dream_types": str(dream_types),
                            "dream_objects": dream_objects,
                            "dream_stories": dream_stories,
                        }],
                stream=False
                ))

                if completion.rows:
                    output_row = completion.rows[0].columns
                    dream_recap = output_row.get("dream_recap")
                    symbol_analysis = output_row.get("symbol_analysis")
                    emotional_context_and_relevance = output_row.get("emotional_context_and_relevance")
                    practical_advices = output_row.get("practical_advices")
                    encouragement = output_row.get("encouragement")

                    st.subheader("🌟 Reveal Your Dream ")
                    st.markdown(
                        f"""
                        <div class="generated-output">
                            <h4>✨ Dream Summary:</h4> <p>{dream_recap.text if dream_recap else 'N/A'}</p>
                            <h4>🚥 Symbol Analysis:</h4> <p>{symbol_analysis.text if symbol_analysis else 'N/A'}</p>
                            <h4>🤗 Emotional and Relevance:</h4> <p>{emotional_context_and_relevance.text if emotional_context_and_relevance else 'N/A'}</p>
                            <h4>💬 Practical Advices:</h4> <p>{practical_advices.text if practical_advices else 'N/A'}</p>
                            <h4>🤔 What Should I do? :</h4> <p>{encouragement.text if encouragement else 'N/A'}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.error("Something went wrong. Please try again later.")
            except Exception as e:
                    st.error(f"An error occurred: {e}")
        st.success("🌙 As you lay down to rest, may your dreams be as beautiful and magical as the stars in the night sky. Sleep well, and may tomorrow bring new adventures. Sweet dreams! 🌌")    
    else:
        st.warning("Please fill in all fields.")