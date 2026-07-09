# Project Context

## Identity

Meet Local Jeju / Jejumate is a RAG-powered mobile-style local experience discovery MVP for Jeju.

The app helps foreign travelers, international students, digital nomads, and workation visitors discover local Jeju culture beyond famous attractions.

## Product Direction

The prototype should feel like:

- Pinterest
- Airbnb-style discovery
- Local lifestyle magazine
- Mobile-first travel app
- Friendly AI local concierge

It should not feel like:

- Plain Streamlit dashboard
- Table-based data viewer
- Generic search app
- Fake class demo

## Current Core

The project already includes:

- Streamlit app
- RAG chat mode
- Experience recommendation mode
- Structured JEJU-KB knowledge base
- Chroma vector store pipeline
- JSON experience card dataset
- Mobile Pinterest-style UI prototype

## Long-Term Vision

The long-term direction is a trip planner and Airbnb-like local experience platform for authentic Jeju local experiences, stories, people, and potentially stays.

This MVP should remain honest: marketplace, booking, payment, real host onboarding, account login, and real save persistence are not built.

## Protected RAG Files

Do not modify unless explicitly requested:

- `rag/loader.py`
- `rag/splitter.py`
- `rag/vectordb.py`
- `rag/retriever.py`
- `rag/chain.py`

Do not replace the working RAG pipeline with mock logic.
