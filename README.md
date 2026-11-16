
 HashiraHelper-Bot: At Your Service

HashiraHelper-Bot is an anime-themed AI-powered Telegram voice chatbot developed using Python. It provides interactive conversations, voice-based communication, AI image generation, and document processing capabilities.

Developed as a team project for **SEEKH-24 Project Expo**, held at Gokaraju Lailavathi Women's Engineering College on November 16, 2024.

## Features

- **AI-Powered Conversations:** Provides informative responses to user queries using OpenAI's GPT model.
- **Voice Interaction:** Accepts voice messages, converts speech into text using OpenAI Whisper, and generates voice responses using ElevenLabs.
- **AI Image Generation:** Generates images based on user-provided text prompts.
- **Document Processing:** Extracts text from PDF, DOCX, and image files using PyMuPDF, python-docx, and Tesseract OCR.
- **Document Summarization:** Generates concise summaries of uploaded documents.
- **Document Question Answering:** Allows users to ask questions based on uploaded document content through the `/ask` command.
- **Anime-Themed Personality:** Provides friendly responses with an anime-inspired conversational style.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Telegram Bot API | Chatbot interface and communication |
| OpenAI GPT | AI-powered conversations |
| OpenAI Whisper | Voice-to-text transcription |
| OpenAI Image API | AI image generation |
| ElevenLabs | Text-to-speech voice generation |
| PyMuPDF | PDF text extraction |
| python-docx | DOCX text extraction |
| Tesseract OCR | Text extraction from images |
| Pillow | Image processing |
| MoviePy | Audio conversion |
| python-telegram-bot | Telegram bot integration |
| python-dotenv | Secure API key management |

## Project Structure

```text
HashiraHelper-Bot/
│
├── bot.py                  # Main chatbot application
│
├── .env                    # Stores API keys (not uploaded to GitHub)
│
├── .env.example            # Example environment variables
│
├── .gitignore              # Excludes sensitive and unnecessary files
│
├── requirements.txt        # Python dependencies
│
└── README.md               # Project documentation
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/HashiraHelper-Bot.git
```

### 2. Navigate to the Project Directory

```bash
cd HashiraHelper-Bot
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows:**
```bash
venv\Scripts\activate
```

**Linux / macOS:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the root directory and add your API credentials:

```env
OPENAI_API_KEY=your_openai_api_key
TELEGRAM_API_TOKEN=your_telegram_bot_token
ELEVENLABS_API_KEY=your_elevenlabs_api_key
```

Obtain the required API keys from:

- OpenAI: https://platform.openai.com/api-keys
- Telegram: https://t.me/BotFather
- ElevenLabs: https://elevenlabs.io/

**Note:** Never upload your `.env` file or expose your API credentials publicly.

### 6. Install Tesseract OCR

Tesseract OCR is required for extracting text from uploaded images.

Download it from:
https://github.com/tesseract-ocr/tesseract

Ensure Tesseract is installed and accessible through your system PATH.

### 7. Run the Bot

```bash
python bot.py
```

The bot will start polling for incoming Telegram messages.

## Telegram Bot Commands

| Command | Description |
|---|---|
| `/summary` | Summarizes the uploaded document |
| `/ask <question>` | Answers questions based on the uploaded document |

## Supported File Formats

| File Format | Functionality |
|---|---|
| PDF | Text extraction, summarization, and question answering |
| DOCX | Text extraction, summarization, and question answering |
| JPG / JPEG | OCR-based text extraction |
| PNG | OCR-based text extraction |

## Team Members

- **Shaik Azra Anisha**
- Ridhima Reddy Challa
- Vyshnavi Podila

## Project Expo

**Event:** SEEKH-24 – Project Expo  
**Institution:** Gokaraju Lailavathi Women's Engineering College  
**Date:** November 16, 2024

## Future Enhancements

- Improve conversation memory and context management.
- Add support for more document formats.
- Enhance document processing for large files.
- Improve error handling and response performance.
- Integrate additional AI-powered features.

## Acknowledgements

We would like to thank our institution, faculty members, and teammates for their guidance, support, and collaboration throughout the development of this project.
