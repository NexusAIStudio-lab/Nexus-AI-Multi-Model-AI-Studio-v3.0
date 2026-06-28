import os
import sys
import json
import customtkinter as ctk
import threading
from google import genai
from google.genai import types
from PIL import Image
from gtts import gTTS

# ==========================================
# DATABASE & REVENUE ENGINE (Preserved)
# ==========================================
MEMORY_FILE = "nexus_memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f: return json.load(f)
        except: pass
    return {"current_user": None, "user_role": "Standard User", "chats": [[]], "active_subscribers": {}}

def save_memory(data):
    try:
        with open(MEMORY_FILE, "w") as f: json.dump(data, f, indent=4)
    except: pass

db = load_memory()

# ==========================================
# NEXUS ENGINE (Upgraded with Model Switching)
# ==========================================
class NexusEngine:
    def __init__(self):
        self.models = {
            "Nexus Flash Lite": "gemini-2.0-flash-lite-preview-02-05",
            "Nexus Flash 3.5": "gemini-1.5-flash",
            "Nexus Pro 3.1": "gemini-1.5-pro",
            "Nexus Thinking (Standard)": "gemini-2.0-flash-thinking",
            "Nexus Thinking (Extended)": "gemini-2.0-flash-thinking-exp"
        }
        self.client = genai.Client(api_key=os.environ.get("NEXUS_API_KEY", "YOUR_KEY"))

    def generate(self, prompt, model_name, thinking_mode):
        model_id = self.models.get(model_name, "gemini-1.5-flash")
        config = None
        if "Thinking" in model_name:
            config = types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(
                    include_thoughts=True if thinking_mode == "Extended" else False
                )
            )
        try:
            response = self.client.models.generate_content(model=model_id, contents=prompt, config=config)
            return response.text
        except Exception as e:
            return f"Nexus Engine Error: {str(e)}"

# ==========================================
# NEXUS STUDIO PRO UI (Integrated)
# ==========================================
class NexusStudioApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.engine = NexusEngine()
        self.title("Nexus AI Studio Pro")
        self.geometry("1200x800")
        self.build_workspace()

    def build_workspace(self):
        # Sidebar with Model Selector
        self.sidebar = ctk.CTkFrame(self, width=280)
        self.sidebar.pack(side="left", fill="y")
        
        ctk.CTkLabel(self.sidebar, text="SELECT NEXUS MODEL").pack(pady=10)
        self.model_menu = ctk.CTkOptionMenu(self.sidebar, values=list(self.engine.models.keys()))
        self.model_menu.pack(pady=5, padx=10)
        
        self.thinking_mode = ctk.CTkSegmentedButton(self.sidebar, values=["Standard", "Extended"])
        self.thinking_mode.set("Standard")
        self.thinking_mode.pack(pady=10, padx=10)
        
        # Floating "+" Tool Menu
        self.tool_btn = ctk.CTkButton(self, text="+", width=50, height=50, corner_radius=25, command=self.show_tools)
        self.tool_btn.place(x=300, y=700)
        
        # Chat
        self.display_box = ctk.CTkTextbox(self)
        self.display_box.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        self.input_bar = ctk.CTkEntry(self, placeholder_text="Ask Nexus...")
        self.input_bar.pack(side="bottom", fill="x", padx=20, pady=20)
        self.input_bar.bind("<Return>", self.send_prompt)

    def show_tools(self):
        win = ctk.CTkToplevel(self)
        win.geometry("200x300")
        for t in ["📂 Files", "🎨 Canvas", "🎵 Music"]:
            ctk.CTkButton(win, text=t, command=lambda x=t: print(f"Tool {x} clicked")).pack(pady=5)

    def send_prompt(self, event=None):
        prompt = self.input_bar.get()
        model = self.model_menu.get()
        mode = self.thinking_mode.get()
        
        self.display_box.insert("end", f"👤 USER: {prompt}\n\n")
        self.input_bar.delete(0, "end")
        threading.Thread(target=self.run_nexus, args=(prompt, model, mode)).start()

    def run_nexus(self, prompt, model, mode):
        response = self.engine.generate(prompt, model, mode)
        self.display_box.insert("end", f"🤖 NEXUS ({model}): {response}\n\n")

if __name__ == "__main__":
    app = NexusStudioApp()
    app.mainloop()
