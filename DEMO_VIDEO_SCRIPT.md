# Demo Video Script

Use this script for your 1–2 minute demo video.

## 1. Introduction

Hello everyone, this is my Task 3 project for the VedGrow Generative AI Internship.

The task is **Document Q&A with RAG**, where a user can upload a PDF and ask questions based on that document.

## 2. GitHub Repository

This is my GitHub repository named:

```text
VedGrow_GAI_03
```

It contains the main Streamlit application file, requirements file, README, deployment guide, and sample questions.

## 3. App Overview

This is the Streamlit web app.

The app allows the user to upload a PDF document. After upload, the system extracts text from the PDF, splits the text into chunks, generates embeddings, and stores them in a FAISS vector database.

## 4. RAG Workflow

The workflow is:

1. Upload PDF
2. Extract text
3. Chunk text
4. Generate embeddings
5. Store embeddings in FAISS
6. Retrieve relevant chunks using semantic search
7. Generate an answer using Gemini based on the retrieved context

## 5. Demo

Now I will upload a PDF.

The app has processed the PDF and created text chunks.

Now I will ask a question:

```text
What is this document about?
```

The chatbot retrieves relevant chunks and generates an answer from the document.

Now I will ask another question:

```text
Summarize the main points of the document.
```

The chatbot again answers based on the uploaded PDF.

## 6. Retrieved Context

The app also shows the retrieved context chunks, which helps us understand what information was used to generate the answer.

## 7. Conclusion

This project helped me understand Retrieval Augmented Generation, PDF processing, embeddings, vector databases, semantic search, FAISS, Gemini API integration, and Streamlit web app development.

Thank you.
