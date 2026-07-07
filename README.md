# 🎙️ Text-to-Speech Bot (Python)

A sleek, modern desktop GUI application that converts typed text into speech using offline speech synthesis. Built with a responsive, multi-threaded architecture to ensure the interface never freezes during playback.

---

## 🚀 Downloads & Releases
Since this is a desktop application, it cannot be run directly in the browser. You can download a standalone pre-compiled executable to run it on your machine without installing Python:

*   **Download Executable**: [Get the latest release here](https://github.com/vamsi-2003/Text-to-speech-bot/releases)

---

## ✨ Features
*   **Modern UI**: Sleek dark mode design with responsive hover effects and clean layout structure.
*   **Voice Selection**: Instantly detects and lists all TTS voices installed on your system.
*   **Speech Rate Control**: Custom slider to adjust speed from 80 wpm to 300 wpm (words per minute).
*   **Speak & Stop Controls**: Multi-threaded controls to start speech playback and interrupt/stop it instantly.
*   **Status Indicator**: A bottom status bar indicating the application's state ("Ready", "Speaking...").
*   **Robust & Non-Blocking**: Speech processing is isolated to background worker threads to keep the UI smooth and responsive.

---

## 🔮 Planned Improvements & Roadmap
Here are some features planned for future releases:
*   **💾 Export to Audio File**: Save the synthesized speech directly as `.mp3` or `.wav` files.
*   **📂 Document Reader**: Import and read text directly from `.txt`, `.pdf`, or `.docx` files.
*   **⏸️ Pause & Resume**: Pause playback mid-sentence and resume from the exact same spot.
*   **🌓 Dark/Light Theme Toggle**: Seamless toggle to switch between a clean light mode and dark mode.
*   **🌐 Online Neural Voices**: Optional integration with online TTS engines for more natural, human-like voices.

---

## 🛠️ Tech Stack
*   **Language**: Python 3.x
*   **GUI Framework**: Tkinter / TTK
*   **Offline Speech Engine**: `pyttsx3` (Offline support - no internet or API key required)

---

## 📦 Setup & Installation

### Prerequisites
Make sure you have Python 3 installed on your system.

### Steps
1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/vamsi-2003/Text-to-speech-bot.git
    cd Text-to-speech-bot
    ```

2.  **Create and Activate Virtual Environment**:
    *   **Windows**:
        ```bash
        python -m venv .venv
        .venv\Scripts\activate
        ```
    *   **macOS/Linux**:
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Application**:
    ```bash
    python tts_bot.py
    ```

---

## ⚙️ Platform-Specific Requirements

*   **Windows**: Works out of the box using built-in SAPI5 voices (e.g., Microsoft David, Zira).
*   **Linux**: Requires `espeak-ng` and standard audio tools:
    ```bash
    sudo apt-get install espeak-ng
    ```
*   **macOS**: Uses the system-native Speech Synthesis Manager.

---

## 🏗️ Build Executable (Optional)
If you want to package the application as a standalone executable (`.exe` on Windows):
1.  Install `pyinstaller`:
    ```bash
    pip install pyinstaller
    ```
2.  Build the bundle:
    ```bash
    pyinstaller --noconsole --onefile tts_bot.py
    ```
3.  The executable will be located in the `dist/` directory.
