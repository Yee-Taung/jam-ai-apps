import streamlit as st
from jamaibase import JamAI, protocol as p
import requests
import os
from dotenv import load_dotenv

## The Dreamer app receives input about the users' dreams. Then, the clues of the dreams are analysed to 
## understand the hidden meanings in each dreams. 
## [Extra] Analyse the user's sleep patterns. 
## [Extra] Explore page to learn about some fun facts about humans' dreams. 