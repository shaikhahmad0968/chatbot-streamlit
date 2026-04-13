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
        except FileNotFoundError:
            return []
    
    def save_messages(self):
        with open(self.file_name, "w") as file:
            json.dump(self.messages, file, indent=4)
    
    def add_message(self, user, message):
        new_msg = {
            "user": user,
            "message": message
        }
        self.messages.append(new_msg)
        self.save_messages()

    def show_messages(self):
        for msg in self.messages:
            print(f"{msg['user']} : {msg['message']}")

def run_chat():
    chat = ChatManager()

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        chat.add_message("You", user_input)
        chat.add_message("Bot", "This is bot's reply")
        chat.show_messages()
if __name__ == "__main__":
    run_chat()