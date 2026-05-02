# app.py
import streamlit as st
from ai_chatbot import get_ai_response, load_pdf, chunk_text, store_chunks, search_chunks
from chat_manager import ChatManager

st.set_page_config(page_title="AIML Chatbot", page_icon="🤖")
st.title("AI Study Assistant 🤖")
st.caption("Chat, learn DSA, or ask questions from PDFs")

mode = st.sidebar.selectbox(
    "Select Mode",
    ["General", "DSA Tutor", "PDF Q&A"]
)

uploaded_file = None
if mode == "PDF Q&A":
    uploaded_file = st.sidebar.file_uploader("Upload PDF 📄", type="pdf")

    if uploaded_file and st.sidebar.button("Process PDF"):
        with st.spinner("Processing PDF..."):
            text = load_pdf(uploaded_file)
            chunks = chunk_text(text)
            store_chunks(chunks)
            st.sidebar.success("PDF Processed! You can now ask questions.")

if st.sidebar.button("Clear Chat 🗑️"):
    st.session_state.chat_manager.messages = []
    st.session_state.chat_manager.save_messages()
    st.rerun()

if st.sidebar.button("Download Chat 📄"):
    chat_text = "\n".join(
        [f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.chat_manager.messages]
    )
    st.sidebar.download_button("Download", chat_text, file_name="chat.txt")

if "chat_manager" not in st.session_state:
    st.session_state.chat_manager = ChatManager()

for msg in st.session_state.chat_manager.messages[-10:]:
    avatar = "🧑‍💻" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

if len(st.session_state.chat_manager.messages) == 0:
    st.info("👋 Welcome! Select a mode from the sidebar and say hello to get started.", icon="ℹ️")

if prompt := st.chat_input("What is on your mind?"):
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)
    st.session_state.chat_manager.add_message("user", prompt)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            history = st.session_state.chat_manager.messages

            if mode == "PDF Q&A" and uploaded_file:
                context_chunks = search_chunks(prompt)
                if context_chunks:
                    context = "\n".join(context_chunks)
                    
                    temp_msg = dict(history[-1]) 
                    temp_msg["content"] = f"Answer based only on this context:\n{context}\n\nQuestion: {prompt}"
                    history = list(history)
                    history[-1] = temp_msg
            response = get_ai_response(history, mode)
            if response.startswith("Error:"):
                st.error('API connection failed. Please try again.', icon="🚨")
            else:
                st.markdown(response)
    
    st.session_state.chat_manager.add_message("assistant", response)
