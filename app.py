import os
import re
import streamlit as st
from dotenv import load_dotenv

from rag import build_vectorstore_from_youtube, build_rag_chain

load_dotenv()

st.set_page_config(page_title="YouTube RAG Chat (LangChain)", page_icon="🎥", layout="wide")

st.title("🎥 Chat with a YouTube Video (RAG + LangChain)")
st.caption("Paste a YouTube URL or video ID → fetch transcript → embed → retrieve → answer grounded in transcript.")

with st.sidebar:
    st.header("Settings")

    openai_key = st.text_input(
        "OpenAI API Key",
        value=os.getenv("OPENAI_API_KEY", ""),
        type="password",
        help="Stored only in this session. Prefer using .env locally."
    )

    st.subheader("Transcript")
    lang = st.text_input("Transcript language codes (comma-separated)", value="en,hi", help="Try: en, hi, bn, etc.")

    st.subheader("Chunking")
    chunk_size = st.slider("Chunk size", 300, 2000, 1000, 50)
    chunk_overlap = st.slider("Chunk overlap", 0, 500, 200, 10)

    st.subheader("Retrieval")
    top_k = st.slider("Top-k retrieved chunks", 1, 10, 4, 1)

    st.subheader("Models")
    embedding_model = st.selectbox(
        "Embedding model",
        options=["text-embedding-3-small", "text-embedding-3-large"],
        index=0
    )
    chat_model = st.selectbox(
        "Chat model",
        options=["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini"],
        index=0
    )
    temperature = st.slider("Temperature", 0.0, 1.0, 0.0, 0.05)

    st.divider()
    st.write("Tip: First run may take time because it embeds the transcript.")

video_input = st.text_input("YouTube URL or Video ID", placeholder="https://www.youtube.com/watch?v=dQw4w9WgXcQ")

col1, col2 = st.columns([1, 1])
with col1:
    build_btn = st.button("📥 Load + Index Transcript", type="primary", use_container_width=True)
with col2:
    clear_btn = st.button("🧹 Clear Session", use_container_width=True)

if clear_btn:
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.success("Cleared session state. Rebuild the index to continue.")
    st.stop()

def extract_video_id(url_or_id: str) -> str:
    s = (url_or_id or "").strip()
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", s):
        return s
    patterns = [
        r"v=([A-Za-z0-9_-]{11})",
        r"youtu\.be/([A-Za-z0-9_-]{11})",
        r"shorts/([A-Za-z0-9_-]{11})",
        r"embed/([A-Za-z0-9_-]{11})",
    ]
    for p in patterns:
        m = re.search(p, s)
        if m:
            return m.group(1)
    raise ValueError("Could not extract video id. Paste a valid YouTube URL or the 11-character video id.")

@st.cache_resource(show_spinner=False)
def cached_build_vectorstore(video_id: str, languages: tuple, chunk_size: int, chunk_overlap: int, embedding_model: str, api_key: str):
    return build_vectorstore_from_youtube(
        video_id=video_id,
        languages=languages,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        embedding_model=embedding_model,
        openai_api_key=api_key
    )

if build_btn:
    if not openai_key:
        st.error("Please provide your OpenAI API key (sidebar).")
        st.stop()
    if not video_input:
        st.error("Please paste a YouTube URL or video ID.")
        st.stop()

    try:
        video_id = extract_video_id(video_input)
    except Exception as e:
        st.error(str(e))
        st.stop()

    languages = tuple([x.strip() for x in lang.split(",") if x.strip()]) or ("en",)

    with st.spinner("Fetching transcript, splitting, embedding, and building FAISS index..."):
        try:
            vectorstore, meta = cached_build_vectorstore(
                video_id=video_id,
                languages=languages,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                embedding_model=embedding_model,
                api_key=openai_key
            )
        except Exception as e:
            st.error(f"Failed to build index: {e}")
            st.stop()

    st.session_state["video_id"] = video_id
    st.session_state["vectorstore"] = vectorstore
    st.session_state["meta"] = meta
    st.success(f"Index ready ✅  | chunks: {meta['num_chunks']}  | transcript chars: {meta['transcript_chars']}")

if "vectorstore" in st.session_state:
    meta = st.session_state.get("meta", {})
    with st.expander("📄 Transcript / Index details", expanded=False):
        st.json(meta)

    rag_chain = build_rag_chain(
        vectorstore=st.session_state["vectorstore"],
        chat_model=chat_model,
        temperature=temperature,
        k=top_k,
        openai_api_key=openai_key
    )

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    for m in st.session_state["messages"]:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    user_q = st.chat_input("Ask a question about the video...")
    if user_q:
        st.session_state["messages"].append({"role": "user", "content": user_q})
        with st.chat_message("user"):
            st.markdown(user_q)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    answer = rag_chain.invoke(user_q)
                except Exception as e:
                    answer = f"Error: {e}"
            st.markdown(answer)

        st.session_state["messages"].append({"role": "assistant", "content": answer})
else:
    st.info("Click **Load + Index Transcript** to start. Then you can chat with the video.")
