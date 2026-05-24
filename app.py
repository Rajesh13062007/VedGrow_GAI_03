import os
from typing import List

import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

load_dotenv()

SYSTEM_PROMPT = """
You are a helpful Document Q&A assistant.

Rules:
- Answer only using the uploaded PDF context.
- If the answer is not found in the PDF, say:
  "I could not find this information in the uploaded document."
- Keep answers clear and beginner-friendly.
- Mention chunk numbers when useful.
- Do not make up facts that are not in the PDF.
"""


def get_secret(name: str, default: str = "") -> str:
    try:
        if name in st.secrets:
            return st.secrets[name]
    except Exception:
        pass
    return os.getenv(name, default)


def get_google_api_key() -> str:
    return get_secret("GOOGLE_API_KEY")


def get_chat_model_name() -> str:
    return get_secret("GEMINI_MODEL", "gemini-1.5-flash")


def get_embedding_model_name() -> str:
    return get_secret("GEMINI_EMBEDDING_MODEL", "models/embedding-001")


def extract_text_from_pdf(uploaded_file) -> str:
    """Extract text from uploaded PDF."""
    reader = PdfReader(uploaded_file)
    page_texts = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            page_texts.append(f"\n\n--- Page {page_number} ---\n{text}")

    return "\n".join(page_texts)


def create_chunks(text: str) -> List[Document]:
    """Split PDF text into chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    chunks = splitter.split_text(text)

    documents = []
    for index, chunk in enumerate(chunks, start=1):
        documents.append(
            Document(
                page_content=chunk,
                metadata={"chunk_id": index, "source": "uploaded_pdf"}
            )
        )

    return documents


def create_vector_store(documents: List[Document]) -> FAISS:
    """Create FAISS vector store using Gemini embeddings."""
    api_key = get_google_api_key()

    if not api_key:
        raise ValueError("GOOGLE_API_KEY is missing. Add it in Streamlit secrets or local .env file.")

    embeddings = GoogleGenerativeAIEmbeddings(
        model=get_embedding_model_name(),
        google_api_key=api_key
    )

    return FAISS.from_documents(documents, embeddings)


def retrieve_relevant_chunks(question: str, vector_store: FAISS, k: int = 4) -> List[Document]:
    """Retrieve relevant chunks from FAISS."""
    return vector_store.similarity_search(question, k=k)


def build_prompt(question: str, retrieved_docs: List[Document]) -> str:
    """Build a grounded RAG prompt."""
    context_parts = []

    for doc in retrieved_docs:
        chunk_id = doc.metadata.get("chunk_id", "unknown")
        context_parts.append(f"[Chunk {chunk_id}]\n{doc.page_content}")

    context = "\n\n".join(context_parts)

    return f"""
{SYSTEM_PROMPT}

Retrieved PDF Context:
{context}

User Question:
{question}

Answer:
"""


def generate_answer(question: str, retrieved_docs: List[Document]) -> str:
    """Generate answer using Gemini and retrieved context."""
    api_key = get_google_api_key()

    if not api_key:
        return "GOOGLE_API_KEY is missing. Add your Gemini API key in Streamlit secrets or local .env file."

    try:
        llm = ChatGoogleGenerativeAI(
            model=get_chat_model_name(),
            google_api_key=api_key,
            temperature=0.2
        )

        prompt = build_prompt(question, retrieved_docs)
        response = llm.invoke(prompt)
        return response.content

    except Exception as error:
        return f"Sorry, something went wrong while generating the answer: {error}"


st.set_page_config(
    page_title="Document Q&A with RAG",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Document Q&A with RAG")
st.caption("Task 3 | Generative AI Internship | PDF Upload + Chunking + Embeddings + FAISS + Gemini + Streamlit")

with st.sidebar:
    st.header("About this project")
    st.write(
        "Upload a PDF and ask questions about it. The app extracts text, chunks it, "
        "creates embeddings, stores them in FAISS, retrieves relevant chunks, "
        "and generates answers using Gemini."
    )

    st.subheader("Requirements Covered")
    st.markdown(
        """
        - Upload PDF
        - Extract text
        - Chunk text
        - Create embeddings
        - Store embeddings in FAISS
        - Semantic search
        - LLM answer using retrieved context
        - Streamlit upload + chat interface
        """
    )

    st.subheader("Model Settings")
    st.write(f"Chat model: `{get_chat_model_name()}`")
    st.write(f"Embedding model: `{get_embedding_model_name()}`")

    if st.button("Clear PDF and Chat"):
        st.session_state.clear()
        st.rerun()


if "messages" not in st.session_state:
    st.session_state.messages = []

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False

if "document_count" not in st.session_state:
    st.session_state.document_count = 0


uploaded_file = st.file_uploader(
    "Upload a PDF document",
    type=["pdf"],
    help="Upload a text-based PDF file."
)

if uploaded_file is not None and not st.session_state.pdf_processed:
    with st.spinner("Processing PDF... extracting text, chunking, embedding, and creating FAISS index."):
        try:
            extracted_text = extract_text_from_pdf(uploaded_file)

            if not extracted_text.strip():
                st.error("No readable text found. Try a text-based PDF instead of a scanned image PDF.")
            else:
                documents = create_chunks(extracted_text)
                vector_store = create_vector_store(documents)

                st.session_state.vector_store = vector_store
                st.session_state.pdf_processed = True
                st.session_state.document_count = len(documents)
                st.session_state.messages = []

                st.success(f"PDF processed successfully. Created {len(documents)} chunks.")

        except Exception as error:
            st.error(f"Error while processing PDF: {error}")


if st.session_state.pdf_processed:
    st.info(f"PDF is ready. Chunks stored in FAISS: {st.session_state.document_count}")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    question = st.chat_input("Ask a question about the uploaded PDF...")

    if question:
        st.session_state.messages.append({"role": "user", "content": question})

        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            with st.spinner("Retrieving chunks and generating answer..."):
                retrieved_docs = retrieve_relevant_chunks(
                    question,
                    st.session_state.vector_store,
                    k=4
                )

                answer = generate_answer(question, retrieved_docs)
                st.write(answer)

                with st.expander("View retrieved context chunks"):
                    for doc in retrieved_docs:
                        chunk_id = doc.metadata.get("chunk_id", "unknown")
                        st.markdown(f"### Chunk {chunk_id}")
                        st.write(doc.page_content[:1200])

        st.session_state.messages.append({"role": "assistant", "content": answer})
else:
    st.warning("Please upload a PDF to start asking questions.")

st.divider()
st.markdown(
    "**Note:** This app answers from the uploaded PDF only. If the PDF does not contain the answer, "
    "the chatbot should say that the information was not found in the document."
)
