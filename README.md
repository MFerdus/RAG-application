```markdown
# YouTube Chat with RAG (LangChain + Streamlit)

Chat with **any YouTube video** using a **Retrieval-Augmented Generation (RAG)** pipeline built with **LangChain** and a **Streamlit UI**.

This app:
- Fetches a YouTube video **transcript**
- Splits it into chunks
- Creates embeddings and stores them in a **vector database (FAISS)**
- Retrieves the most relevant transcript chunks for your question
- Uses an LLM to answer **only from the retrieved transcript context**

---

## 🚀 Features

- ✅ Paste a **YouTube URL** (or video ID)
- ✅ Choose transcript language (e.g., `en`, `hi`)
- ✅ Build an index (FAISS) from the transcript
- ✅ Ask questions like:
  - “Summarize this video in 5 bullet points”
  - “Is AI discussed in this video? If yes, what exactly?”
  - “What does the speaker say about nuclear fusion?”
- ✅ Shows retrieved context (optional/debug)
- ✅ Simple, clean **Streamlit Chat UI**

---

## 🧠 RAG Architecture (High-level)

The system follows the classic RAG steps:

### 1) Indexing
1. Load Transcript (YouTubeTranscriptApi)
2. Split into chunks (RecursiveCharacterTextSplitter)
3. Create embeddings (OpenAI Embeddings)
4. Store vectors in FAISS

### 2) Retrieval
- Convert your query to an embedding
- Search FAISS for the most similar transcript chunks

### 3) Augmentation
- Combine your question + retrieved transcript chunks into a prompt

### 4) Generation
- LLM generates an answer grounded in transcript context

---

## 📁 Project Structure

```

youtube-rag-streamlit/
├── app.py               # Streamlit UI (chat + controls)
├── rag.py               # RAG pipeline: transcript -> chunks -> FAISS -> chain
├── requirements.txt     # Dependencies
├── README.md            # Documentation
└── .env.example         # Example env file

````

---

## ✅ Requirements

- Python **3.9+** (recommended 3.10+)
- An OpenAI API key
- Internet connection (to fetch transcript)

---

## 🔐 Setup: OpenAI API Key

### Option A (Recommended): Using `.env`
1. Copy `.env.example` → `.env`
2. Put your key inside:

```bash
OPENAI_API_KEY=your_openai_key_here
````

### Option B: Set key in terminal

**Windows (PowerShell):**

```powershell
setx OPENAI_API_KEY "your_openai_key_here"
```

**Mac/Linux:**

```bash
export OPENAI_API_KEY="your_openai_key_here"
```

---

## 🛠️ Installation

### 1) Unzip the project

```bash
unzip youtube-rag-streamlit.zip
cd youtube-rag-streamlit
```

### 2) Create and activate a virtual environment (recommended)

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Streamlit App

```bash
streamlit run app.py
```

Then open the local URL shown (usually):

* [http://localhost:8501](http://localhost:8501)

---

## 🧪 How to Use

### Step 1: Paste YouTube Link

Example:

* `https://www.youtube.com/watch?v=dQw4w9WgXcQ`

or just the ID:

* `dQw4w9WgXcQ`

### Step 2: Choose Language

* English: `en`
* Hindi: `hi`

If the transcript is not available in `en`, switch to `hi`.

### Step 3: Click "Build Index"

This will:

* download transcript
* chunk it
* embed chunks
* store them in FAISS

### Step 4: Chat!

Ask questions in the chat input.

---

## ⚙️ Configuration Options

In the UI you can control:

* **Chunk Size** (default ~1000)
* **Chunk Overlap** (default ~200)
* **Top-K retrieval** (default 4)

**What these mean:**

* Larger chunks: fewer pieces, but may lose precision
* Smaller chunks: better retrieval precision but more embeddings (cost/time)
* Overlap: helps preserve continuity between chunks

---

## 🧩 Transcript Notes & Common Issues

### 1) Transcript not available

Some videos:

* have no captions
* have disabled transcripts
* have auto-generated captions only in certain languages

Solution:

* try another language (`hi`)
* try another video
* verify captions exist on YouTube

### 2) Long videos

2–3 hour podcasts create many chunks.
Solutions:

* increase chunk size (e.g., 1200–1500)
* reduce top_k
* optionally store FAISS index on disk (future improvement)

### 3) Answers hallucinating

RAG reduces hallucinations, but you must enforce grounding.

This app prompt tells the model:

* **answer only using transcript context**
* if context is insufficient, say **"I don't know"**

---

## 🧠 Example Questions

Try these:

* “Summarize the entire video in 5 bullet points.”
* “What is the main argument of the speaker?”
* “Does the speaker mention AI? What is said?”
* “What does the speaker say about nuclear fusion?”
* “What are the key takeaways?”

---

## 🔍 How This Project Works (Code Overview)

### `rag.py`

Contains:

* `get_video_id(url_or_id)`
* `fetch_transcript(video_id, language)`
* `split_text(transcript)`
* `build_vectorstore(chunks)`
* `build_rag_chain(vectorstore)`

### `app.py`

* Streamlit UI for:

  * input URL/ID
  * selecting language
  * building the index
  * chatting with the RAG chain
* Stores vectorstore and chain in `st.session_state`

---

## ✅ Recommended Improvements (Next Steps)

If you want an industry-grade project, you can extend it with:

### UI Enhancements

* show YouTube video embedded
* chat history panel
* download transcript button

### RAG Improvements

* Hybrid retrieval (semantic + keyword)
* MMR search
* Reranking with cross-encoder
* Contextual compression
* Multi-query expansion

### Evaluation

* RAGAS evaluation metrics:

  * faithfulness
  * context precision/recall
  * answer relevancy
* LangSmith tracing

### Storage

* Save FAISS index to disk
* Cache transcript and embeddings per video

### Advanced RAG

* Agentic RAG (allow web browsing/tools)
* Memory-based RAG (personalized chat history)

---

## 🧾 Troubleshooting

### Problem: `ModuleNotFoundError`

Run:

```bash
pip install -r requirements.txt
```

### Problem: Transcript error

* Check captions on YouTube
* Try language `hi`
* Try another video





