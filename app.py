import os
import streamlit as st
import requests
import json
import faiss
import pickle
import numpy as np
from dotenv import load_dotenv
load_dotenv()

from sentence_transformers import SentenceTransformer

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

model = "deepseek/deepseek-llm-r1:free"

with open("vectordb/chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

index = faiss.read_index("vectordb/faiss.index")
embedder = SentenceTransformer(EMBEDDING_MODEL)

def retrieve(query, top_k=3):
    query_vec = embedder.encode([query])
    D, I = index.search(np.array(query_vec), top_k)
    return [chunks[i] for i in I[0]]

def get_response_from_model(prompt):
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "HTTP-Referer": "http://localhost",
        "X-Title": "rag-chatbot",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [
            {"role": "system", "content": "Answer the question using the following document content."},
            {"role": "user", "content": prompt}
        ],
        "stream": True,
        "max_tokens": 500, 
        "temperature": 0.7,
        "top_p": 0.9,
        "presence_penalty": 0.1,
        "frequency_penalty": 0.1
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            stream=True,
            timeout=60  
        )
        
        if response.status_code != 200:
            error_msg = f"API Error: {response.status_code} - {response.text}"
            st.error(error_msg)
            return

    
        for line in response.iter_lines():
            if line:
                if line.startswith(b"data: "):
                    try:
                        json_str = line[6:].decode('utf-8') 
                        if json_str.strip() == "[DONE]":
                            break
                        chunk = json.loads(json_str)
                        if "choices" in chunk and chunk["choices"]:
                            delta = chunk["choices"][0].get("delta", {})
                            if "content" in delta:
                                yield delta["content"]
                    except json.JSONDecodeError:
                        continue
                    except Exception as e:
                        st.error(f"Error processing chunk: {str(e)}")
                        continue
                        
    except requests.exceptions.Timeout:
        st.error("API request timed out. Please try again.")
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {str(e)}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")


#Streamlit UI
st.set_page_config(page_title="RAG Chatbot", layout="wide")
st.title("Chatbot using Mistral-7B and Document Search")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask something about the document..."):
    if prompt:
        if len(prompt.strip()) < 5 or not any(c.isalpha() for c in prompt):
            st.error("⚠️ Please enter a meaningful question.")
            st.stop()


    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    docs = retrieve(prompt, top_k=2)
    context = "\n\n".join(docs)

    model_input = f"""Please provide a detailed answer to the question based on the following context. Include relevant information and be specific in your response.

Context:
{context}

Question:
{prompt}

Please provide a comprehensive answer:"""

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        final_response = ""
    
        st.write("Source Chunks:")
        cols = st.columns(3) 
        
        for i, (doc, col) in enumerate(zip(docs, cols), 1):
            preview = doc[:100] + "..." if len(doc) > 100 else doc
            
        for token in get_response_from_model(model_input):
            final_response += token
            response_placeholder.markdown(final_response + "▌")
    
        response_placeholder.markdown(final_response)
        
        with st.expander("Source Chunks Used (click to expand each)"):
            for i, doc in enumerate(docs):
                preview = doc.strip().split('\n')[0][:60] + "..."
                with st.expander(f"Chunk {i+1}: {preview}"):
                    st.markdown(doc.strip())

        st.session_state.messages.append({
            "role": "assistant",
            "content": final_response
        })

with st.sidebar:
    st.sidebar.markdown("Model: Mistral-7B (OpenRouter)")
    st.markdown(f" **Total Chunks Indexed:** {len(chunks)}")
    if st.button(" Reset Chat"):
        st.session_state.messages = []
        st.rerun()
