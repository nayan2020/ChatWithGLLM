"""
GPT Server Module

This module sets up a FastAPI server to handle chat requests. It integrates with a FAISS database
for storing and retrieving chat history and uses a generative AI model for generating responses.

Endpoints:
- POST /chat: Handle chat requests from the frontend.
- GET /health: Check the health of the server.

Dependencies:
- FastAPI
- uuid
- logging
- backend.utils.database
- backend.utils.messages
- backend.utils.logging_config
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uuid
import logging
from backend.utils.database import save_message_to_db, retrieve_similar_context, vector_db, genai_model
from backend.utils.messages import generate_messages
from backend.utils.logging_config import setup_logging  

# Initialize FastAPI app
app = FastAPI()

# Initialize logging
setup_logging()
logger = logging.getLogger(__name__)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your frontend's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# In-memory storage for session chat history
session_data = {}



@app.post("/chat")
async def chat(request: Request):
    """Handle chat requests from the frontend."""
    try:
        data = await request.json()
        session_id = data.get("session_id") or str(uuid.uuid4())
        user_input = data.get("user_input")

        if not user_input:
            logger.error("Missing user_input.")
            raise HTTPException(status_code=400, detail="Missing user_input.")

        # Initialize session if it doesn't exist
        if session_id not in session_data:
            session_data[session_id] = []

        # Save user input to session and database
        session_data[session_id].append(("human", user_input))
        save_message_to_db(vector_db, session_id, "human", user_input)

        # Retrieve similar context and structure the conversation
        similar_context = retrieve_similar_context(vector_db, session_id, user_input)
        messages = generate_messages(similar_context, session_data[session_id])

        # Get AI response
        ai_response = genai_model.invoke(messages).content

        # Save AI response and persist to the database
        session_data[session_id].append(("assistant", ai_response))
        save_message_to_db(vector_db, session_id, "assistant", ai_response)

        # Return the AI's response
        return {"session_id": session_id, "response": ai_response}

    except ValueError as ve:
        logger.error(f"ValueError: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except HTTPException as he:
        logger.error(f"HTTPException: {str(he)}")
        raise he
    except RuntimeError as re:
        logger.error(f"RuntimeError: {str(re)}")
        raise HTTPException(status_code=500, detail=str(re))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.get("/health", response_class=JSONResponse)
async def health_check() -> JSONResponse:
    """Check the health of the server."""
    try:
        # Check database connection
        db_status = "ok" if vector_db else "failed"
        
        # Check model status
        model_status = "ok" if genai_model else "not ready"
        
        # Prepare health status
        health_status = {
            "status": "ok",
            "database_connection": db_status,
            "model_status": model_status,
            "session_count": len(session_data)
        }
        
        # Log health status
        logger.info(f"Health check status: {health_status}")
        
        return JSONResponse(content=health_status)
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "failed",
                "error": str(e),
                "database_connection": "unknown",
                "model_status": "unknown",
                "session_count": len(session_data)
            }
        )
    
