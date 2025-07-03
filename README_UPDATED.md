
# 📚 RAG Chatbot using Mistral‑7B (OpenRouter)

This is a document-aware chatbot project that answers user questions based on the content of a provided PDF file. It uses a Retrieval-Augmented Generation (RAG) pipeline and displays responses in a real-time streaming format.

---

## 🧠 Key Features

- ✅ Document-aware question answering
- ✅ Real-time streamed responses using Mistral‑7B (OpenRouter)
- ✅ Semantic chunk retrieval using FAISS
- ✅ Source chunk transparency (expandable in UI)
- ✅ Input validation to block meaningless input
- ✅ Streamlit UI with chunk index and reset feature

---

## 🔗 GitHub Repo

👉 [rag_chatbot_rohit](https://github.com/Rohit-raj96/rag_chatbot_rohit)

---

## 📺 Streaming Demo

![Streaming Demo](https://github.com/Rohit-raj96/rag_chatbot_rohit/blob/main/streaming_demo.gif)

---

## 📁 Project Structure

```
rag-chatbot/
├── app.py                       # Main Streamlit app
├── requirements.txt             # All required packages
├── .env                         # Your OpenRouter API key (keep secret)
├── vectordb/
│   ├── faiss.index              # FAISS vector DB
│   └── chunks.pkl               # Saved document chunks
├── chunks/                      # Split chunks (if stored)
├── src/
│   ├── preprocess.py            # PDF loader and chunker
│   └── embed_store.py           # Embedding generator + FAISS store
├── AI_Assignment_Rohit_Garg.pdf  # Final report with screenshots
├── streaming_demo.gif           # Live typing demo
├── invalid_input_warning.png    # Screenshot of input validation
```

---

## ⚙️ How to Run

### 1. Clone the repo
```bash
git clone https://github.com/Rohit-raj96/rag_chatbot_rohit.git
cd rag_chatbot_rohit
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your OpenRouter API key

Create a `.env` file with:
```
OPENROUTER_API_KEY=your_key_here
```

### 4. Process PDF & Store Embeddings

```bash
python src/preprocess.py
python src/embed_store.py
```

### 5. Run the Chatbot

```bash
streamlit run app.py
```

---

## 💬 Example Questions to Try

| Input                             | Behavior                        |
|----------------------------------|----------------------------------|
| What is the refund policy?       | ✅ Answered from 2 source chunks |
| What are the deliverables?       | ✅ Answered from document        |
| What is the capital of France?   | ✅ Answered (not in document)    |
| asdf                             | ❌ Blocked                       |
| asdfgh123#$%                     | ⚠️ Returns answer (low relevance)|

---

## 📊 Architecture & Flow

1. PDF → split into 87 chunks using LangChain
2. Chunks → embedded using MiniLM
3. Stored in FAISS index
4. At runtime:
   - Top chunks retrieved via similarity
   - Combined with question to form a prompt
   - Sent to Mistral‑7B via OpenRouter
   - Response streamed token-by-token
   - Source chunks shown below answer

---

## ✅ Requirements Covered from AI Task

- ✅ Document chunking and semantic search
- ✅ Answer generation using external model (OpenRouter)
- ✅ Streaming token display
- ✅ Reference to source chunks
- ✅ Blocking of invalid input
- ✅ Readme includes demo GIF and GitHub URL

---

## 👤 Author

**Rohit Garg**  
03 July 2025
