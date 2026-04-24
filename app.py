import streamlit as st
import os
import json
from groq import Groq
from dotenv import load_dotenv

# 1. Configuration
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
HISTORY_FILE = "chat_history.json"

# --- HISTORY LOGIC ---
def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                content = f.read()
                if not content: # Agar file khali hai
                    return []
                return json.loads(content)
        except Exception as e:
            print(f"Error loading file: {e}")
            return []
    return []

def save_history(messages):
    with open(HISTORY_FILE, "w") as f:
        json.dump(messages, f, indent=4)

# 2. Page Setup
st.set_page_config(page_title="AQS Agent", page_icon="🤖")
st.title("🤖 AQS Agent")

# 3. Force Load History into Session State
# Ye check karega ke agar messages khali hain ya pehli baar load ho rahe hain
if "messages" not in st.session_state or not st.session_state.messages:
    saved_data = load_history()
    if saved_data:
        st.session_state.messages = saved_data
    else:
        st.session_state.messages = []

# 4. Sidebar
with st.sidebar:
    st.subheader("Menu")
    if st.button("➕ New Chat"):
        st.session_state.messages = []
        save_history([])
        st.rerun()

# 5. Display ALL Messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Chat Logic
if prompt := st.chat_input("Type your message here..."):
    # Add User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI Response
    with st.chat_message("assistant"):
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Your name is AQS Agent. Respond only in English."},
                    *st.session_state.messages
                ]
            )
            response_text = completion.choices[0].message.content
            st.markdown(response_text)
            
            # Save Assistant Message
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            save_history(st.session_state.messages)
            
        except Exception as e:
            st.error(f"Error: {e}")