import streamlit as st
from ui import show_ui
from qa_chain import build_qa_chain
from youtube_utils import extract_yt_video_id,transcript_chunks
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title='Youtube Chatbot',layout='wide')

yt_video,question,language,col1,col2 = show_ui()
with col1:
    if st.button('send'):
        if not yt_video or not question:
            st.warning("please enter both a video url and your question")
        else:
                with st.spinner("Processing..."):
                    try:    
                        video_id = extract_yt_video_id(yt_video)
                        print("video_id before id check:",video_id)
                        if "video_id" not in st.session_state:
                            st.session_state.video_id = None
                        if "video_id" not in st.session_state or st.session_state.video_id != video_id:
                            print("video_id after id check:",st.session_state.video_id)
                            chunks,full_transcript = transcript_chunks(video_id,language)
                            st.session_state.video_id = video_id
                            st.session_state.full_transcript = full_transcript
                            qa_chain = build_qa_chain(video_id,language)
                            result = qa_chain.invoke(question)
                            st.write(result)
                        else:
                            qa_chain = build_qa_chain(video_id,language)
                            result = qa_chain.invoke(question)
                            st.write(result)        
                    except Exception as e:
                        st.error(f"Error:{str(e)}")   
                             
with col2:
    if "full_transcript" in st.session_state:
        st.subheader("Video Transcript")
        st.text_area("Video Transcript",value=st.session_state.full_transcript,height=400)                    
    else:
        st.subheader("Video Transcript")
        st.text_area("Video Transcript",value="",placeholder="Transcript will appear here once available",height=400)                    
                        