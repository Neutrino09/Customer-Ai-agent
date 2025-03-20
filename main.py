import streamlit as st
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "b7bb2eeb-2c8d-4c57-9cab-56385f398e13"
FLOW_ID = "5c1b755c-1a30-4eb5-ba4e-898eee743920"
APPLICATION_TOKEN = "AstraCS:zQNvAyIEPtvRuDtcJpClOHPC:cbdc4ca5efd3cd88680a5267321e73e86c4be75116c0bcc0566db9cced70c5e7"
ENDPOINT = "customer"  # The endpoint name of the flow

def run_flow(message: str) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"
    
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    
    # Debug: Print the token to ensure it is not None
    print("APPLICATION_TOKEN:", APPLICATION_TOKEN)
    
    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    
    # Debug: Check response before decoding JSON
    print("Status code:", response.status_code)
    print("Response text:", response.text)
    
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        return {
            "error": "Invalid JSON response",
            "status_code": response.status_code,
            "response": response.text,
        }

def main():
    # Set up page config
    st.set_page_config(page_title="Customer Agent Chat", page_icon="🤖", layout="wide")
    
    st.title("🤖 Customer Agent Chat")
    st.markdown("Welcome! Type your message below and get a response from our agent.")
    
    # Sidebar with instructions
    st.sidebar.header("Instructions")
    st.sidebar.write(
        "1. Enter your message in the text box and click **Send**.\n"
        "2. Your conversation history will appear on the right.\n"
        "3. Enjoy chatting with our Customer Agent!"
    )
    
    # Initialize chat history in session_state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Layout: Two columns for input and chat history
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Send a Message")
        message = st.text_area("Your Message", placeholder="Type your query here...", height=150)
        if st.button("Send"):
            if not message.strip():
                st.error("Please enter a message.")
            else:
                with st.spinner("Sending your message..."):
                    response = run_flow(message)
                try:
                    # Extract agent's response
                    agent_response = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
                except Exception as e:
                    agent_response = f"Error processing response: {e}"
                
                # Save the conversation in session_state
                st.session_state.chat_history.append({"sender": "You", "message": message})
                st.session_state.chat_history.append({"sender": "Agent", "message": agent_response})
                st.success("Message sent!")
    
    with col2:
        st.subheader("Chat History")
        if st.session_state.chat_history:
            for chat in st.session_state.chat_history:
                if chat["sender"] == "You":
                    st.markdown(f"**You:** {chat['message']}")
                else:
                    st.markdown(f"**Agent:** {chat['message']}")
        else:
            st.info("No messages yet. Start the conversation!")
    
    st.markdown("---")
    st.markdown("Developed by [NICO](https://github.com/Neutrino09?tab=repositories)")

if __name__ == "__main__":
    main()
