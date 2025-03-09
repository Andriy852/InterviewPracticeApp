from streamlit_mic_recorder import speech_to_text
import streamlit as st
text = speech_to_text(
    language='en',
    start_prompt="Start recording",
    stop_prompt="Stop recording",
    just_once=False,
    use_container_width=False,
    callback=None,
    args=(),
    kwargs={},
    key=None
)

st.write(text)
print(text)