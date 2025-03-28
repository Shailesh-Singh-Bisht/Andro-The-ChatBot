import json
from difflib import get_close_matches
import tkinter as tk
from tkinter import scrolledtext, simpledialog, Menu
import webbrowser

class ChatBotUI:
    def __init__(self, knowledge_base_file="knowledge_base.json"):
        self.window = tk.Tk()
        self.window.title("Andro The Chatbot")
        self.window.geometry("900x600")
        self.window.configure(bg="#1e1e2f")

        # Title Label
        title_label = tk.Label(
            self.window,
            text="Andro The Chatbot",
            font=("Arial", 20, "bold"),
            fg="#f5a623",
            bg="#1e1e2f"
        )
        title_label.pack(pady=10)

        # Menu Bar
        menu_bar = Menu(self.window)
        self.window.config(menu=menu_bar)

        # Developer Menu
        developer_menu = Menu(menu_bar, tearoff=0)
        developer_menu.add_command(label="GitHub", command=lambda: self.open_website("https://github.com/Shailesh-Singh-Bisht"))
        developer_menu.add_command(label="LeetCode", command=lambda: self.open_website("https://leetcode.com/Shailesh_Singh_Bisht/"))
        developer_menu.add_command(label="Linkedin", command=lambda: self.open_website("https://www.linkedin.com/in/shailesh-singh-bisht-13b30b258/"))
        menu_bar.add_cascade(label="Developer", menu=developer_menu)

        # About Menu
        about_menu = Menu(menu_bar, tearoff=0)
        about_menu.add_command(label="About The App", command=self.show_about_app)
        about_menu.add_command(label="About The Developer", command=self.show_about_developer)
        menu_bar.add_cascade(label="About", menu=about_menu)

        # Chat Display Area
        self.text_area = scrolledtext.ScrolledText(
            self.window,
            wrap=tk.WORD,
            width=80,
            height=20,
            bg="#2e2e3e",
            fg="#f0f0f0",
            font=("Arial", 12),
            state=tk.DISABLED
        )
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Entry Frame
        entry_frame = tk.Frame(self.window, bg="#1e1e2f")
        entry_frame.pack(fill=tk.X, padx=10, pady=10)

        # Entry Field
        self.input_entry = tk.Entry(
            entry_frame,
            width=70,
            font=("Arial", 12),
            bg="#3e3e4e",
            fg="#ffffff",
            insertbackground="#ffffff"
        )
        self.input_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

        # Send Button
        self.send_button = tk.Button(
            entry_frame,
            text="Send",
            command=self.process_input,
            font=("Arial", 12),
            bg="#f5a623",
            fg="#1e1e2f",
            activebackground="#f0f0f0"
        )
        self.send_button.pack(side=tk.RIGHT, padx=5)

        # Tag Configuration
        self.text_area.tag_configure("user_tag", foreground="#7eca9c", justify="left")
        self.text_area.tag_configure("bot_tag", foreground="#f5a623", justify="right")

        # Knowledge Base
        self.knowledge_base_file = knowledge_base_file
        self.knowledge_base = self.load_knowledge_base()

    def load_knowledge_base(self) -> dict:
        try:
            with open(self.knowledge_base_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {"questions": []}

    def save_knowledge_base(self):
        with open(self.knowledge_base_file, 'w') as file:
            json.dump(self.knowledge_base, file, indent=2)

    def find_best_match(self, user_question: str) -> str | None:
        questions = [q["question"] for q in self.knowledge_base["questions"]]
        matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
        return matches[0] if matches else None

    def get_answer_for_question(self, question: str) -> str | None:
        for q in self.knowledge_base["questions"]:
            if q["question"] == question:
                return q["answer"]

    def open_website(self, url: str):
        webbrowser.open(url)

    def show_about_app(self):
        self.display_message("Andro: This is a chatbot application designed to learn and respond interactively.", "bot_tag")

    def show_about_developer(self):
        self.display_message("Andro: Developed by Shailesh Singh Bisht.", "bot_tag")

    def display_message(self, message: str, tag: str):
        self.text_area.configure(state=tk.NORMAL)
        self.text_area.insert(tk.END, f"{message}\n", tag)
        self.text_area.configure(state=tk.DISABLED)
        self.text_area.see(tk.END)

    def process_input(self):
        user_input = self.input_entry.get().strip()
        self.input_entry.delete(0, tk.END)

        if not user_input:
            return

        self.display_message(f"You: {user_input}", "user_tag")

        if user_input.lower() == "quit":
            self.window.destroy()
            return

        best_match = self.find_best_match(user_input)

        if best_match:
            answer = self.get_answer_for_question(best_match)
            self.display_message(f"Andro: {answer}", "bot_tag")
        else:
            self.display_message("Andro: I don't know the answer. Can you teach me?", "bot_tag")
            new_answer = simpledialog.askstring("Teach Me", "Type the answer or click OK to skip:")

            if new_answer:
                self.knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                self.save_knowledge_base()
                self.display_message("Andro: Thank you! I've learned something new.", "bot_tag")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    chat_bot_ui = ChatBotUI()
    chat_bot_ui.run()
