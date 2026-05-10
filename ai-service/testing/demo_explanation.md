# Demo Explanation — Day 20

This project is an AI-powered Compliance Calendar Tracker backend system developed using Flask, Groq API, ChromaDB, Redis caching, and Retrieval-Augmented Generation (RAG).

Flask is used to build REST APIs and manage backend operations. Groq API powers the AI-generated responses and report generation functionality. ChromaDB is used as a vector database to store embeddings and retrieve relevant compliance-related context using RAG architecture.

Redis caching improves performance by storing repeated responses temporarily, reducing repeated AI processing time. The project also includes async report generation, AI fallback handling, performance benchmarking, and health monitoring APIs.

The `/health` endpoint displays system status, uptime, cache statistics, and model information for monitoring backend health and performance.