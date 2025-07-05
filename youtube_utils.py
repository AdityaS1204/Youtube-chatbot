import re
from langchain_community.document_loaders.youtube import YoutubeLoader,TranscriptFormat
from langchain.text_splitter import RecursiveCharacterTextSplitter


def extract_yt_video_id(url):
    regex = (
        r"(?:https?://)?(?:www\.)?(?:youtube\.com/(?:watch\?v=|embed/)|youtu\.be/)([\w\-]{11})"
    )
    match = re.search(regex, url)
    return match.group(1) if match else None

def transcript_chunks(video_id,language):
    loader = YoutubeLoader(
        video_id=video_id,
        language=language,
        transcript_format=TranscriptFormat.TEXT,
        chunk_size_seconds=120
    )
    transcript = loader.load()
    full_transcript = "\n\n".join(doc.page_content for doc in transcript)
    spliter = RecursiveCharacterTextSplitter(chunk_size=900,chunk_overlap=200)
    chunks = spliter.split_documents(transcript)
    return chunks,full_transcript     