from chat_manager import ChatManager
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
# Use the correct OpenAI compatibility endpoint
URL = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"

def get_ai_response(history):

    system_instruction ={
        "role": "system",
        "content": "You are small AI assistant, be concise."
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    recent_history = history[-4:]

    api_messages = [{"role": m["role"], "content": m["content"]} for m in recent_history]
    final_payload =[system_instruction] + api_messages

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