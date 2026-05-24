# Document Q&A with RAG

This repository contains **Task 3** for the VedGrow Generative AI Internship.

## Task Title

**Document Q&A with RAG**

## Objective

Build a Retrieval Augmented Generation system that answers questions from uploaded PDF documents.

## What is RAG?

RAG stands for **Retrieval Augmented Generation**. It improves an LLM response by retrieving relevant information from a document first, then asking the LLM to answer using that retrieved context.

## Features

| Requirement | Status |
|---|---|
| Upload PDF | Completed |
| Extract text from PDF | Completed |
| Chunk extracted text | Completed |
| Create embeddings | Completed using Gemini embeddings |
| Store embeddings | Completed using FAISS |
| Semantic search | Completed |
| LLM answer using retrieved context | Completed using Gemini |
| Simple web interface | Completed using Streamlit |
| Submit GitHub repo + demo video | Ready |

## Tools Used

- Python
- Streamlit
- LangChain
- Gemini API
- FAISS
- pypdf
- python-dotenv

## Project Structure

```text
VedGrow_GAI_03/
│
├── app.py
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── sample_questions.md
├── DEMO_VIDEO_SCRIPT.md
├── DEPLOYMENT.md
└── test_pdf_extract.py
```

## How the App Works

1. User uploads a PDF.
2. The app extracts text using `pypdf`.
3. The text is split into smaller chunks using LangChain.
4. Gemini embeddings are created for each chunk.
5. The embeddings are stored in a FAISS vector database.
6. When the user asks a question, semantic search retrieves relevant chunks.
7. Gemini generates an answer using only the retrieved PDF context.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/VedGrow_GAI_03.git
cd VedGrow_GAI_03
```

### 2. Install Required Packages

```bash
pip install -r requirements.txt
```

### 3. Create a `.env` File

Create a file named `.env` in the project folder.

```env
GOOGLE_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash
GEMINI_EMBEDDING_MODEL=models/gemini-embedding-001
```

Do not upload your real `.env` file to GitHub.

### 4. Run the App

```bash
streamlit run app.py
```

## Deployment

You can deploy this app on Streamlit Community Cloud.

Add these secrets in Streamlit:

```toml
GOOGLE_API_KEY = "your_gemini_api_key_here"
GEMINI_MODEL = "gemini-1.5-flash"
GEMINI_EMBEDDING_MODEL = "models/embedding-001"
```

## Demo Video Requirement

Record a short 1–2 minute demo video showing:

1. GitHub repository overview
2. Streamlit app opening
3. PDF upload
4. PDF processing
5. Asking 2–3 questions
6. Showing retrieved context chunks
7. Explaining that the app uses RAG with FAISS and Gemini

A script is included in `DEMO_VIDEO_SCRIPT.md`.

## Author

Rajesh A
