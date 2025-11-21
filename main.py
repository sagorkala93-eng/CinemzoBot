#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CINEMZO.COM Telegram Bot - Simplified Working Version
"""

from flask import Flask, request, jsonify
import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
BOT_TOKEN = "8501866882:AAFLjFY-x6svgvnvCeTlNx2_lSpmf91rFtg"
BOT_NAME = "CINEMZO.COM"
BOT_LINK = "https://t.me/CINEMZOBOT"
CHANNEL_USERNAME = "@cinemzo_com"
CHANNEL_LINK = "https://t.me/cinemzo_com"
WEBAPP_URL = "https://cinemzo-com.blogspot.com/?m=1#home-page"
BOT_DESCRIPTION = "Stream free movies & series on Cinemzo.com — updated daily for nonstop entertainment on all devices!"

# Flask app
app = Flask(__name__)

def send_message(chat_id, text, reply_markup=None, parse_mode="Markdown"):
    """Send message via Telegram API"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode
    }
    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)
    
    response = requests.post(url, data=data)
    return response.json()

def send_photo(chat_id, photo, caption, reply_markup=None, parse_mode="Markdown"):
    """Send photo via Telegram API"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    data = {
        "chat_id": chat_id,
        "photo": photo,
        "caption": caption,
        "parse_mode": parse_mode
    }
    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)
    
    response = requests.post(url, data=data)
    return response.json()

def edit_message_text(chat_id, message_id, text, reply_markup=None, parse_mode="Markdown"):
    """Edit message text via Telegram API"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText"
    data = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": parse_mode
    }
    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)
    
    response = requests.post(url, data=data)
    return response.json()

def answer_callback_query(callback_query_id, text=None, show_alert=False):
    """Answer callback query via Telegram API"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery"
    data = {
        "callback_query_id": callback_query_id,
        "show_alert": show_alert
    }
    if text:
        data["text"] = text
    
    response = requests.post(url, data=data)
    return response.json()

def check_channel_membership(user_id):
    """Check if user is a member of the required channel"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember"
        data = {
            "chat_id": CHANNEL_USERNAME,
            "user_id": user_id
        }
        response = requests.post(url, data=data)
        result = response.json()
        
        if result.get("ok"):
            status = result["result"]["status"]
            return status in ["member", "administrator", "creator"]
        return False
    except Exception as e:
        logger.error(f"Error checking membership: {e}")
        return False

def get_movie_data(movie_name):
    """Get movie data (mock implementation)"""
    movies_db = {
        "avatar": {
            "title": "Avatar",
            "year": "2009",
            "rating": "7.9/10",
            "genre": "Action, Adventure, Fantasy",
            "description": "A paraplegic Marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home.",
            "thumbnail": "https://m.media-amazon.com/images/M/MV5BZDA0OGQxNTItMDZkMC00N2UyLTg3MzMtYTJmNjg3Nzk5MzRiXkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_SX300.jpg"
        },
        "titanic": {
            "title": "Titanic",
            "year": "1997",
            "rating": "7.9/10",
            "genre": "Drama, Romance",
            "description": "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic.",
            "thumbnail": "https://m.media-amazon.com/images/M/MV5BMDdmZGU3NDQtY2E5My00ZTliLWIzOTUtMTY4ZGI1YjdiNjk3XkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_SX300.jpg"
        },
        "avengers": {
            "title": "Avengers: Endgame",
            "year": "2019",
            "rating": "8.4/10",
            "genre": "Action, Adventure, Drama",
            "description": "After the devastating events of Avengers: Infinity War, the universe is in ruins. With the help of remaining allies, the Avengers assemble once more.",
            "thumbnail": "https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2NzM@._V1_SX300.jpg"
        }
    }
    
    movie_key = movie_name.lower().strip()
    
    # Search in database
    for key, movie in movies_db.items():
        if key in movie_key or movie_key in key:
            return movie
    
    # Default movie if not found
    return {
        "title": movie_name.title(),
        "year": "2023",
        "rating": "8.0/10",
        "genre": "Action, Drama",
        "description": f"Watch {movie_name} and many more movies on Cinemzo.com! Stream unlimited movies and series.",
        "thumbnail": "https://via.placeholder.com/300x450/1a1a1a/ffffff?text=CINEMZO.COM"
    }

def handle_start_command(chat_id, user_id):
    """Handle /start command"""
    is_member = check_channel_membership(user_id)
    
    if is_member:
        # Show main interface
        keyboard = {
            "inline_keyboard": [
                [{"text": "🎬 Watch", "web_app": {"url": WEBAPP_URL}}]
            ]
        }
        message = f"🎉 **Welcome to CINEMZO.COM!**\n\n{BOT_DESCRIPTION}\n\n🎬 Click 'Watch' to browse movies and series\n🔍 Or send me a movie name to search for it!"
        send_message(chat_id, message, keyboard)
    else:
        # Show join channel message
        keyboard = {
            "inline_keyboard": [
                [{"text": "🔗 Join Channel", "url": CHANNEL_LINK}],
                [{"text": "✅ I Joined", "callback_data": "check_membership"}]
            ]
        }
        message = f"🎬 **Welcome to CINEMZO.COM Bot!**\n\n{BOT_DESCRIPTION}\n\n📢 To access all features, please join our channel first:\n👇 Click the button below to join"
        send_message(chat_id, message, keyboard)

def handle_movie_search(chat_id, user_id, movie_name):
    """Handle movie search"""
    is_member = check_channel_membership(user_id)
    
    if not is_member:
        handle_start_command(chat_id, user_id)
        return
    
    # Search for movie
    movie_data = get_movie_data(movie_name)
    
    if movie_data:
        # Create movie result
        search_query = movie_name.replace(' ', '+')
        movie_url = f"{WEBAPP_URL}?search={search_query}"
        
        keyboard = {
            "inline_keyboard": [
                [{"text": "🎬 Watch Now", "url": movie_url}]
            ]
        }
        
        message = f"🎬 **{movie_data['title']}**\n\n📅 Year: {movie_data['year']}\n⭐ Rating: {movie_data['rating']}\n🎭 Genre: {movie_data['genre']}\n\n📝 {movie_data['description']}"
        
        if movie_data.get('thumbnail'):
            send_photo(chat_id, movie_data['thumbnail'], message, keyboard)
        else:
            send_message(chat_id, message, keyboard)

def handle_callback_query(callback_query):
    """Handle callback queries"""
    query_id = callback_query["id"]
    chat_id = callback_query["message"]["chat"]["id"]
    message_id = callback_query["message"]["message_id"]
    user_id = callback_query["from"]["id"]
    data = callback_query["data"]
    
    if data == "check_membership":
        is_member = check_channel_membership(user_id)
        
        if is_member:
            # Show main interface
            keyboard = {
                "inline_keyboard": [
                    [{"text": "🎬 Watch", "web_app": {"url": WEBAPP_URL}}]
                ]
            }
            message = f"🎉 **Welcome to CINEMZO.COM!**\n\n{BOT_DESCRIPTION}\n\n🎬 Click 'Watch' to browse movies and series\n🔍 Or send me a movie name to search for it!"
            edit_message_text(chat_id, message_id, message, keyboard)
        else:
            answer_callback_query(query_id, "❌ You haven't joined the channel yet. Please join first!", True)
    
    answer_callback_query(query_id)

# Flask routes
@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        "status": "running",
        "bot": "CINEMZO.COM Telegram Bot",
        "message": "Webhook bot is running successfully!",
        "webhook_url": f"{request.host_url}webhook",
        "bot_link": BOT_LINK
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "CINEMZO.COM Bot Webhook API"
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming webhook updates from Telegram"""
    try:
        update_data = request.get_json()
        
        if not update_data:
            return jsonify({"status": "ok"})
        
        logger.info(f"Received update: {update_data.get('update_id', 'unknown')}")
        
        # Handle message
        if "message" in update_data:
            message = update_data["message"]
            chat_id = message["chat"]["id"]
            user_id = message["from"]["id"]
            
            if "text" in message:
                text = message["text"]
                
                if text.startswith("/start"):
                    handle_start_command(chat_id, user_id)
                else:
                    # Movie search
                    handle_movie_search(chat_id, user_id, text)
        
        # Handle callback query
        elif "callback_query" in update_data:
            handle_callback_query(update_data["callback_query"])
        
        return jsonify({"status": "ok"})
        
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return jsonify({"status": "ok"})  # Always return 200 to avoid Telegram retries

@app.route('/set_webhook', methods=['POST'])
def set_webhook():
    """Set webhook URL for the bot"""
    try:
        webhook_url = f"{request.host_url}webhook"
        
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
        data = {"url": webhook_url}
        
        response = requests.post(url, data=data)
        result = response.json()
        
        if result.get("ok"):
            return jsonify({
                "status": "success",
                "message": f"Webhook set to {webhook_url}"
            })
        else:
            return jsonify({
                "status": "error",
                "message": result.get("description", "Failed to set webhook")
            }), 500
            
    except Exception as e:
        logger.error(f"Error setting webhook: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

