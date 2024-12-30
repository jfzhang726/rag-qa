import streamlit as st 
import requests
from io import BytesIO
import os
from dotenv import load_dotenv


import logging

logger = logging.getLogger("Streamlit")

load_dotenv()

FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8001/api")
STORAGE_TYPE = os.getenv("RAW_FILE_STORAGE_TYPE", "local")

def list_files():
    try:
        response = requests.get(f"{FASTAPI_URL}/files")
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Error listing files: {response.text}")
            return []
    except Exception as e:
        logger.error(f"Error listing files: {e}")
        return []


def main():
    st.title("Retrieval-Augmented Generation (RAG) Demo")

    menu = ["Home", "Ask Questions", "Upload Documents", "Manage Documents"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Home":
        st.subheader("Welcome to the RAG demo!")
        st.write("Use the sidebar to navigate to different sections of the demo.")
    elif choice == "Upload Documents":
        st.subheader("Upload Documents")
        uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'txt'], accept_multiple_files=False)
        if st.button("Upload"):
            if uploaded_file:
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                try:
                    response = requests.post(f"{FASTAPI_URL}/upload", files=files)
                    if response.status_code == 200:
                        uuid = response.json().get("uuid")
                        st.success(f"File uploaded successfully! UUID: {uuid}")
                    else:
                        error_details = response.json().get("detail", "Unknown error")
                        st.error(f"Error uploading file: {error_details}")
                except Exception as e:
                    st.error(f"Error uploading file: {e}")
            else:
                st.warning("Please choose a file to upload.")
    elif choice == "Ask Questions":
        st.subheader("Ask a Question")
        query = st.text_area("Enter your query")
        if st.button("Submit"):
            st.info(f"Processing your query...{query}")
            if query.strip() != "":
                payload = {"query": query}
                try:
                    response = requests.post(f"{FASTAPI_URL}/ask", json=payload)
                    if response.status_code == 200:
                        response_text = response.json().get("response", "No response")
                        st.success(response_text)
                    else:
                        error_details = response.json().get("detail", "Unknown error")
                        st.error(f"Error processing query: {error_details}")
                except Exception as e:
                    st.error(f"Error processing query: {e}")
            else:
                st.warning("Please enter a query to ask.")
    elif choice == "Manage Documents":
        st.subheader("Manage Documents")
        result = list_files()
        files = result.get("files", [])
        if files:
            st.write("List of uploaded documents:")
            for file in files:
                st.write(f"UUID: {file['uuid']}, Filename: {file['original_filename']}, status: {file['status']}, uploaded on: {file['upload_timestamp']}")
        else:
            st.warning("No documents found.")

if __name__ == "__main__":
    main()