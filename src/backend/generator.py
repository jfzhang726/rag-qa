
from typing import List
import streamlit as st

from langchain import hub
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

from backend.interfaces import IVectorStore
from backend.interfaces import ILLMService


rag_prompt_template = hub.pull("rlm/rag-prompt")
Stringoutputparser = StrOutputParser()

def format_docs(docs: List[str]) -> str:
    return "\n\n".join(doc for doc in docs)

def generate_response(query_text:str, vector_store: IVectorStore, llm_service: ILLMService)->str:
    try:
        documents = vector_store.query(query_text, top_k=5)
        context = format_docs(documents)
        prompt = rag_prompt_template.format(context=context, question=query_text)
        response = llm_service.generate_response(prompt)
        result = Stringoutputparser.invoke(response)
        return result
        # RAG chain
        # rag_chain = (
        #     {"context": retriever | format_docs,  "question": RunnablePassthrough()}
        #     | prompt
        #     | llm
        #     | StrOutputParser()
        # )

        # st.write("RAG chain set up successfully.")
        # st.write("Generating response...")
        # response = rag_chain.invoke(query_text)
        # st.write("Response generated successfully.")
        # return response
    except Exception as e:
        st.error(f"Error generating response: {e}")
        st.stop()
    