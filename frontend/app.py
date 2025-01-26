import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000/chat"

def chat_with_ai(session_id, user_input):
    """Send user input to the backend and get the response."""
    payload = {
        "session_id": session_id,
        "user_input": user_input
    }
    try:
        response = requests.post(BACKEND_URL, json=payload)
        response.raise_for_status()
        return response.json().get("response", "No response field in the server reply.")
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def main():
    """Streamlit UI for interacting with the chatbot."""
    st.title("Chat with AI")

    session_id = st.text_input("Session ID", "")
    user_input = st.text_input("You: ", "")

    if st.button("Send"):
        if not session_id:
            st.error("Session ID is required!")
        elif user_input:
            ai_response = chat_with_ai(session_id, user_input)
            st.write(f"**AI:** {ai_response}")
        else:
            st.error("Please enter a message.")

if __name__ == "__main__":
    main()
