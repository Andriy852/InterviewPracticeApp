import streamlit as st
from utils.utilities import (start_interview, end_interview, 
                             record_and_transcribe, is_input_safe, 
                             process_user_input)
from utils.system_prompt import generate_system_prompt
from streamlit_mic_recorder import speech_to_text

# set page configuration
st.set_page_config(page_title="Mock Technical Interview App", layout="wide")
st.title("Mock Technical Interview App")

# create input fields
role = st.text_input("Enter the role:*")
company = st.text_input("Enter the company:*")
job_description = st.text_area("Enter the job description:*")
level = st.selectbox("Select the role level:*", ["Junior", "Mid-Level", "Senior", "Lead"])
persona = st.selectbox("Select the persona of the interviewer:*", ["Strict", "Neutral", "Friendly"])
resume = st.file_uploader("Upload your resume*", type="pdf")

st.subheader("Customize Interview Questions")
custom_questions = st.text_area("Enter questions you want the interviewer to ask you (one per line)")

# create session state variables
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "interview_started" not in st.session_state:
    st.session_state.interview_started = False
    
all_fields_filled = role and company and job_description and level and resume and persona

# generate system prompt
if all_fields_filled:
    system_prompt = generate_system_prompt(role, company, level, resume, job_description, persona, custom_questions)

# create chat container
st.subheader("Interview Conversation")
chat_container = st.container()

with chat_container:
    for message in st.session_state.conversation:
        if message["role"] == "assistant":
            st.chat_message("assistant").write(message["content"])
        elif message["role"] == "user":
            st.chat_message("user").write(message["content"])

# start-end interview buttons
# disabled=not all_fields_filled
if not st.session_state.interview_started:
    if st.button("Start Interview"):
        start_interview(system_prompt)
else:
    if st.button("End Interview"):
         end_interview()

# chat input
if st.session_state.interview_started:
    user_input = st.chat_input("Your response...")
    text = speech_to_text(
                    language='en',
                    start_prompt="Start recording",
                    stop_prompt="Stop recording",
                    just_once=True
                )
    if text:
        user_input = text
    if user_input:
        if not is_input_safe(user_input):
            st.error("Your input violates security policies. Please rephrase.")
        else:
            process_user_input(user_input, system_prompt)
