import streamlit as st 
from app.utils.streamlit_helpers import create_spinner 
from backend.data_loader import process_documents
from backend.interfaces import IVectorStore, ILLMService
from backend.dependency_factory import DependencyFactory
from backend.generator import generate_response

import logging

logger = logging.getLogger("Streamlit")

@st.cache_resource 
def get_vector_store() -> IVectorStore:
    return DependencyFactory.get_vector_store()

@st.cache_resource
def get_llm_service() -> ILLMService:
    return DependencyFactory.get_llm_service()




def ask_questions():
    st.title("Ask Questions")
    st.write("This is a demo of RAG using  gpt-4o-mini model.")

    query_text = st.text_input(
        "Enter your query",
        placeholder="Enter your query here"
        )

    result = None

    with st.form(key="qa_form", clear_on_submit=False, border=False):
        submitted = st.form_submit_button(label="Submit", disabled=not query_text)
        if submitted:
            try:
                st.write("Generating response...")
                vector_store = get_vector_store()
                llm_service = get_llm_service()
                response = generate_response(query_text, vector_store, llm_service)
                result = response
                st.write("Response generated successfully.")
            except Exception as e:
                st.error(f"Error generating response: {e}")
                st.stop()
    if result is not None:
        st.info(result)


def upload_documents():
    st.title("Upload Documents")

    uploaded_files = st.file_uploader(
        "Choose a file",
        type=['pdf', 'txt'],
        accept_multiple_files=True)

    if uploaded_files:
        with st.form(key="upload_form", clear_on_submit=True):
            submitted = st.form_submit_button("Upload")
            if submitted:
                try:
                    # Process and store documents
                    st.write("Uploading documents...")
                    vector_store = get_vector_store()
                    texts = [f.read().decode("utf-8") for f in uploaded_files]
                    logger.info(f"uploaded content size {len(texts)}")
                    documents = process_documents(texts)
                    logger.info(f"processed documents: {len(documents)}")
                    vector_store.add_documents(documents)
                    st.success("Documents uploaded successfully!")
                    
                except Exception as e:
                    st.error(f"Error uploading documents: {e}")
              


st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Ask Questions", "Upload Documents"], key="navigation")

if page == "Ask Questions":
    ask_questions()
elif page == "Upload Documents":
    # from app.upload import upload_documents
    upload_documents()
    


