"""
Text-to-Speech Bot
-------------------
A desktop application that converts typed text into speech.
Users can enter text, choose a voice, adjust the speech rate,
and start/stop playback.

Tech stack: Python, Tkinter (GUI), pyttsx3 (offline speech engine)

Author: V. Vamshi Krishna
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pyttsx3
import threading


class TextToSpeechBot:
    def __init__(self, root):
        self.root = root
        self.root.title("Text-to-Speech Bot")
        self.root.geometry("540x480")
        self.root.resizable(False, False)

        # Style colors (Modern Dark Theme)
        self.bg_color = "#121214"
        self.card_color = "#1e1e24"
        self.accent_color = "#5856d6"
        self.text_color = "#e2e2e9"
        self.text_muted = "#a1a1b5"
        
        self.btn_speak_normal = "#27ae60"
        self.btn_speak_hover = "#2ecc71"
        self.btn_speak_disabled = "#1e3d29"
        
        self.btn_stop_normal = "#c0392b"
        self.btn_stop_hover = "#e74c3c"
        self.btn_stop_disabled = "#401c18"

        self.root.config(bg=self.bg_color)
        
        # Configure TTK style
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Apply dark theme to TTK styles
        self.style.configure(".", background=self.bg_color, foreground=self.text_color)
        self.style.configure(
            "TCombobox",
            fieldbackground=self.card_color,
            background="#3a3a42",
            foreground=self.text_color,
            arrowcolor=self.text_color,
            bordercolor="#2d2d34",
            lightcolor="#2d2d34",
            darkcolor="#2d2d34"
        )
        self.style.map(
            "TCombobox",
            fieldbackground=[("readonly", self.card_color)],
            foreground=[("readonly", self.text_color)]
        )

        # Configure Combobox Popdown Listbox Colors via Option Database
        self.root.option_add("*TCombobox*Listbox.background", self.card_color)
        self.root.option_add("*TCombobox*Listbox.foreground", self.text_color)
        self.root.option_add("*TCombobox*Listbox.selectBackground", self.accent_color)
        self.root.option_add("*TCombobox*Listbox.selectForeground", "#ffffff")
        self.root.option_add("*TCombobox*Listbox.font", ("Segoe UI", 10))

        # Safely query voices on startup using a temporary engine instance
        self.voices = []
        try:
            temp_engine = pyttsx3.init()
            self.voices = temp_engine.getProperty("voices") or []
            del temp_engine
        except Exception:
            pass

        self._speech_lock = threading.Lock()
        self._is_speaking = False
        self._speech_thread = None
        self.engine = None  # Reference to the engine running in the background thread

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        self._build_ui()

    def _build_ui(self):
        # Header / Title
        header_frame = tk.Frame(self.root, bg=self.bg_color)
        header_frame.pack(fill="x", pady=(20, 10))

        title = tk.Label(
            header_frame,
            text="Text-to-Speech Bot",
            font=("Segoe UI", 16, "bold"),
            bg=self.bg_color,
            fg=self.accent_color,
        )
        title.pack()

        subtitle = tk.Label(
            header_frame,
            text="Enter text, choose a voice, and adjust speed.",
            font=("Segoe UI", 9),
            bg=self.bg_color,
            fg=self.text_muted,
        )
        subtitle.pack(pady=(2, 0))

        # --- Text Input Area ---
        text_frame = tk.Frame(self.root, bg=self.bg_color)
        text_frame.pack(fill="both", expand=True, padx=25, pady=5)

        self.text_input = tk.Text(
            text_frame,
            height=6,
            wrap="word",
            bg=self.card_color,
            fg=self.text_color,
            insertbackground=self.text_color,  # White cursor
            font=("Segoe UI", 11),
            relief="flat",
            bd=0,
            padx=10,
            pady=10,
            highlightthickness=1,
            highlightbackground="#2d2d34",
            highlightcolor=self.accent_color,
        )
        self.text_input.pack(fill="both", expand=True)
        self.text_input.insert("1.0", "Type something here and click Speak...")

        # Clear placeholder text on focus
        self.text_input.bind("<FocusIn>", self._clear_placeholder)

        # --- Controls Frame (Voice & Rate) ---
        controls_frame = tk.Frame(self.root, bg=self.bg_color)
        controls_frame.pack(fill="x", padx=25, pady=10)

        # Voice selection
        voice_subframe = tk.Frame(controls_frame, bg=self.bg_color)
        voice_subframe.pack(side="left", fill="x", expand=True, padx=(0, 10))

        tk.Label(
            voice_subframe,
            text="CHOOSE VOICE",
            font=("Segoe UI", 8, "bold"),
            bg=self.bg_color,
            fg=self.text_muted,
        ).pack(anchor="w", pady=(0, 4))

        self.voice_names = [v.name for v in self.voices] if self.voices else ["Default Voice"]
        self.selected_voice = tk.StringVar(value=self.voice_names[0])

        self.voice_dropdown = ttk.Combobox(
            voice_subframe,
            textvariable=self.selected_voice,
            values=self.voice_names,
            state="readonly",
            font=("Segoe UI", 10),
        )
        self.voice_dropdown.pack(fill="x")

        # Speech rate
        rate_subframe = tk.Frame(controls_frame, bg=self.bg_color)
        rate_subframe.pack(side="right", fill="x", expand=True, padx=(10, 0))

        self.rate_label_var = tk.StringVar(value="SPEECH RATE: 175 wpm")
        tk.Label(
            rate_subframe,
            textvariable=self.rate_label_var,
            font=("Segoe UI", 8, "bold"),
            bg=self.bg_color,
            fg=self.text_muted,
        ).pack(anchor="w", pady=(0, 4))

        self.rate_slider = tk.Scale(
            rate_subframe,
            from_=80,
            to=300,
            orient="horizontal",
            showvalue=False,
            command=self._on_rate_change,
            bg=self.bg_color,
            fg=self.text_color,
            troughcolor=self.card_color,
            activebackground=self.accent_color,
            highlightbackground=self.bg_color,
            highlightcolor=self.bg_color,
            bd=0,
        )
        self.rate_slider.set(175)
        self.rate_slider.pack(fill="x")

        # --- Buttons Frame ---
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(fill="x", padx=25, pady=(15, 10))

        self.speak_btn = tk.Button(
            button_frame,
            text="Speak",
            font=("Segoe UI", 10, "bold"),
            bg=self.btn_speak_normal,
            fg="white",
            relief="flat",
            bd=0,
            padx=20,
            pady=8,
            activebackground="#219653",
            activeforeground="white",
            command=self.speak_text,
            cursor="hand2"
        )
        self.speak_btn.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.speak_btn.bind("<Enter>", lambda e: self._on_btn_hover(self.speak_btn, self.btn_speak_hover))
        self.speak_btn.bind("<Leave>", lambda e: self._on_btn_hover(self.speak_btn, self.btn_speak_normal))

        self.stop_btn = tk.Button(
            button_frame,
            text="Stop",
            font=("Segoe UI", 10, "bold"),
            bg=self.btn_stop_normal,
            fg="white",
            relief="flat",
            bd=0,
            padx=20,
            pady=8,
            activebackground="#962d22",
            activeforeground="white",
            command=self.stop_speaking,
            cursor="hand2"
        )
        self.stop_btn.pack(side="right", fill="x", expand=True, padx=(8, 0))
        self.stop_btn.bind("<Enter>", lambda e: self._on_btn_hover(self.stop_btn, self.btn_stop_hover))
        self.stop_btn.bind("<Leave>", lambda e: self._on_btn_hover(self.stop_btn, self.btn_stop_normal))
        
        # Initialize buttons state
        self._set_speaking_state(False)

        # --- Status Bar ---
        self.status_var = tk.StringVar(value="Status: Ready")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Segoe UI", 9),
            bg=self.card_color,
            fg=self.text_muted,
            anchor="w",
            padx=15,
            pady=6,
        )
        status_bar.pack(fill="x", side="bottom")

    def _clear_placeholder(self, event):
        current_text = self.text_input.get("1.0", "end-1c")
        if current_text == "Type something here and click Speak...":
            self.text_input.delete("1.0", "end")

    def _on_btn_hover(self, btn, color):
        if str(btn["state"]) == "normal":
            btn.config(bg=color)

    def _on_rate_change(self, value):
        self.rate_label_var.set(f"SPEECH RATE: {value} wpm")

    def _set_speaking_state(self, speaking):
        self._is_speaking = speaking
        if speaking:
            self.speak_btn.config(state="disabled", bg=self.btn_speak_disabled)
            self.stop_btn.config(state="normal", bg=self.btn_stop_normal)
            self.status_var.set("Status: Speaking...")
        else:
            self.speak_btn.config(state="normal", bg=self.btn_speak_normal)
            self.stop_btn.config(state="disabled", bg=self.btn_stop_disabled)
            self.status_var.set("Status: Ready")

    def _find_voice_id(self, voice_name):
        for voice in self.voices:
            if voice.name == voice_name:
                return voice.id
        return None

    def _show_error(self, title, message):
        messagebox.showerror(title, message)

    def _on_close(self):
        self.stop_speaking()
        self.root.destroy()

    def speak_text(self):
        text = self.text_input.get("1.0", "end").strip()

        if not text or text == "Type something here and click Speak...":
            messagebox.showwarning("Input Required", "Please enter text to speak!")
            return

        if self._is_speaking:
            return

        self._set_speaking_state(True)

        # Run speech in a separate thread so the UI doesn't freeze
        def run_speech():
            with self._speech_lock:
                try:
                    # Initialize pyttsx3 inside the thread to avoid COM apartment issues
                    self.engine = pyttsx3.init()
                    
                    # Apply selected voice and rate
                    voice_name = self.selected_voice.get()
                    voice_id = self._find_voice_id(voice_name)
                    if voice_id:
                        self.engine.setProperty("voice", voice_id)

                    self.engine.setProperty("rate", int(self.rate_slider.get()))
                    
                    self.engine.say(text)
                    self.engine.runAndWait()
                except Exception as exc:
                    self.root.after(0, lambda: self._show_error("Speech Error", f"Speech playback failed: {exc}"))
                finally:
                    # Reset references and state in the main thread
                    self.root.after(0, lambda: self._set_speaking_state(False))
                    self.root.after(0, lambda: setattr(self, "_speech_thread", None))
                    self.root.after(0, lambda: setattr(self, "engine", None))

        self._speech_thread = threading.Thread(target=run_speech, daemon=True)
        self._speech_thread.start()

    def stop_speaking(self):
        try:
            if self.engine:
                self.engine.stop()
            self._set_speaking_state(False)
        except Exception as exc:
            messagebox.showerror("Speech Error", f"Could not stop speech: {exc}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TextToSpeechBot(root)
    root.mainloop()
