# Chatbot Application

This is a chatbot application using Google Generative AI and FastAPI for the backend. The frontend is built using Streamlit.

## Setup

1. Install dependencies:
   - For backend: `pip install -r backend/requirements.txt`
   - For frontend: `pip install -r frontend/requirements.txt`

2. Create a `.env` file with the following content:

3. Run the application:
- Backend: `uvicorn backend.gpt_server:app --reload`
- Frontend: `streamlit run frontend/app.py`

4. Access the chatbot at [http://localhost:8501](http://localhost:8501).

## Docker

To run the application using Docker:

1. Build the services:
```bash
docker-compose build
docker-compose up

---

This structure ensures clarity and maintainability, as well as easy deployment with Docker. Let me know if you need further explanations or adjustments!

## Advance USER
`uvicorn backend.gpt_server:app --host 0.0.0.0 --port 8080 --reload'

.
├── backend
│   ├── gpt_server.py             # Main FastAPI server
│   ├── utils
│   │   ├── database.py           # Handles FAISS database interactions
│   │   ├── messages.py           # Processes and structures chat messages
│   │   ├── logging_config.py     # Configures backend logging
|   |   ├──config.py              # Configures backend .env and db path
│   ├── requirements.txt          # Backend dependencies
│   ├── faiss_db/                 # FAISS database storage
│
├── frontend
│   ├── app.py                    # Streamlit frontend interface
│   ├── requirements.txt          # Frontend dependencies
│
├── docker-compose.yml            # Docker Compose for backend and frontend
├── .env                          # Environment variables (API keys)
├── .gitignore                    # Ignore sensitive/unnecessary files
├── README.md                     # Project documentation
