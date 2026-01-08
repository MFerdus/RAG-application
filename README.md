

markdown
# YouTube Chat Application using RAG (LangChain + Streamlit)

This project implements a **Retrieval-Augmented Generation (RAG)** system that allows users to **chat with any YouTube video**.  
By leveraging **LangChain**, **OpenAI embeddings**, **FAISS**, and a **Streamlit UI**, the system enables users to ask questions, get summaries, and extract insights from long YouTube videos without watching them end-to-end.

---

## 🚀 Key Features

- 🔗 Chat with **any YouTube video** using its transcript  
- 🧠 Retrieval-Augmented Generation (RAG) architecture  
- 📄 Automatic transcript extraction from YouTube  
- ✂️ Smart text chunking with overlap  
- 📊 Vector search using FAISS  
- 🤖 LLM-based grounded responses (no hallucinations)  
- 💬 Interactive Streamlit chat interface  
- 🌐 Supports multiple transcript languages (e.g., English, Hindi)

---

## 🧠 How It Works (RAG Pipeline)

The system follows a standard **RAG workflow**:

### 1️⃣ Indexing
- Fetch YouTube transcript using `YouTubeTranscriptApi`
- Split transcript into overlapping chunks
- Generate embeddings using OpenAI
- Store embeddings in a FAISS vector database

### 2️⃣ Retrieval
- Convert user query into an embedding
- Perform similarity search on FAISS
- Retrieve top-K most relevant transcript chunks

### 3️⃣ Augmentation
- Merge retrieved context with user question
- Construct a prompt grounded strictly in transcript data

### 4️⃣ Generation
- LLM generates a response **only using retrieved context**
- If context is insufficient, the model responds with *“I don’t know”*

---

## 📁 Project Structure

```

youtube-rag-streamlit/
├── app.py               # Streamlit UI (user interaction & chat)
├── rag.py               # RAG pipeline (transcript, embeddings, retrieval)
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
└── .env.example         # Environment variable template

````

---

## 🛠️ Tech Stack

- **Python**
- **LangChain**
- **OpenAI (LLM + Embeddings)**
- **FAISS (Vector Store)**
- **Streamlit (UI)**
- **YouTubeTranscriptApi**

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/youtube-rag-streamlit.git
cd youtube-rag-streamlit
````

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate:

* **Windows**

```bash
venv\Scripts\activate
```

* **Mac / Linux**

```bash
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 OpenAI API Key Setup

Create a `.env` file using `.env.example`:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Or set it directly:

**Windows**

```powershell
setx OPENAI_API_KEY "your_openai_api_key_here"
```

**Mac / Linux**

```bash
export OPENAI_API_KEY="your_openai_api_key_here"
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

Open your browser at:

```
http://localhost:8501
```

---

## 🧪 How to Use

1. Paste a **YouTube URL or Video ID**
2. Select transcript language (e.g., `en`, `hi`)
3. Click **Build Index**
4. Start chatting with the video:

   * “Summarize this video”
   * “Is AI discussed here?”
   * “What does the speaker say about nuclear fusion?”

---

## 📌 Example Use Cases

* 🎧 Chat with long podcasts
* 🎓 Ask questions about recorded lectures
* 📚 Generate summaries from educational videos
* 🔍 Extract specific insights without watching full videos

---



---













































