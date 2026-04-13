import streamlit as st
from ai_chatbot import get_ai_response
from chat_manager import ChatManager

st.set_page_config(page_title="AIML Chatbot", page_icon="🤖")
st.title("AI Chatbot")

if "chat_manager" not in st.session_state:
    st.session_state.chat_manager = ChatManager()

for msg in st.session_state.chat_manager.messages[-10:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("What is on your mind?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.chat_manager.add_message("user", prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            history = st.session_state.chat_manager.messages[-6:]
            response = get_ai_response(history)
            st.markdown(response)
    
    st.session_state.chat_manager.add_message("assistant", response)
