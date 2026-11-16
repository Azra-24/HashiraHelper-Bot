
# HashiraHelper-Bot: At Your Service

import os
import openai

from dotenv import load_dotenv
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from telegram import Update
from telegram.constants import ParseMode
from moviepy.editor import AudioFileClip
from elevenlabslib import ElevenLabsUser
import pytesseract
from PIL import Image
import fitz  # PyMuPDF for PDFs
from docx import Document as DocxDocument


# --------------------------------------------------
# LOAD API KEYS FROM .ENV FILE
# --------------------------------------------------

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Check whether all API keys are available
if not all([OPENAI_API_KEY, TELEGRAM_API_TOKEN, ELEVENLABS_API_KEY]):
    raise ValueError(
        "Missing API keys! Please configure your .env file."
    )

# Configure OpenAI
openai.api_key = OPENAI_API_KEY


# --------------------------------------------------
# INITIALIZE ELEVENLABS
# --------------------------------------------------

user = ElevenLabsUser(ELEVENLABS_API_KEY)
voice = user.get_voices_by_name("Matilda")[0]


# --------------------------------------------------
# INITIALIZE CONVERSATION HISTORY
# --------------------------------------------------

messages = [
    {
        "role": "system",
        "content": (
            "You are a knowledgeable assistant skilled in a wide range of topics, "
            "including science, technology, history, astronomy, and everyday facts. "
            "Your goal is to provide accurate, informative, and concise responses to any query. "
            "Answer clearly and in a friendly manner. And always call the user sensei and "
            "occasionally use a few common basic Japanese words as you are an anime-themed super chatbot."
        ),
    }
]


# --------------------------------------------------
# DOCUMENT EXTRACTION FUNCTIONS
# --------------------------------------------------

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)


def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text


def extract_text_from_docx(docx_path):
    doc = DocxDocument(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])


# --------------------------------------------------
# HANDLE TEXT MESSAGES
# --------------------------------------------------

async def text_message(update, context):

    user_message = update.message.text.lower()

    await update.message.reply_text(
        "I've received your message! Please give me a second to respond :)"
    )

    if "generate an image of" in user_message:

        image_prompt = user_message.replace(
            "generate an image of", ""
        ).strip()

        try:
            image_response = openai.Image.create(
                prompt=image_prompt,
                n=1,
                size="1024x1024"
            )

            image_url = image_response['data'][0]['url']

            await context.bot.send_photo(
                chat_id=update.message.chat.id,
                photo=image_url
            )

            await update.message.reply_text(
                f"Here is the generated image for: {image_prompt}"
            )

        except Exception:
            await update.message.reply_text(
                "Sorry, there was an issue generating the image. Please try again later."
            )

    else:

        messages.append({
            "role": "user",
            "content": update.message.text
        })

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        response_text = response["choices"][0]["message"]["content"]

        messages.append({
            "role": "assistant",
            "content": response_text
        })

        response_byte_audio = voice.generate_audio_bytes(response_text)

        with open("response_elevenlabs.mp3", "wb") as f:
            f.write(response_byte_audio)

        with open("response_elevenlabs.mp3", "rb") as audio_file:
            await context.bot.send_voice(
                chat_id=update.message.chat.id,
                voice=audio_file
            )

        await update.message.reply_text(
            text=f"[Bot]: {response_text}",
            parse_mode=ParseMode.MARKDOWN
        )


# --------------------------------------------------
# HANDLE VOICE MESSAGES
# --------------------------------------------------

async def voice_message(update, context):

    await update.message.reply_text(
        "I've received a voice message! Please give me a second to respond :)"
    )

    voice_file = await context.bot.get_file(
        update.message.voice.file_id
    )

    await voice_file.download_to_drive("voice_message.ogg")

    audio_clip = AudioFileClip("voice_message.ogg")
    audio_clip.write_audiofile("voice_message.mp3")
    audio_clip.close()

    with open("voice_message.mp3", "rb") as audio_file:
        transcript = openai.Audio.transcribe(
            "whisper-1",
            audio_file
        ).text

    await update.message.reply_text(
        text=f"[You]: {transcript}",
        parse_mode=ParseMode.MARKDOWN
    )

    messages.append({
        "role": "user",
        "content": transcript
    })

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    response_text = response["choices"][0]["message"]["content"]

    response_byte_audio = voice.generate_audio_bytes(response_text)

    with open("response_elevenlabs.mp3", "wb") as f:
        f.write(response_byte_audio)

    with open("response_elevenlabs.mp3", "rb") as audio_file:
        await context.bot.send_voice(
            chat_id=update.message.chat.id,
            voice=audio_file
        )

    await update.message.reply_text(
        text=f"[Bot]: {response_text}",
        parse_mode=ParseMode.MARKDOWN
    )

    messages.append({
        "role": "assistant",
        "content": response_text
    })


# --------------------------------------------------
# HANDLE DOCUMENT UPLOADS
# --------------------------------------------------

async def document_message(update: Update, context):

    await update.message.reply_text(
        "Document received! Extracting text, please wait..."
    )

    document = await context.bot.get_file(
        update.message.document.file_id
    )

    file_name = update.message.document.file_name
    file_extension = file_name.split(".")[-1].lower()

    file_path = "downloaded_document." + file_extension

    await document.download_to_drive(file_path)

    if file_extension == "pdf":

        extracted_text = extract_text_from_pdf(file_path)

    elif file_extension == "docx":

        extracted_text = extract_text_from_docx(file_path)

    elif file_extension in ["jpg", "jpeg", "png"]:

        extracted_text = extract_text_from_image(file_path)

    else:

        await update.message.reply_text(
            "Unsupported document format."
        )
        return

    context.user_data["document_text"] = extracted_text

    await update.message.reply_text(
        "Text extracted successfully! You can ask questions or request a summary."
    )


# --------------------------------------------------
# HANDLE DOCUMENT SUMMARY
# --------------------------------------------------

async def handle_summary(update: Update, context):

    extracted_text = context.user_data.get("document_text")

    if not extracted_text:

        await update.message.reply_text(
            "No document text available. Please upload a document first."
        )
        return

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"Summarize this text: {extracted_text}"
            }
        ]
    )

    summary_text = response["choices"][0]["message"]["content"]

    await update.message.reply_text(summary_text)


# --------------------------------------------------
# HANDLE DOCUMENT QUESTIONS
# --------------------------------------------------

async def handle_ask(update: Update, context):

    extracted_text = context.user_data.get("document_text")

    if not extracted_text:

        await update.message.reply_text(
            "No document text available. Please upload a document first."
        )
        return

    if not context.args:

        await update.message.reply_text(
            "Please provide a question after the /ask command. "
            "Example: /ask What is the document about?"
        )
        return

    question = " ".join(context.args)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": (
                    f"Based on this document: {extracted_text}. "
                    f"Question: {question}"
                )
            }
        ]
    )

    answer_text = response["choices"][0]["message"]["content"]

    await update.message.reply_text(answer_text)


# --------------------------------------------------
# CREATE TELEGRAM BOT APPLICATION
# --------------------------------------------------

application = Application.builder().token(
    TELEGRAM_API_TOKEN
).build()


# --------------------------------------------------
# REGISTER MESSAGE HANDLERS
# --------------------------------------------------

application.add_handler(
    MessageHandler(
        filters.TEXT & (~filters.COMMAND),
        text_message
    )
)

application.add_handler(
    MessageHandler(
        filters.VOICE,
        voice_message
    )
)

application.add_handler(
    MessageHandler(
        filters.Document.ALL,
        document_message
    )
)

application.add_handler(
    CommandHandler("summary", handle_summary)
)

application.add_handler(
    CommandHandler("ask", handle_ask)
)


# --------------------------------------------------
# START BOT
# --------------------------------------------------

if __name__ == "__main__":
    print("HashiraHelper-Bot is starting...")

    application.run_polling()
