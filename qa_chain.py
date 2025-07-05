import streamlit as st 
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from youtube_utils import transcript_chunks
from dotenv import load_dotenv

load_dotenv()

@st.cache_resource(show_spinner="Embedding transcript and building vector store...")
def build_vector_store(video_id,language):
    chunks,_ = transcript_chunks(video_id,language)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    return FAISS.from_documents(chunks, embeddings)

def build_qa_chain(video_id,language):
    vectorStore = build_vector_store(video_id,language)
    retriever = vectorStore.as_retriever(search_type='similarity', kwargs={'k': 4})
    prompt = PromptTemplate(
        template="""
         you are a helpful assistant.
    Answer form the provided transcript context.
    if the context is insufficient, just say you don't know.
    No matter what is the language used in context reply only in english.\n
    {context}\n
    Question: {question}
         """,
        input_variables=['context', 'question']
    )
    
    def context_text(retrieved_docs):
        return '\n\n'.join(doc.page_content for doc in retrieved_docs)

    context_chain = RunnableParallel({
        'context': retriever | RunnableLambda(context_text),
        'question': RunnablePassthrough()
    })

    model = ChatGoogleGenerativeAI(model='gemini-2.0-flash-001')
    parser = StrOutputParser()

    return context_chain | prompt | model | parser
