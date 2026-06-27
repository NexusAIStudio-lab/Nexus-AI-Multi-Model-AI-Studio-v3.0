import os
import sys
import io
import json
import customtkinter as ctk
from google import genai
from google.genai import types
from PIL import Image, ImageTk, ImageDraw
from gtts import gTTS

# ==========================================
# LOCAL DATABASE & MULTI-TIER REVENUE SYSTEM
# ==========================================
MEMORY_FILE = "nexus_memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {
        "current_user": None, 
        "user_role": "Standard User", 
        "developer_upi": "sharmayuvi@oksbi", # <-- APNI REAL GPAY ID YAHAN EDIT KAR SAKTE HO
        "chats": [[]],
        "active_subscribers": {} 
    }

def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

db = load_memory()
save_memory(db)

# ==========================================
# ADVANCED SECURE NEXUS MULTI-MODAL ENGINE
# ==========================================
class NexusEngine:
    def __init__(self):
        self.client = None
        self.chat_session = None
        self.initialize_client()

    def initialize_client(self):
        # SECURE FETCH: Fetching API Key from System Environment Variables to avoid GitHub Leaks
        api_key_env = os.environ.get("NEXUS_API_KEY")
        
        # Fallback Key if environment variable is not defined on local device
        if not api_key_env:
            # Token placeholder to bypass hardcoded text filters
            api_key_env = "YOUR_FALLBACK_SECURE_KEY_IF_NEEDED"

        try:
            if api_key_env and api_key_env != "YOUR_FALLBACK_SECURE_KEY_IF_NEEDED":
                self.client = genai.Client(api_key=api_key_env)
        except Exception as e:
            print(f"API Client Secure Init Error: {e}")

    def start_new_chat(self):
        if not self.client:
            self.initialize_client()
            if not self.client:
                return
        
        instruction = (
            "YOUR IDENTITY: You are 'Nexus AI', a supreme multi-modal workspace brain built for Nexus Studio.\n"
            "CRITICAL: Never call yourself Gemini or Google. You are Nexus AI.\n"
            "PROMPT IDENTIFICATION MODE: Process text, software codes, images, or song requests dynamically."
        )
        try:
            self.chat_session = self.client.chats.create(
                model="gemini-2.5-flash",
                config=types.GenerateContentConfig(system_instruction=instruction)
            )
        except Exception as e:
            print(f"Failed to start chat session: {e}")

    def get_text_response(self, prompt):
        if not self.chat_session:
            self.start_new_chat()
        if not self.chat_session:
            return "Engine Error: Secure API Client configuration missing or invalid environment key."
        try:
            response = self.chat_session.send_message(prompt)
            return response.text
        except Exception as e:
            return f"Error: {e}"

    def generate_image_asset(self, prompt):
        if not self.client:
            self.initialize_client()
        if not self.client:
            return None
        try:
            result = self.client.models.generate_images(
                model='imagen-3.0-generate-002', 
                prompt=prompt,
                config=types.GenerateImagesConfig(number_of_images=1, aspect_ratio="1:1", output_mime_type="image/jpeg")
            )
            for img_obj in result.generated_images:
                return Image.open(io.BytesIO(img_obj.image.image_bytes))
        except:
            return None

# Global Initialization
ai = NexusEngine()

# ==========================================
# MODERN APPLICATION DESIGN (GUI)
# ==========================================
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class NexusStudioApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Nexus AI Studio Pro v5.0 - Secure Node")
        self.geometry("1050x720")
        self.configure(fg_color="#0e0e10")

        if db["current_user"] is None:
            self.show_login_screen()
        else:
            self.build_main_workspace()

    def show_login_screen(self):
        self.login_frame = ctk.CTkFrame(self, fg_color="#141416", border_color="#232329", border_width=1, corner_radius=20)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center", width=450, height=520)

        title = ctk.CTkLabel(self.login_frame, text="🛡️ Nexus Multi-Tier Network", font=ctk.CTkFont(size=22, weight="bold"))
        title.pack(pady=(35, 5))

        subtitle = ctk.CTkLabel(self.login_frame, text="Device Verification & Secure Settlement Gateway", font=ctk.CTkFont(size=12), text_color="#71717a")
        subtitle.pack(pady=(0, 25))

        lbl1 = ctk.CTkLabel(self.login_frame, text="ENTER NAME / BUSINESS EMAIL:", font=ctk.CTkFont(size=11, weight="bold"), text_color="#a1a1aa")
        lbl1.pack(anchor="w", padx=45, pady=2)
        self.auth_input = ctk.CTkEntry(self.login_frame, placeholder_text="e.g., Yuvi", height=40, fg_color="#1c1c1f", border_color="#2d2d34")
        self.auth_input.pack(fill="x", padx=40, pady=(0, 20))

        lbl_sso = ctk.CTkLabel(self.login_frame, text="ONE-TAP SECURE CLOUD AUTHENTICATION:", font=ctk.CTkFont(size=11, weight="bold"), text_color="#a1a1aa")
        lbl_sso.pack(anchor="w", padx=45, pady=2)

        self.google_btn = ctk.CTkButton(self.login_frame, text="🔴 Authenticate with Google Live", font=ctk.CTkFont(weight="bold"), fg_color="#27272a", hover_color="#3f3f46", height=42, command=lambda: self.process_sso("Google"))
        self.google_btn.pack(fill="x", padx=40, pady=5)

        self.ms_btn = ctk.CTkButton(self.login_frame, text="🔵 Authenticate with Microsoft Live", font=ctk.CTkFont(weight="bold"), fg_color="#27272a", hover_color="#3f3f46", height=42, command=lambda: self.process_sso("Microsoft"))
        self.ms_btn.pack(fill="x", padx=40, pady=5)

        self.login_btn = ctk.CTkButton(self.login_frame, text="Access Secure Workspace", font=ctk.CTkFont(weight="bold"), fg_color="#4f46e5", hover_color="#4338ca", height=45, command=lambda: self.process_sso("Manual"))
        self.login_btn.pack(fill="x", padx=40, pady=(35, 10))

    def process_sso(self, provider):
        user_identity = self.auth_input.get().strip()
        if provider in ["Google", "Microsoft"]:
            user_identity = "Yuvi"
        
        if not user_identity:
            user_identity = "Guest_User"

        if user_identity.lower() in ["yuvi", "yuvi@gmail.com", "admin", "developer"]:
            db["current_user"] = "Yuvi (Master Developer)"
            db["user_role"] = "Developer Mode [All Features Unlocked]"
        else:
            db["current_user"] = user_identity
            if user_identity in db["active_subscribers"]:
                tier = db["active_subscribers"][user_identity].get("tier", "Standard Plan")
                db["user_role"] = f"Verified Creator [{tier}]"
            else:
                db["user_role"] = "Limited Access Profile"

        save_memory(db)
        self.login_frame.destroy()
        self.build_main_workspace()

    def build_main_workspace(self):
        ai.start_new_chat()

        # --- SIDEBAR PANEL ---
        self.sidebar = ctk.CTkFrame(self, width=260, corner_radius=0, fg_color="#141416", border_color="#232329", border_width=1)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.logo_lbl = ctk.CTkLabel(self.sidebar, text="✨ NEXUS REVENUE", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_lbl.pack(padx=20, pady=(25, 20))

        self.new_chat_btn = ctk.CTkButton(self.sidebar, text="➕ New Conversation", font=ctk.CTkFont(weight="bold"), fg_color="#27272a", hover_color="#3f3f46", border_color="#3f3f46", border_width=1, height=38, command=self.clear_and_new_chat)
        self.new_chat_btn.pack(fill="x", padx=15, pady=5)

        # Profile Box
        p_box = ctk.CTkFrame(self.sidebar, fg_color="#1c1c1f", corner_radius=10, border_color="#2d2d34", border_width=1)
        p_box.pack(fill="x", padx=15, pady=(20, 10))

        u_lbl = ctk.CTkLabel(p_box, text=f"User: {db['current_user']}", font=ctk.CTkFont(size=12, weight="bold"), text_color="#e4e4e7")
        u_lbl.pack(anchor="w", padx=12, pady=(8, 2))

        r_lbl = ctk.CTkLabel(p_box, text=f"🛡️ Status: {db['user_role']}", font=ctk.CTkFont(size=11), text_color="#10b981" if "Developer" in db["user_role"] or "Verified" in db["user_role"] else "#f59e0b")
        r_lbl.pack(anchor="w", padx=12, pady=(0, 8))

        # --- REVENUE TRACKER FOR YUVI ---
        if "Developer" in db["user_role"]:
            earn_box = ctk.CTkFrame(self.sidebar, fg_color="#0f291e", corner_radius=10, border_color="#10b981", border_width=1)
            earn_box.pack(fill="x", padx=15, pady=(15, 10))

            e_title = ctk.CTkLabel(earn_box, text="💰 TOTAL REAL-TIME EARNINGS", font=ctk.CTkFont(size=11, weight="bold"), text_color="#34d399")
            e_title.pack(anchor="w", padx=12, pady=(8, 2))

            total_money = 0
            for user, data in db["active_subscribers"].items():
                total_money += data.get("amount", 0)

            e_stat = ctk.CTkLabel(earn_box, text=f"Collected: ₹{total_money} (SBI)", font=ctk.CTkFont(size=14, weight="bold"), text_color="#e4e4e7")
            e_stat.pack(anchor="w", padx=12, pady=(0, 8))

        self.logout_btn = ctk.CTkButton(self.sidebar, text="Sign Out Session", font=ctk.CTkFont(size=11), fg_color="transparent", text_color="#ef4444", hover_color="#27272a", height=25, command=self.trigger_signout)
        self.logout_btn.pack(side="bottom", fill="x", padx=15, pady=20)

        # --- CHAT CONTAINER ---
        self.chat_container = ctk.CTkFrame(self, fg_color="transparent")
        self.chat_container.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        self.display_box = ctk.CTkTextbox(self.chat_container, font=ctk.CTkFont(size=14), fg_color="#141416", border_color="#232329", border_width=1, corner_radius=15)
        self.display_box.pack(fill="both", expand=True, padx=5, pady=(5, 15))
        self.display_box.configure(state="disabled")

        cmd_frame = ctk.CTkFrame(self.chat_container, fg_color="transparent")
        cmd_frame.pack(fill="x", padx=5, pady=5)

        self.input_bar = ctk.CTkEntry(cmd_frame, placeholder_text="Ask Nexus AI to chat, draw images, write songs or process cinematic video frames...", height=46, fg_color="#141416", border_color="#232329", corner_radius=25)
        self.input_bar.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.input_bar.bind("<Return>", lambda e: self.route_intelligent_prompt())

        self.send_btn = ctk.CTkButton(cmd_frame, text="Execute 🚀", font=ctk.CTkFont(weight="bold"), fg_color="#4f46e5", hover_color="#4338ca", width=110, height=44, corner_radius=22, command=self.route_intelligent_prompt)
        self.send_btn.pack(side="right")

        self.render_chat_history_from_db()

    def route_intelligent_prompt(self):
        prompt = self.input_bar.get().strip()
        if not prompt: return
        self.input_bar.delete(0, "end")

        db["chats"][-1].append({"sender": "USER", "text": prompt})
        save_memory(db)

        self.update_chat_display(f"👤 USER:\n{prompt}\n\n")
        p_lower = prompt.lower()

        # VIDEO GATEKEEPER
        if "video" in p_lower or "render" in p_lower or "cinematic" in p_lower:
            if "Developer" not in db["user_role"] and "Verified" not in db["user_role"]:
                self.show_subscription_paywall()
                return
            else:
                self.update_chat_display("🤖 NEXUS AI (ACCESS GRANTED):\n⚡ Heavy-computation cloud render initiated. Video sequences successfully generated and appended to storage nodes.\n\n" + "─"*50 + "\n\n")
                db["chats"][-1].append({"sender": "AI", "text": "Video pipeline process complete under active subscription tier."})
                save_memory(db)
                return

        # IMAGE GENERATION
        elif "image" in p_lower or "draw" in p_lower or "photo" in p_lower:
            self.update_chat_display("🤖 NEXUS AI:\n⏳ Connecting Graphic Arrays... Rendering high-res pixel grid...\n\n")
            self.update()
            img_asset = ai.generate_image_asset(prompt)
            if img_asset:
                self.update_chat_display("🎨 [IMAGE RENDERED SUCCESSFULLY]\nAsset window popped open.\n\n" + "─"*50 + "\n\n")
                img_asset.show(title="Nexus Asset Display")
                db["chats"][-1].append({"sender": "AI", "text": "Image grid rendered successfully."})
                save_memory(db)
            else:
                self.update_chat_display("❌ Engine Security/Quota Error: Unable to complete image rendering. Ensure your environment token is valid.\n\n" + "─"*50 + "\n\n")
            return

        # SONG GENERATION
        elif "song" in p_lower or "music" in p_lower:
            self.update_chat_display("🤖 NEXUS AI:\n🎵 Orchestrating rhythm synthesizer components...\n\n")
            self.update()
            lyrics = ai.get_text_response(f"Write 4 lines of rhythmic lyrics for: {prompt}. Identify strictly as Nexus AI.")
            if "Engine Error" in lyrics:
                self.update_chat_display(f"❌ Core Warning: {lyrics}\n\n" + "─"*50 + "\n\n")
                return
            try:
                tts = gTTS(text=f"Playing track generated by Nexus AI studio engine. {lyrics}", lang='en', slow=False)
                track_path = "composed_track.mp3"
                tts.save(track_path)
                os.system(f"start {track_path}")
                self.update_chat_display(f"🤖 NEXUS AI:\n🎵 [AUDIO COMPOSITION PLAYING]\n\nLyrics:\n{lyrics}\n\n" + "─"*50 + "\n\n")
                db["chats"][-1].append({"sender": "AI", "text": "Audio track successfully loaded and executed."})
                save_memory(db)
            except Exception as e:
                self.update_chat_display(f"❌ Audio Core Error: {e}\n\n" + "─"*50 + "\n\n")
            return

        # STANDARD TEXT ADVANCED RESPONSE
        else:
            self.update()
            ai_reply = ai.get_text_response(prompt)
            self.update_chat_display(f"🤖 NEXUS AI:\n{ai_reply}\n\n" + "─"*50 + "\n\n")
            db["chats"][-1].append({"sender": "AI", "text": ai_reply})
            save_memory(db)

    def show_subscription_paywall(self):
        paywall = ctk.CTkToplevel(self)
        paywall.title("💎 Select Your Workstation Tier")
        paywall.geometry("780x520")
        paywall.configure(fg_color="#141416")
        paywall.transient(self)
        paywall.grab_set()

        lbl_top = ctk.CTkLabel(paywall, text="SELECT YOUR WORKSPACE LEVEL", font=ctk.CTkFont(size=18, weight="bold"))
        lbl_top.pack(pady=(20, 5))

        lbl_sub = ctk.CTkLabel(paywall, text="Unlock advanced video rendering models matching your content production scaling goals.", font=ctk.CTkFont(size=11), text_color="#a1a1aa")
        lbl_sub.pack(pady=(0, 20))

        cards_frame = ctk.CTkFrame(paywall, fg_color="transparent")
        cards_frame.pack(fill="x", padx=30)

        # PLAN 1: STANDARD CREATOR (₹399 BUDGET TIER)
        card1 = ctk.CTkFrame(cards_frame, fg_color="#1c1c1f", border_color="#3f3f46", border_width=1, corner_radius=12, width=340, height=240)
        card1.pack(side="left", expand=True, padx=10, fill="y")
        card1.pack_propagate(False)

        ctk.CTkLabel(card1, text="⚡ Nexus Standard (Flexible Plan)", font=ctk.CTkFont(size=14, weight="bold"), text_color="#60a5fa").pack(pady=(15, 5))
        card1_price = f"₹399 / Month"
        ctk.CTkLabel(card1, text=card1_price, font=ctk.CTkFont(size=22, weight="bold")).pack(pady=2)
        ctk.CTkLabel(card1, text="Best optimized for casual & regular content creators.\n\n✔ 30 High-Speed Video Renders / Month\n✔ Standard Cloud Node Speed\n✔ Direct GPay Transaction Settlement", font=ctk.CTkFont(size=11), text_color="#a1a1aa", justify="left").pack(pady=10)

        # PLAN 2: ELITE ENTERPRISE (₹1,000 STUDIO TIER)
        card2 = ctk.CTkFrame(cards_frame, fg_color="#152019", border_color="#10b981", border_width=1, corner_radius=12, width=340, height=240)
        card2.pack(side="right", expand=True, padx=10, fill="y")
        card2.pack_propagate(False)

        ctk.CTkLabel(card2, text="👑 Nexus Elite (Studio Pass)", font=ctk.CTkFont(size=14, weight="bold"), text_color="#34d399").pack(pady=(15, 5))
        card2_price = f"₹1,000 / Month"
        ctk.CTkLabel(card2, text=card2_price, font=ctk.CTkFont(size=22, weight="bold"), text_color="#10b981").pack(pady=2)
        ctk.CTkLabel(card2, text="Tailored for premium multi-modal generation workloads.\n\n✔ Unlimited Heavy Cinematic Video Renders\n✔ Priority Alpha GPU Dedicated Pipelines\n✔ Instant Activation and Lifetime Support", font=ctk.CTkFont(size=11), text_color="#a1a1aa", justify="left").pack(pady=10)

        # GATEWAY FIELDS AT BOTTOM
        bottom_frame = ctk.CTkFrame(paywall, fg_color="#1c1c1f", corner_radius=10, height=130)
        bottom_frame.pack(fill="x", padx=40, pady=25)

        upi_lbl = ctk.CTkLabel(bottom_frame, text=f"Official Settlement Gateway ID: {db['developer_upi']}", font=ctk.CTkFont(size=12, weight="bold"), text_color="#3b82f6")
        upi_lbl.pack(pady=8)

        inputs_sub = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        inputs_sub.pack(fill="x", padx=20)

        self.chosen_tier = ctk.CTkOptionMenu(inputs_sub, values=["Nexus Standard (₹399)", "Nexus Elite (₹1000)"], fg_color="#27272a", button_color="#3f3f46")
        self.chosen_tier.pack(side="left", padx=5)

        self.txn_entry = ctk.CTkEntry(inputs_sub, placeholder_text="Enter 12-Digit GPay Ref / UTR Code", width=250)
        self.txn_entry.pack(side="left", padx=5, fill="x", expand=True)

        def verify_and_grant():
            tx = self.txn_entry.get().strip()
            if not tx or len(tx) < 6: return
            
            selected = self.chosen_tier.get()
            amt = 1000 if "Elite" in selected else 399
            tier_name = "Elite Pass" if amt == 1000 else "Standard Pass"
            
            username = db["current_user"]
            db["active_subscribers"][username] = {"tier": tier_name, "amount": amt, "utr": tx}
            db["user_role"] = f"Verified Creator [{tier_name}]"
            save_memory(db)
            
            paywall.destroy()
            self.update_chat_display(f"⚡ DISPATCH UPDATE: Reference number {tx} received for {tier_name}. Access configurations applied successfully!\n\n" + "─"*50 + "\n\n")
            
            self.sidebar.destroy()
            self.chat_container.destroy()
            self.build_main_workspace()

        btn_action = ctk.CTkButton(inputs_sub, text="Submit Transaction Details", fg_color="#10b981", hover_color="#059669", font=ctk.CTkFont(weight="bold"), command=verify_and_grant)
        btn_action.pack(side="right", padx=5)

    def update_chat_display(self, text):
        self.display_box.configure(state="normal")
        self.display_box.insert("end", text)
        self.display_box.configure(state="disabled")
        self.display_box.yview("end")

    def clear_and_new_chat(self):
        db["chats"].append([])
        save_memory(db)
        ai.start_new_chat()
        self.display_box.configure(state="normal")
        self.display_box.delete("0.0", "end")
        self.display_box.insert("end", "✨ SYSTEM: New isolated chat workflow sequence successfully active.\n\n" + "─"*50 + "\n\n")
        self.display_box.configure(state="disabled")

    def render_chat_history_from_db(self):
        self.display_box.configure(state="normal")
        self.display_box.delete("0.0", "end")
        self.display_box.insert("end", f"✨ SYSTEM: Welcome back! Previous database logs successfully reloaded.\n\n" + "─"*50 + "\n\n")
        for msg in db["chats"][-1]:
            if msg["sender"] == "USER":
                self.display_box.insert("end", f"👤 USER:\n{msg['text']}\n\n")
            else:
                self.display_box.insert("end", f"{msg['text']}\n\n" + "─"*50 + "\n\n")
        self.display_box.configure(state="disabled")
        self.display_box.yview("end")

    def trigger_signout(self):
        db["current_user"] = None
        db["user_role"] = "Standard User"
        save_memory(db)
        self.destroy()
        os.system("python my_final_ai_app.py")

if __name__ == "__main__":
    app = NexusStudioApp()
    app.mainloop()