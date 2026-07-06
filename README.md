# Text-to-Speech Bot (Python)

A desktop GUI application that converts typed text into speech using offline speech synthesis.

## Features
- Text input area for typing/pasting content
- Voice selection dropdown (lists all system-installed voices)
- Adjustable speech rate slider
- Speak and Stop controls
- Non-blocking UI (speech runs on a background thread)

## Tech Stack
- **Language:** Python 3
- **GUI:** Tkinter
- **Speech Engine:** pyttsx3 (offline, no internet/API key required)

## How to Run
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Run the app:
   ```
   python tts_bot.py
   ```

## Notes
- On Windows, pyttsx3 uses the built-in SAPI5 voices (e.g. Microsoft David, Microsoft Zira).
- On Linux, install `espeak-ng` for voice support: `sudo apt install espeak-ng`.
