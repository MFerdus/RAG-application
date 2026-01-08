# 🎥 YouTube RAG Chat (Streamlit + LangChain)

Chat with any YouTube video using **RAG (Retrieval-Augmented Generation)**:

1) Fetch transcript (via `youtube-transcript-api`)  
2) Split transcript into chunks  
3) Create embeddings + store in **FAISS**  
4) Retrieve top-k relevant chunks for each question  
5) Use an OpenAI chat model to answer **grounded in the transcript**

---

## ✅ Features
- Paste **YouTube URL or Video ID**
- Transcript language fallback (e.g., `en,hi`)
- Adjustable chunk size / overlap
- Adjustable retriever **top-k**
- Choose embedding + chat model
- Streamlit chat UI with history

---

## 📁 Structure
```
youtube_rag_streamlit/
├─ app.py
├─ rag.py
├─ requirements.txt
├─ .env.example
└─ README.md
```

---

## 🚀 Run

### 1) Create & activate venv
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate
```

### 2) Install
```bash
pip install -r requirements.txt
```

### 3) Add API key
```bash
cp .env.example .env
```

Edit `.env`:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 4) Start Streamlit
```bash
streamlit run app.py
```

---

## 🧠 Notes / Tips
- If transcript isn’t available in English, try `hi` (Hindi) or other languages in the sidebar.
- For production, consider: persistence of FAISS index, citations, evaluation (RAGAS/LangSmith), semantic chunking, reranking.
# RAG-application
