# app.py
import streamlit as st
from ai_chatbot import get_ai_response
from chat_manager import ChatManager

st.set_page_config(page_title="AIML Chatbot", page_icon="🤖")
st.title("AI Chatbot")

mode = st.sidebar.selectbox(
    "Select Mode",
    ["General", "DSA Tutor", "PDF Q&A"]
)

if st.sidebar.button("Clear Chat 🗑️"):
    st.session_state.chat_manager.messages = []
    st.session_state.chat_manager.save_messages()
    st.rerun()

if "chat_manager" not in st.session_state:
    st.session_state.chat_manager = ChatManager()

for msg in st.session_state.chat_manager.messages[-10:]:
    avatar = "🧑‍💻" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

if len(st.session_state.chat_manager.messages) == 0:
    st.info("👋 Welcome! Select a mode from the sidebar and say hello to get started.", icon="ℹ️")

if prompt := st.chat_input("What is on your mind?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.chat_manager.add_message("user", prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            history = st.session_state.chat_manager.messages
            response = get_ai_response(history, mode)
            if response.startswith("Error:"):
                st.error('API connection failed. Please try again.', icon="🚨")
            else:
                st.markdown(response)
    
    st.session_state.chat_manager.add_message("assistant", response)
