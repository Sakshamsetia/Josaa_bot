import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from ai import ask_gemini
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import os

# --- Configuration ---
tg_token = os.environ.get("JOSAA_BOT")

# --- Logging Setup ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def teleResponse(user_query: str) -> str:
    resp = ask_gemini(user_query)
    return resp

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hey! I’m your IIT Mandi counsellor bot for JOSAA 2025. Ask me anything about branches, placements, fests, or comparisons I am there for help.\n\nIt is Whatsapp group for IIT Mandi Councelling: https://chat.whatsapp.com/FokoEbUXk6S69Vy9oNaiqo \n If you find my answers insufficient, Use it to connect to students there."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    user_text = update.message.text.strip()
    logging.info(f"User {update.message.chat.id} → {user_text}")
    try:
        answer = teleResponse(user_text)
        await update.message.reply_text(answer)
    except Exception as e:
        logging.error(f"Error while generating response: {e}")
        await update.message.reply_text("Sorry, something went wrong. Please try again.")
        
class KeepAliveHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def start_web_server():
    port = int(os.environ.get("PORT", 10000))  # Render sets $PORT automatically
    server = HTTPServer(("", port), KeepAliveHandler)
    server.serve_forever()

# --- Step 6: Run the Bot ---
if __name__ == '__main__':
    threading.Thread(target=start_web_server).start()
    application = ApplicationBuilder().token(tg_token).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()
