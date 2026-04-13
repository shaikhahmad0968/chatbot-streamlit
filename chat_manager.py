import json
import datetime
class ChatManager:
    def __init__(self, file_name="chat.json"):
        self.file_name = file_name
        self.messages = self.load_messages()
    
    def load_messages(self):
        try:
            with open(self.file_name, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def save_messages(self):
        with open(self.file_name, "w") as file:
            json.dump(self.messages, file, indent=4)
    
    def add_message(self, role, content):
        new_msg = {
            "role": role,
            "content": content,
            "time": datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S")
        }
        self.messages.append(new_msg)
        self.save_messages()

    def show_messages(self):
        for msg in self.messages[-6:]:
            role_label = "You" if msg['role'] == "user" else "Gemini"
            print(f"[{msg['time']}] {role_label} : {msg['content']}")

def run_chat():
    chat = ChatManager()

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        chat.add_message("user", user_input)
        chat.add_message("assistant", "This is bot's reply")
        chat.show_messages()
if __name__ == "__main__":
    run_chat()