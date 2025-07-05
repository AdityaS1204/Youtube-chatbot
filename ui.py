import streamlit as st

Language_options = [
    "en", "hi", "bg", "zh", "hr", "cs", "da", "nl", "ar", "et",
  "fi", "fr", "de", "el", "iw", "bn", "hu", "id", "it", "ja",
  "ko", "lv", "lt", "no", "pl", "pt", "ro", "ru", "sr", "sk",
  "sl", "es", "sw", "sv", "th", "tr", "uk", "vi"
]


def show_ui():
  st.header('Chat with Youtube videos')
  col1,col2 = st.columns(2)
  with col1:
    yt_video = st.text_input("Youtube video link:",placeholder='Enter youtube video Link')
    question = st.text_input("Your Question:",placeholder='Ask anything about the video')
    language = st.selectbox("Transcript Language:",Language_options)
  return yt_video,question,language,col1,col2