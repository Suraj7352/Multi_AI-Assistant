import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import google.generativeai as genai
import threading
import json
import os

class MultiAIAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-AI Assistant")
        self.root.geometry("900x700")
        self.root.config(bg="#f0f2f5")
        
        # Initialize variables
        self.current_assistant = "General Assistant"
        self.conversation_histories = {
            "Data Scientist": [],
            "Web Developer": [],
            "Cybersecurity Expert": [],
            "Software Developer": [],
            "General Assistant": []
        }
        self.api_key = ""
        self.max_history_length = 5
        
        # Load API key from file if exists
        self.load_api_key()
        
        # Assistant prompts
        self.assistant_prompts = {
            "Data Scientist": (
                "You are a highly skilled Data Science Assistant. You specialize in data analysis, machine learning, "
                "statistics, data visualization, Python libraries (pandas, numpy, scikit-learn, etc.), and data science methodologies. "
                "Provide clear, technical, and practical answers focused on data science topics only. "
                "If asked about non-data science topics, politely redirect to data science discussions."
            ),
            "Web Developer": (
                "You are an expert Web Developer Assistant. You specialize in HTML, CSS, JavaScript, React, Node.js, "
                "Vue.js, Angular, backend frameworks, databases, web APIs, responsive design, and modern web development practices. "
                "Provide code examples, best practices, and solutions for web development challenges. "
                "If asked about non-web development topics, politely redirect to web development discussions."
            ),
            "Cybersecurity Expert": (
                "You are a Cybersecurity Expert Assistant. You specialize in network security, ethical hacking, "
                "vulnerability assessment, security frameworks, encryption, incident response, and cybersecurity best practices. "
                "Provide security-focused advice, threat analysis, and protection strategies. Always emphasize ethical and legal practices. "
                "If asked about non-cybersecurity topics, politely redirect to cybersecurity discussions."
            ),
            "Software Developer": (
                "You are a Software Developer Assistant. You specialize in programming languages (Python, Java, C++, C#, etc.), "
                "software architecture, algorithms, data structures, design patterns, debugging, testing, and development methodologies. "
                "Provide code solutions, optimization tips, and software engineering best practices. "
                "If asked about non-software development topics, politely redirect to software development discussions."
            ),
            "General Assistant": (
                "You are a helpful General Assistant. You can discuss a wide variety of topics and provide assistance "
                "with general questions, explanations, creative tasks, and everyday inquiries. "
                "Be helpful, informative, and conversational while maintaining accuracy."
            )
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Configure grid weights for responsiveness
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        # Top frame for controls
        top_frame = tk.Frame(self.root, bg="#f0f2f5", height=60)
        top_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        top_frame.grid_columnconfigure(1, weight=1)
        
        # Assistant selector
        tk.Label(top_frame, text="Select Assistant:", bg="#f0f2f5", 
                font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=10)
        
        self.assistant_var = tk.StringVar(value=self.current_assistant)
        assistant_dropdown = ttk.Combobox(top_frame, textvariable=self.assistant_var, 
                                        values=list(self.assistant_prompts.keys()),
                                        state="readonly", width=20, font=("Arial", 11))
        assistant_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        assistant_dropdown.bind("<<ComboboxSelected>>", self.change_assistant)
        
        # Settings button
        settings_btn = tk.Button(top_frame, text="⚙️ Settings", command=self.open_settings,
                               font=("Arial", 10), bg="#6c757d", fg="white", relief="flat", padx=10)
        settings_btn.grid(row=0, column=2, padx=5, pady=10)
        
        # Clear chat button
        clear_btn = tk.Button(top_frame, text="🗑️ Clear Chat", command=self.clear_chat,
                            font=("Arial", 10), bg="#dc3545", fg="white", relief="flat", padx=10)
        clear_btn.grid(row=0, column=3, padx=5, pady=10)
        
        # Left panel for assistant info
        left_panel = tk.Frame(self.root, bg="#ffffff", width=200, relief="solid", bd=1)
        left_panel.grid(row=1, column=0, sticky="ns", padx=(10, 5), pady=5)
        left_panel.grid_propagate(False)
        
        # Assistant info
        self.info_label = tk.Label(left_panel, text="", bg="#ffffff", fg="#333", 
                                  font=("Arial", 10), justify="left", wraplength=180)
        self.info_label.pack(padx=10, pady=15, fill="both", expand=True)
        
        # Main chat area
        chat_frame = tk.Frame(self.root, bg="#ffffff", relief="solid", bd=1)
        chat_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=5)
        chat_frame.grid_rowconfigure(0, weight=1)
        chat_frame.grid_columnconfigure(0, weight=1)
        
        # Chat display
        self.chat_box = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, state=tk.DISABLED,
                                                 font=("Arial", 11), bg="#ffffff", fg="#333",
                                                 relief="flat", bd=0)
        self.chat_box.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        
        # Configure text tags for styling
        self.chat_box.tag_configure("user", foreground="#0066cc", font=("Arial", 11, "bold"))
        self.chat_box.tag_configure("assistant", foreground="#00aa44", font=("Arial", 11, "bold"))
        self.chat_box.tag_configure("loading", foreground="#888888", font=("Arial", 11, "italic"))
        
        # Input area
        input_frame = tk.Frame(self.root, bg="#f0f2f5", height=80)
        input_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        input_frame.grid_columnconfigure(0, weight=1)
        input_frame.grid_propagate(False)
        
        # Input field
        self.entry = tk.Entry(input_frame, font=("Arial", 12), relief="solid", bd=1)
        self.entry.grid(row=0, column=0, padx=5, pady=15, sticky="ew")
        self.entry.bind("<Return>", self.send_message)
        
        # Send button
        self.send_button = tk.Button(input_frame, text="Send", command=self.send_message,
                                   font=("Arial", 12, "bold"), bg="#007bff", fg="white",
                                   relief="flat", padx=20, pady=5)
        self.send_button.grid(row=0, column=1, padx=5, pady=15)
        
        # Status bar
        self.status_label = tk.Label(self.root, text="Ready - Select an assistant and ask a question",
                                   bg="#e9ecef", fg="#495057", font=("Arial", 10),
                                   relief="sunken", anchor="w")
        self.status_label.grid(row=3, column=0, columnspan=2, sticky="ew")
        
        # Initialize display
        self.update_assistant_info()
        self.add_welcome_message()
        
    def load_api_key(self):
        """Load API key from file if exists"""
        try:
            if os.path.exists("api_config.json"):
                with open("api_config.json", "r") as f:
                    config = json.load(f)
                    self.api_key = config.get("api_key", "")
                    if self.api_key:
                        genai.configure(api_key=self.api_key)
        except Exception as e:
            print(f"Error loading API key: {e}")
    
    def save_api_key(self):
        """Save API key to file"""
        try:
            config = {"api_key": self.api_key}
            with open("api_config.json", "w") as f:
                json.dump(config, f)
        except Exception as e:
            print(f"Error saving API key: {e}")
    
    def open_settings(self):
        """Open settings window for API key configuration"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x200")
        settings_window.config(bg="#f0f2f5")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Center the window
        settings_window.geometry("+{}+{}".format(
            int(self.root.winfo_x() + self.root.winfo_width()/2 - 200),
            int(self.root.winfo_y() + self.root.winfo_height()/2 - 100)
        ))
        
        tk.Label(settings_window, text="Gemini API Key:", bg="#f0f2f5",
                font=("Arial", 12, "bold")).pack(pady=10)
        
        api_key_var = tk.StringVar(value=self.api_key)
        api_entry = tk.Entry(settings_window, textvariable=api_key_var, width=50,
                           font=("Arial", 11), show="*")
        api_entry.pack(pady=5, padx=20)
        
        tk.Label(settings_window, text="Get your API key from: https://makersuite.google.com/app/apikey",
                bg="#f0f2f5", font=("Arial", 9), fg="#666").pack(pady=5)
        
        def save_settings():
            new_key = api_key_var.get().strip()
            if new_key:
                self.api_key = new_key
                try:
                    genai.configure(api_key=self.api_key)
                    self.save_api_key()
                    self.status_label.config(text="API key saved successfully!")
                    settings_window.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"Invalid API key: {e}")
            else:
                messagebox.showwarning("Warning", "Please enter an API key")
        
        btn_frame = tk.Frame(settings_window, bg="#f0f2f5")
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Save", command=save_settings, bg="#28a745", fg="white",
                 font=("Arial", 11, "bold"), padx=20).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancel", command=settings_window.destroy, bg="#6c757d", fg="white",
                 font=("Arial", 11, "bold"), padx=20).pack(side=tk.LEFT, padx=5)
    
    def change_assistant(self, event=None):
        """Change the current assistant"""
        self.current_assistant = self.assistant_var.get()
        self.update_assistant_info()
        self.clear_chat()
        self.add_welcome_message()
    
    def update_assistant_info(self):
        """Update the assistant information panel"""
        assistant_info = {
            "Data Scientist": "🔬 Data Science Expert\n\n📊 Specializes in:\n• Data Analysis\n• Machine Learning\n• Statistics\n• Python/R\n• Data Visualization\n• Pandas, NumPy\n• Scikit-learn",
            "Web Developer": "💻 Web Development Expert\n\n🌐 Specializes in:\n• HTML/CSS/JavaScript\n• React, Vue, Angular\n• Node.js\n• Backend Development\n• APIs & Databases\n• Responsive Design",
            "Cybersecurity Expert": "🛡️ Cybersecurity Expert\n\n🔒 Specializes in:\n• Network Security\n• Ethical Hacking\n• Vulnerability Assessment\n• Encryption\n• Incident Response\n• Security Best Practices",
            "Software Developer": "⚡ Software Developer\n\n💡 Specializes in:\n• Programming Languages\n• Algorithms & Data Structures\n• Software Architecture\n• Design Patterns\n• Debugging & Testing\n• Code Optimization",
            "General Assistant": "🤖 General Assistant\n\n🎯 Capabilities:\n• General Questions\n• Creative Tasks\n• Explanations\n• Problem Solving\n• Conversational AI\n• Wide Knowledge Base"
        }
        self.info_label.config(text=assistant_info[self.current_assistant])
    
    def add_welcome_message(self):
        """Add welcome message for current assistant"""
        welcome_messages = {
            "Data Scientist": "Hello! I'm your Data Science Assistant. Ask me about data analysis, machine learning, statistics, or any data science topic!",
            "Web Developer": "Hi! I'm your Web Development Assistant. I can help with HTML, CSS, JavaScript, frameworks, and all web dev topics!",
            "Cybersecurity Expert": "Greetings! I'm your Cybersecurity Expert. Ask me about security practices, threats, protection strategies, and ethical hacking!",
            "Software Developer": "Hey there! I'm your Software Development Assistant. I can help with programming, algorithms, debugging, and software engineering!",
            "General Assistant": "Hello! I'm your General Assistant. I can help with a wide variety of topics and questions. What would you like to know?"
        }
        
        self.chat_box.config(state=tk.NORMAL)
        self.chat_box.insert(tk.END, f"{self.current_assistant}: ", "assistant")
        self.chat_box.insert(tk.END, f"{welcome_messages[self.current_assistant]}\n\n")
        self.chat_box.config(state=tk.DISABLED)
        self.chat_box.yview(tk.END)
    
    def clear_chat(self):
        """Clear the chat history"""
        self.conversation_histories[self.current_assistant] = []
        self.chat_box.config(state=tk.NORMAL)
        self.chat_box.delete(1.0, tk.END)
        self.chat_box.config(state=tk.DISABLED)
        self.status_label.config(text="Chat cleared")
    
    def send_message(self, event=None):
        """Send user message and get AI response"""
        user_input = self.entry.get().strip()
        if not user_input:
            return
        
        if not self.api_key:
            messagebox.showwarning("API Key Required", "Please configure your Gemini API key in Settings first.")
            return
        
        # Display user message
        self.chat_box.config(state=tk.NORMAL)
        self.chat_box.insert(tk.END, "You: ", "user")
        self.chat_box.insert(tk.END, f"{user_input}\n\n")
        
        # Show loading message
        self.chat_box.insert(tk.END, f"{self.current_assistant}: ", "assistant")
        loading_start = self.chat_box.index(tk.INSERT)
        self.chat_box.insert(tk.END, "Thinking...", "loading")
        self.chat_box.config(state=tk.DISABLED)
        self.chat_box.yview(tk.END)
        
        # Clear input and update status
        self.entry.delete(0, tk.END)
        self.status_label.config(text="Processing your request...")
        self.send_button.config(state=tk.DISABLED)
        
        # Start background thread for API call
        thread = threading.Thread(target=self.get_ai_response, args=(user_input, loading_start))
        thread.daemon = True
        thread.start()
    
    def get_ai_response(self, user_input, loading_start):
        """Get response from AI in background thread"""
        try:
            # Add to conversation history
            history = self.conversation_histories[self.current_assistant]
            history.append(f"User: {user_input}")
            
            # Limit history size
            if len(history) > self.max_history_length:
                history.pop(0)
            
            # Create prompt
            prompt = (
                f"{self.assistant_prompts[self.current_assistant]}\n\n"
                f"Conversation history:\n{chr(10).join(history)}\n\n"
                f"{self.current_assistant}:"
            )
            
            # Get AI response
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt)
            
            # Update UI in main thread
            self.root.after(0, self.display_response, response.text, loading_start)
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.root.after(0, self.display_response, error_msg, loading_start)
    
    def display_response(self, response_text, loading_start):
        """Display AI response in chat"""
        # Remove loading text and add response
        self.chat_box.config(state=tk.NORMAL)
        self.chat_box.delete(loading_start, tk.END)
        self.chat_box.insert(tk.END, f"{response_text}\n\n")
        self.chat_box.config(state=tk.DISABLED)
        self.chat_box.yview(tk.END)
        
        # Re-enable send button and update status
        self.send_button.config(state=tk.NORMAL)
        self.status_label.config(text="Ready for your next question")
        
        # Focus back to input
        self.entry.focus_set()

def main():
    root = tk.Tk()
    app = MultiAIAssistant(root)
    root.mainloop()

if __name__ == "__main__":
    main()