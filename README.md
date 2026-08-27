[README.md](https://github.com/user-attachments/files/31525812/README.md)
# BUJJI AI Assistant

BUJJI is a Windows desktop voice assistant written in Python. It listens through a microphone, transcribes speech with Faster-Whisper, and can open applications, websites, and Google searches from spoken commands. The project also contains an AI manager and intent router that can use Groq or a local Ollama model for natural-language requests.

## Features

- Speech-to-text with Faster-Whisper
- Microphone recording, voice activity detection, and wake-word support
- Windows application launching
- Website opening and Google search
- Text-to-speech responses with Edge TTS
- Optional Groq API and Ollama AI backends
- Modular `voice`, `brain`, and `actions` packages

## Requirements

- Windows 10 or later
- Python 3.10 or newer
- A working microphone
- An NVIDIA GPU with CUDA support for the current Faster-Whisper configuration
- Internet access for Edge TTS and optional Groq requests
- [Ollama](https://ollama.com/) if using the local AI fallback

The current audio configuration uses microphone device `12`, a 48 kHz capture rate, and the Faster-Whisper `small` model on CUDA with `float16` compute. Update the constants in [`voice/whisper.py`](voice/whisper.py) if your hardware or microphone differs.

## Installation

1. Clone or download the project and open a terminal in its root directory.
2. Create and activate a virtual environment:

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Install the Python dependencies:

   ```powershell
   python -m pip install --upgrade pip
   python -m pip install numpy scipy sounddevice faster-whisper edge-tts pygame python-dotenv ollama groq google-genai
   ```

   `sounddevice` may require an installed PortAudio-compatible audio device. On Windows, install the package in the active virtual environment and confirm that your microphone is available to Python.

4. If you want local AI responses, install Ollama and download the configured model:

   ```powershell
   ollama pull llama3.2:3b
   ```

## Configuration

Create a `.env` file in the project root. Never commit real keys to source control.

```env
GROQ_API_KEY=your_groq_api_key
GEMINI_API_KEY=your_gemini_api_key
```

`GROQ_API_KEY` is optional. When present, BUJJI tries Groq first and falls back to Ollama. Ollama is always expected by the current `AIManager` fallback path. `GEMINI_API_KEY` is used by the separate Gemini integration in [`brain/ai.py`](brain/ai.py).

If an API key has ever been shared publicly or committed, revoke it and create a replacement.

## Running BUJJI

Activate the virtual environment and run:

```powershell
python main.py
```

The default entry point initializes Faster-Whisper and the command handler, then continuously listens for speech. Press `Ctrl+C` to stop.

Example commands:

```text
Open Chrome
Open YouTube
Open Notepad
Open Calculator
Search Python tutorials
Search for today's news
Exit
```

Supported website shortcuts include YouTube, Google, Gmail, GitHub, ChatGPT, Instagram, and Facebook. Supported Windows actions include File Explorer, Command Prompt, PowerShell, Task Manager, and Settings.

## Project structure

```text
.
├── main.py                  # Default application entry point
├── actions/
│   ├── command_handler.py   # Parses commands and dispatches actions
│   ├── app_index.py         # Application discovery and launching
│   ├── apps.py              # Windows application helpers
│   ├── browser.py           # Browser shortcuts
│   ├── system.py            # Windows system actions
│   └── applications.json    # Application metadata
├── brain/
│   ├── ai_manager.py        # Groq/Ollama provider selection
│   ├── router.py            # AI intent classification
│   ├── controller.py         # Voice pipeline controller
│   └── config.py            # Environment configuration
├── voice/
│   ├── microphone.py        # Microphone capture
│   ├── vad.py               # Voice activity detection
│   ├── whisper.py           # Faster-Whisper transcription
│   ├── wakeword.py          # Wake-word handling
│   └── speak.py             # Edge TTS playback
└── tests/                   # Unit and component tests
```

## Testing

Run the test suite with:

```powershell
python -m unittest discover -s tests
```

Tests that access a microphone, GPU, speech services, or external APIs may require the corresponding hardware or service configuration.

## Troubleshooting

- **Faster-Whisper cannot initialize:** verify CUDA, NVIDIA drivers, and the `small` model requirements. For CPU-only systems, change `DEVICE` and `COMPUTE_TYPE` in `voice/whisper.py`.
- **No microphone input:** check the `MIC_DEVICE` index and Windows microphone permissions.
- **Ollama errors:** ensure Ollama is running and `llama3.2:3b` is installed.
- **No spoken response:** verify internet access for Edge TTS and audio output availability.
- **Application does not open:** confirm the application is installed and that its executable is discoverable on `PATH`.

## License

No license file is currently included. Add a license before distributing the project.
