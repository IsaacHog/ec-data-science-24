import streamlit as st
import google.generativeai as genai
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import configparser
import asyncio

# försök för att göra första inladdnigen snabbare genom att cacha data
@st.cache_data
def load_data():
    return pickle.load(open("texts.pkl", "rb")), faiss.read_index("faiss_index.bin")

texts, index = load_data()
model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

config = configparser.ConfigParser()
config.read("config.ini")
api_key = config.get("api", "key").strip('"') # ta bort citat tecken från nycklen


def get_relevant_context(query, top_n=3):
    query_vector = model.encode([query])
    distances, indices = index.search(query_vector, top_n)
    return [texts[i] for i in indices[0]]


async def generate_answer(query, api_key):  # kallar genai, retunerar svar
    try:
        relevant_info = get_relevant_context(query)
        context_str = "\n".join(relevant_info)

        if not api_key:
            st.error("API key not found in config.ini")
            return None

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = f"""You are a storyteller deeply familiar with the Harry Potter universe contained in the context of movie subtitles.  Based on the following movie subtitles and your extensive knowledge, answer the question in a way that best suits the context: use descriptive language and evoke the atmosphere and tone of the Harry Potter universe. If the question specifically asks about a particular character, answer from that character's perspective using first-person narration; otherwise, provide a third-person narrative account.

        Context:
        {context_str}

        Question: {query}"""
        response = await asyncio.to_thread(model.generate_content, prompt) # async kör generate_content från model klassen
        return response.text
    except Exception as e:
        st.error(f"Error generating answer: {e}")
        return None


# Streamlit app - frontend 
st.title("The Blabbering Hat")
st.subheader("A mystical hat overflowing with wisdom, but is unfortunetly far too enchanted with the sound of its own voice")
query = st.text_input("Enter your question:")

if query:
    with st.spinner("Generating answer..."):  # loading
        answer = asyncio.run(generate_answer(query, api_key)) # async kör generate_answer
    if answer: # Display svar om svar finns
        st.write(answer)
