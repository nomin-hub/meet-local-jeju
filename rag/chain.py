"""RAG answer chain for JEJU-KB.

Combines `rag.retriever.retrieve_relevant_documents` with an OpenAI chat model to
answer traveler questions using only retrieved JEJU-KB context. This module owns
prompting and answer generation only — retrieval lives in `rag/retriever.py`, and
the Streamlit UI is not implemented here.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

# Allow `python3 rag/chain.py` to resolve `rag.retriever` even though running the
# file directly does not put the project root on sys.path.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from rag.retriever import retrieve_relevant_documents

DEFAULT_CHAT_MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """\
You are the Meet Local Jeju AI assistant. You help international travelers \
discover authentic local experiences, culture, seasonal activities, and stories \
about Jeju Island, Korea — not just generic tourist attractions.

You must answer strictly using the JEJU-KB CONTEXT provided in the user message. \
Do not use outside knowledge about Jeju beyond that context.

Rules you must always follow:
- Answer in clear, helpful English.
- Focus on authentic local Jeju experiences, culture, and seasonal context over \
generic tourist attractions.
- If the context does not fully answer the question, say so plainly rather than \
guessing. Clearly mention what is uncertain or not available in JEJU-KB.
- Never invent exact prices, schedules, addresses, phone numbers, or named \
individuals. If the context does not include these specifics, say they are not \
available in JEJU-KB and should be confirmed locally.
- Recommend specific local experiences from the context when appropriate.
- When you use information from a source, cite it inline using its document \
title and ID in parentheses, e.g. ("Voices from the Sea: A Haenyeo's Daily \
Dive", STORY-0001).
"""

USER_PROMPT_TEMPLATE = """\
JEJU-KB CONTEXT:
{context}

QUESTION:
{query}

Answer the question using only the JEJU-KB CONTEXT above, following the rules \
in your system instructions.
"""


def get_chat_model(model: str = DEFAULT_CHAT_MODEL) -> ChatOpenAI:
    """Return the OpenAI chat model used to generate grounded answers.

    Loads environment variables via python-dotenv (so a project-root `.env` file
    is picked up) and reads the API key from `OPENAI_API_KEY`.

    Args:
        model: OpenAI chat model name. Defaults to `gpt-4o-mini`.

    Returns:
        A configured `ChatOpenAI` instance with a low temperature, favoring
        grounded, consistent answers over creative variation.

    Raises:
        RuntimeError: if `OPENAI_API_KEY` is not set in the environment or `.env`.
    """
    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Add it to a .env file at the project root "
            "(see .env.example) or export it in your environment before running "
            "this module."
        )
    return ChatOpenAI(model=model, api_key=api_key, temperature=0.2)


def format_context(documents: list[Document]) -> str:
    """Format retrieved chunks into a numbered context block for the prompt.

    Each block includes the source's KDS `id`, `title`, `category`, and the
    chunk's `page_content`, giving the model everything it needs to answer and
    to cite sources correctly.

    Args:
        documents: Retrieved chunks, typically from
            `rag.retriever.retrieve_relevant_documents`.

    Returns:
        A formatted string with one block per document, or a placeholder string
        if `documents` is empty.
    """
    if not documents:
        return "(no relevant JEJU-KB context found)"

    blocks: list[str] = []
    for rank, document in enumerate(documents, start=1):
        meta = document.metadata
        blocks.append(
            f"[Source {rank}]\n"
            f"ID: {meta.get('id')}\n"
            f"Title: {meta.get('title')}\n"
            f"Category: {meta.get('category')}\n"
            f"Content: {document.page_content}"
        )
    return "\n\n".join(blocks)


def _document_to_source(document: Document) -> dict[str, Any]:
    """Build a plain source dict from a retrieved chunk's metadata."""
    meta = document.metadata
    return {
        "id": meta.get("id"),
        "title": meta.get("title"),
        "category": meta.get("category"),
        "chunk_id": meta.get("chunk_id"),
        "file_path": meta.get("file_path"),
    }


def answer_question(query: str, k: int = 4) -> dict[str, Any]:
    """Answer a traveler's question, grounded only in retrieved JEJU-KB context.

    Retrieves the top-k most relevant JEJU-KB chunks for `query`, assembles them
    into a context block, and asks the chat model to answer strictly from that
    context, per `SYSTEM_PROMPT`.

    Args:
        query: The traveler's natural-language question.
        k: Number of chunks to retrieve as context. Defaults to 4.

    Returns:
        A dict with:
          - `answer` (str): the model's grounded answer.
          - `sources` (list[dict]): one entry per retrieved chunk, each with
            `id`, `title`, `category`, `chunk_id`, and `file_path`.
          - `retrieved_documents` (list[Document]): the raw retrieved chunks.
    """
    retrieved_documents = retrieve_relevant_documents(query, k=k)
    context = format_context(retrieved_documents)

    chat_model = get_chat_model()
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=USER_PROMPT_TEMPLATE.format(context=context, query=query)),
    ]
    response = chat_model.invoke(messages)

    return {
        "answer": response.content,
        "sources": [_document_to_source(doc) for doc in retrieved_documents],
        "retrieved_documents": retrieved_documents,
    }


if __name__ == "__main__":
    test_questions = [
        "I want to learn about haenyeo culture.",
        "What can I do in Jeju in October?",
        "I want to meet local people at a market.",
        "Tell me about Jeju stone walls.",
    ]

    for question in test_questions:
        result = answer_question(question)

        print(f"Question: {question}")
        print(f"Answer:\n{result['answer']}\n")
        print("Sources:")
        for source in result["sources"]:
            print(
                f"  - {source['id']} | {source['title']} | "
                f"{source['category']} | {source['chunk_id']} | {source['file_path']}"
            )
        print("\n" + "-" * 80 + "\n")
