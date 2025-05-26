import streamlit as st
import google.generativeai as genai
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os
import configparser

# Load pre-computed data
texts = pickle.load(open("texts.pkl", "rb"))
index = faiss.read_index("faiss_index.bin")
model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

config = configparser.ConfigParser()
config.read("config.ini")
api_key = config["api"]["key"]


def get_relevant_context(query, top_n=3):
    query_vector = model.encode([query])
    distances, indices = index.search(query_vector, top_n)
    return [texts[i] for i in indices[0]]


def generate_answer(query):
    relevant_info = get_relevant_context(query)
    context_str = "\n".join(relevant_info)

    try:
        st.write(f"API Key: {api_key}")
        if not api_key:
            st.error("API key not found in config.ini")
            return None
        st.write(f"API Key: {api_key}")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(
            f"Based on the following movie subtitles, answer the question:\n\nContext:\n{context_str}\n\nQuestion: {query}"
        )
        return response.text
    except Exception as e:
        st.error(f"Error generating answer: {e}")  # Use Streamlit's error handling
        return "Error generating answer."


# Streamlit app
st.title("Harry Potter Subtitle RAG")
query = st.text_input("Enter your question:")

if query:
    answer = generate_answer(query)
    st.write(answer)

