"""
Database Module

This module initializes the FAISS database for storing and retrieving chat history.
It also sets up the generative AI model for generating responses.

Dependencies:
- logging
- os
- langchain_community.vectorstores.FAISS
- langchain_google_genai.GoogleGenerativeAIEmbeddings
- langchain_google_genai.ChatGoogleGenerativeAI
- langchain.schema.Document
- dotenv
- backend.utils.logging_config
- backend.utils.config

Functions:
- save_message_to_db: Save a message to the FAISS database.
- retrieve_similar_context: Retrieve context-relevant messages from the FAISS database.
"""
import logging
import os
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import Document
from backend.utils.logging_config import setup_logging  
from backend.utils.config import settings

# Initialize logging
setup_logging()
logger = logging.getLogger(__name__)

# Global variables for chatbot configuration
FAISS_DB_PATH = settings.faiss_db_path

# Initialize AI model
genai_model = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)


# Initialize embeddings
embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Ensure FAISS database directory exists
if not os.path.exists(FAISS_DB_PATH):
    os.makedirs(FAISS_DB_PATH)


try:
    # Check if the FAISS index file exists
    if os.path.exists(os.path.join(FAISS_DB_PATH, "index.faiss")):
        logger.info("Loading FAISS database from disk.")
        vector_db = FAISS.load_local(FAISS_DB_PATH, embeddings=embedding_function, allow_dangerous_deserialization=True)
    else:
        # Add a placeholder document to initialize the FAISS database
        logger.info("Creating a new FAISS database.")
        placeholder_doc = Document(page_content="Placeholder content", metadata={"role": "assistant", "session_id": "default"})
        vector_db = FAISS.from_documents([placeholder_doc], embedding_function)
        vector_db.save_local(FAISS_DB_PATH)  # Save the initial database
except Exception as e:
    logger.error(f"Failed to initialize FAISS database: {str(e)}")
    raise RuntimeError(f"Failed to initialize FAISS database: {str(e)}")


def save_message_to_db(db, session_id, role, content):
    """Save a message to the FAISS database."""
    doc = Document(page_content=content, metadata={"role": role, "session_id": session_id})
    db.add_documents([doc])

    db.save_local(FAISS_DB_PATH)

def retrieve_similar_context(db, session_id, user_input, num_results=5):
    """Retrieve context-relevant messages from the FAISS database."""
    docs = db.similarity_search(user_input, k=num_results)
    return [
        (doc.metadata["role"], doc.page_content)
        for doc in docs if doc.metadata.get("session_id") == session_id
    ]

