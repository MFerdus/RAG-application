from __future__ import annotations
import os
from typing import Tuple

from youtube_transcript_api import YouTubeTranscriptApi

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda


def fetch_transcript_text(video_id: str, languages: Tuple[str, ...]) -> str:
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=list(languages))
    return " ".join(item["text"] for item in transcript_list)


def build_vectorstore_from_youtube(
    video_id: str,
    languages: Tuple[str, ...] = ("en",),
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    embedding_model: str = "text-embedding-3-small",
    openai_api_key: str | None = None,
):
    if openai_api_key:
        os.environ["OPENAI_API_KEY"] = openai_api_key

    transcript_text = fetch_transcript_text(video_id, languages=languages)

    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_text(transcript_text)

    embeddings = OpenAIEmbeddings(model=embedding_model)
    vectorstore = FAISS.from_texts(chunks, embedding=embeddings)

    meta = {
        "video_id": video_id,
        "languages": list(languages),
        "chunk_size": chunk_size,
        "chunk_overlap": chunk_overlap,
        "embedding_model": embedding_model,
        "num_chunks": len(chunks),
        "transcript_chars": len(transcript_text),
    }
    return vectorstore, meta


def _format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)


def build_rag_chain(
    vectorstore: FAISS,
    chat_model: str = "gpt-4o-mini",
    temperature: float = 0.0,
    k: int = 4,
    openai_api_key: str | None = None,
):
    if openai_api_key:
        os.environ["OPENAI_API_KEY"] = openai_api_key

    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": k})

    prompt = ChatPromptTemplate.from_template(
        """You are a helpful assistant.
Answer ONLY from the provided transcript context.
If the context is insufficient, say "I don't know."

Transcript context:
{context}

Question:
{question}
"""
    )

    llm = ChatOpenAI(model=chat_model, temperature=temperature)
    parser = StrOutputParser()

    parallel_chain = RunnableParallel(
        {
            "context": retriever | RunnableLambda(_format_docs),
            "question": RunnablePassthrough(),
        }
    )

    return parallel_chain | prompt | llm | parser
