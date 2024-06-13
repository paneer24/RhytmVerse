import os
import base64
import json
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Get environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure the Google API key
genai.configure(api_key=GOOGLE_API_KEY)

generation_config_b64 = 'eyJ0ZW1wZXJhdHVyZSI6MC45LCJ0b3BfcCI6MSwidG9wX2siOjEsIm1heF9vdXRwdXRfdG9rZW5zIjoyMDQ4LCJzdG9wX3NlcXVlbmNlcyI6W119' # @param {isTemplate: true}
safety_settings_b64 = 'W3siY2F0ZWdvcnkiOiJIQVJNX0NBVEVHT1JZX0hBUkFTU01FTlQiLCJ0aHJlc2hvbGQiOiJCTE9DS19NRURJVU1fQU5EX0FCT1ZFIn0seyJjYXRlZ29yeSI6IkhBUk1fQ0FURUdPUllfSEFURV9TUEVFQ0giLCJ0aHJlc2hvbGQiOiJCTE9DS19NRURJVU1fQU5EX0FCT1ZFIn0seyJjYXRlZ29yeSI6IkhBUk1fQ0FURUdPUllfU0VYVUFMTFlfRVhQTElDSVQiLCJ0aHJlc2hvbGQiOiJCTE9DS19NRURJVU1fQU5EX0FCT1ZFIn0seyJjYXRlZ29yeSI6IkhBUk1fQ0FURUdPUllfREFOR0VST1VTX0NPTlRFTlQiLCJ0aHJlc2hvbGQiOiJCTE9DS19NRURJVU1fQU5EX0FCT1ZFIn1d' # @param {isTemplate: true}
generation_config = json.loads(base64.b64decode(generation_config_b64))
safety_settings = json.loads(base64.b64decode(safety_settings_b64))
model = 'gemini-pro'

# Include custom CSS for background
st.markdown(
    """
    <style>
    body {
        background-image: url('https://example.com/your-background-image.jpg');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    st.title("Rhymeweaver")
    st.write("Invoking the magic of poetry, this name alludes to the application's ability to craft intricate rhymes that dance off the page.")
    st.write('With an intuitive user interface and a user-friendly design, this web application invites users to embark on a creative odyssey. By simply providing a few details about the individual, such as their name, interests, and passions, the application harnesses the transformative power of Gemini Pro to generate a personalized poem. Whether it"s a heartfelt tribute to a loved one, a celebration of personal achievements, or a reflective exploration of lifes complexities, the application adapts to the users preferences, producing poems that resonate with authenticity and emotional depth.')

# Main application title
st.title("Rhymeweaver")

# Areas of interest
aoi = [
    "Reading",
    "Exercising",
    "Listening to music",
    "Watching movies",
    "Playing video games",
    "Traveling",
    "Cooking",
    "Gardening",
    "Photography",
    "Art and crafts",
    "DIY projects",
    "Learning new skills",
    "Meditation",
    "Spending time with friends and family",
    "Volunteering",
    "Technology",
    "Science",
    "History",
    "Politics",
    "Economics",
    "Philosophy",
    "Psychology",
    "Sociology",
    "Art",
    "Music",
    "Literature",
    "Film",
    "Fashion",
    "Travel",
    "Food and drink",
    "Health and wellness",
    "Sports",
    "Current events"
]

# Form input
col1, col2, col3 = st.columns(3)
with col1:
    name = st.text_input('Name')
    age = st.text_input('Age')
    interest = st.multiselect('Area of interest', options=aoi)
    others = st.text_input('Other interest (if any)', placeholder='separated by comma')
with col2:
    state = st.text_input('State ')
    country = st.text_input('Country ')
    profession = st.text_input('What is your job')
    fav_show_movie = st.text_input('Favourite Show and movies', placeholder='separated by comma')
with col3:
    fav_songs = st.text_input('Favourite songs/singers/genres', placeholder='separated by comma')
    gender = st.selectbox('Gender', options=['Male', 'Female'])
    language = st.selectbox('Poem ka language', ['English', 'Hindi', 'Tamil'])

# Generate poem content
contents = f'A person whose name is {name}. Gender is {gender}. Age is {age}. Area of interest are {", ".join(interest)}.'
contents += f' Lives in state of {state} located in country {country}.'
contents += f'Profession is {profession}. Favourite show and movies are {fav_show_movie}. And Favourite songs/singers/genres are {fav_songs}.'
contents += f'Write a high quality rhyming poem about 50 lines describing the person which will be a masterpiece when read by a user. Language of the poem would be {language}.'

# Button to generate the poem
if st.button('Generate', key='gen'):
    with st.spinner('Wait for it'):
        try:
            gemini = genai.GenerativeModel(model_name=model)
            response = gemini.generate_content(
                contents,
                generation_config=generation_config,
                safety_settings=safety_settings,
                stream=False
            )

            if generation_config.get('candidate_count', 1) == 1:
                st.text_area(label="", value=response.text, height=500)
            else:
                st.error('It is Prohibited.')
        except Exception as e:
            st.error('Retry after some time')
            
    st.success('Done')
