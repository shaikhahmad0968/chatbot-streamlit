#si_chstbot.py
from chat_manager import ChatManager
import requests
import streamlit as st

API_KEY = st.secrets["API_KEY"]
# Use the correct OpenAI compatibility endpoint
URL = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"

def get_system_prompt(mode):
    if mode == "DSA Tutor":
        return "You are a DSA tutor. Explain step-by-step with examples."
    elif mode == "PDF Q&A":
        return "You answer only from provided document context."
    else:
        return "You are a helpful assistant. Be concise."
    
def summarize_messages(messages):
    if len(messages) <= 6:
        return ""

    old_msgs = messages[:-5]
    text = "\n".join([m["content"] for m in old_msgs])

    prompt = f"Summarize this conversation in 3-4 lines:\n{text}"

    summary = get_ai_response([
        {"role": "user", "content": prompt}
    ])

    return summary

def get_ai_response(history, mode="General"):

    system_instruction ={
        "role": "system",
        "content": get_system_prompt(mode)
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    summary = summarize_messages(history)

    final_messages = []
    if summary:
        final_messages.append({
            "role": "system",
            "content": f"Conversation summary: {summary}"
        })
    
    # Get the latest 5 messages
    recent_history = history[-5:]
    api_messages = [{"role": m["role"], "content": m["content"]} for m in recent_history]
    
    # Combine the main system prompt, the summary (if any), and recent history
    final_payload = [system_instruction] + final_messages + api_messages

    data = {
        "model": "gemini-2.5-flash-lite",
        "messages": final_payload
    }
    response = requests.post(URL, headers=headers, json=data)
    if response.status_code !=200:
        return f"Error: {response.status_code} - {response.text}"
    
    result = response.json()
    return result["choices"][0]["message"]["content"]

if __name__ == "__main__":
    chat = ChatManager()
    print("--- Chat Started (type 'exit' to stop) ---")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        chat.add_message("user", user_input)
        ai_reply = get_ai_response(chat.messages)
        chat.add_message("assistant", ai_reply)
        print("-" * 30)
        chat.show_messages()
        print("-" * 30)