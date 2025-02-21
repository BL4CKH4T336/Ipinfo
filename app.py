import requests
import random
import hashlib
import base64
import json
import os
import pyqrcode
import io
import threading
from gtts import gTTS
from flask import Flask, jsonify
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, CallbackContext

# Replace with your bot token
BOT_TOKEN = "7952215311:AAFeEJHu7TuwXDGezvlDJUxkGTheM14ipGs"

# Initialize Flask
app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({"status": "OK"})

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("👋 Welcome to the Ultimate MultiTool Bot! Use /help to see available commands. ⚡")

async def help_command(update: Update, context: CallbackContext) -> None:
    help_text = """📌 *Available Commands:*
🔠 /reverse <text> - Reverse text
📝 /wordcount <text> - Count words & characters
🔊 /tts <text> - Convert text to speech
📸 /qr <text> - Generate QR code
📄 /filetotext - Convert file to text
🔐 /b64encode <text> - Base64 encode
🔓 /b64decode <text> - Base64 decode
🔑 /password <length> - Generate strong password
🌍 /ipinfo <IP> - Get IP details
🔒 /hash <text> <algorithm> - Generate hash
🤣 /joke - Get a random joke
💡 /fact - Get a fun fact
📜 /quote - Get a motivational quote
🎲 /roll - Roll a dice
🤖 /choose <option1> <option2> ... - Random decision maker
🧮 /calc <expression> - Solve math problems
📏 /convert <value> <unit1> <unit2> - Convert units
💰 /currency <amount> <from> <to> - Convert currency
🌐 /whois <domain> - WHOIS lookup
📶 /ping <website> - Ping a website"""
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def reverse_text(update: Update, context: CallbackContext) -> None:
    text = " ".join(context.args)
    await update.message.reply_text(f"🔄 Reversed: {text[::-1]}")

async def generate_qr(update: Update, context: CallbackContext) -> None:
    text = " ".join(context.args)
    qr = pyqrcode.create(text)
    buffer = io.BytesIO()
    qr.png(buffer, scale=5)
    buffer.seek(0)
    await update.message.reply_photo(photo=InputFile(buffer, filename="qrcode.png"))

async def base64_encode(update: Update, context: CallbackContext) -> None:
    text = " ".join(context.args)
    encoded = base64.b64encode(text.encode()).decode()
    await update.message.reply_text(f"🔐 Base64 Encoded: `{encoded}`", parse_mode="Markdown")

async def base64_decode(update: Update, context: CallbackContext) -> None:
    text = " ".join(context.args)
    decoded = base64.b64decode(text.encode()).decode()
    await update.message.reply_text(f"🔓 Base64 Decoded: `{decoded}`", parse_mode="Markdown")

async def generate_password(update: Update, context: CallbackContext) -> None:
    length = int(context.args[0]) if context.args else 12
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()"
    await update.message.reply_text(f"🔑 Generated Password: `{''.join(random.choices(chars, k=length))}`", parse_mode="Markdown")

async def ip_lookup(update: Update, context: CallbackContext) -> None:
    ip = " ".join(context.args)
    response = requests.get(f"http://ip-api.com/json/{ip}").json()
    await update.message.reply_text(f"🌍 *IP Info:* `{json.dumps(response, indent=4)}`", parse_mode="Markdown")

async def generate_hash(update: Update, context: CallbackContext) -> None:
    text = " ".join(context.args[:-1])
    algo = context.args[-1].lower()
    if algo in hashlib.algorithms_available:
        hashed = hashlib.new(algo, text.encode()).hexdigest()
        await update.message.reply_text(f"🔒 {algo.upper()} Hash: `{hashed}`", parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ Unsupported hash algorithm!")

async def joke(update: Update, context: CallbackContext) -> None:
    jokes = ["Why don't skeletons fight? They don’t have the guts!", "Parallel lines have so much in common. It’s a shame they’ll never meet."]
    await update.message.reply_text(f"🤣 {random.choice(jokes)}")

async def fact(update: Update, context: CallbackContext) -> None:
    facts = ["Octopuses have three hearts!", "Bananas are berries, but strawberries aren't."]
    await update.message.reply_text(f"💡 {random.choice(facts)}")

async def quote(update: Update, context: CallbackContext) -> None:
    quotes = ["Believe in yourself!", "The only limit is your mind."]
    await update.message.reply_text(f"📜 {random.choice(quotes)}")

async def roll_dice(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(f"🎲 You rolled a {random.randint(1, 6)}!")

async def choose(update: Update, context: CallbackContext) -> None:
    options = context.args
    await update.message.reply_text(f"🤖 I choose: {random.choice(options)}")

def run_flask():
    """Run Flask in a separate thread"""
    app.run(host="0.0.0.0", port=8000)

def main():
    bot = Application.builder().token(BOT_TOKEN).build()

    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CommandHandler("help", help_command))
    bot.add_handler(CommandHandler("reverse", reverse_text))
    bot.add_handler(CommandHandler("qr", generate_qr))
    bot.add_handler(CommandHandler("b64encode", base64_encode))
    bot.add_handler(CommandHandler("b64decode", base64_decode))
    bot.add_handler(CommandHandler("password", generate_password))
    bot.add_handler(CommandHandler("ipinfo", ip_lookup))
    bot.add_handler(CommandHandler("hash", generate_hash))
    bot.add_handler(CommandHandler("joke", joke))
    bot.add_handler(CommandHandler("fact", fact))
    bot.add_handler(CommandHandler("quote", quote))
    bot.add_handler(CommandHandler("roll", roll_dice))
    bot.add_handler(CommandHandler("choose", choose))

    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    print("🚀 Bot & Flask Running!")
    bot.run_polling()

if __name__ == "__main__":
    main()
