#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CINEMZO.COM Telegram Bot - Webhook Implementation
"""

from flask import Flask, request, jsonify
import asyncio
import logging
import json
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Import configuration and modules
from config import *
from movie_search import MovieSearcher

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Flask app
app = Flask(__name__)

# Global bot application
bot_application = None
movie_searcher = MovieSearcher()

def setup_bot():
    """Setup bot application"""
    global bot_application
    if bot_application is None:
        bot_application = Application.builder().token(BOT_TOKEN).build()
        
        # Add handlers
        bot_application.add_handler(CommandHandler("start", start_command))
        bot_application.add_handler(CallbackQueryHandler(button_callback))
        bot_application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_movie_search))
        
        logger.info("Bot application setup completed")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command"""
    user = update.effective_user
    logger.info(f"Start command from user: {user.id} ({user.username})")
    
    # Check if user is already a member of the channel
    is_member = await check_channel_membership(user.id, context)
    
    if is_member:
        # User is already a member, show the main interface
        await show_main_interface(update, context)
    else:
        # User is not a member, show join channel message
        await show_join_channel_message(update, context)

async def check_channel_membership(user_id, context):
    """Check if user is a member of the required channel"""
    try:
        chat_member = await context.bot.get_chat_member(
            chat_id=CHANNEL_USERNAME, 
            user_id=user_id
        )
        is_member = chat_member.status in ['member', 'administrator', 'creator']
        logger.info(f"Channel membership check for user {user_id}: {is_member}")
        return is_member
    except Exception as e:
        logger.error(f"Error checking channel membership: {e}")
        return False

async def show_join_channel_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show message asking user to join the channel"""
    keyboard = [
        [InlineKeyboardButton("🔗 Join Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("✅ I Joined", callback_data="check_membership")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = WELCOME_MESSAGE.format(description=BOT_DESCRIPTION)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            text=message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            text=message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

async def show_main_interface(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show the main interface with Watch button"""
    keyboard = [
        [InlineKeyboardButton("🎬 Watch", web_app=WebAppInfo(url=WEBAPP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = MAIN_INTERFACE_MESSAGE.format(description=BOT_DESCRIPTION)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            text=message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            text=message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "check_membership":
        user_id = query.from_user.id
        is_member = await check_channel_membership(user_id, context)
        
        if is_member:
            await show_main_interface(update, context)
        else:
            await query.answer("❌ You haven't joined the channel yet. Please join first!", show_alert=True)

async def handle_movie_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle movie search requests"""
    user = update.effective_user
    movie_name = update.message.text.strip()
    
    logger.info(f"Movie search request from user {user.id}: '{movie_name}'")
    
    # Check if user is a member of the channel
    is_member = await check_channel_membership(user.id, context)
    
    if not is_member:
        await show_join_channel_message(update, context)
        return
    
    # Process movie search
    await search_and_send_movie(update, context, movie_name)

async def search_and_send_movie(update: Update, context: ContextTypes.DEFAULT_TYPE, movie_name: str):
    """Search for movie and send result"""
    try:
        # Send "searching" message
        searching_msg = await update.message.reply_text(f"🔍 Searching for '{movie_name}'...")
        
        # Search for movie using the movie searcher
        movie_data = await movie_searcher.search_movie(movie_name)
        
        if movie_data:
            # Create movie result message
            movie_url = movie_searcher.get_movie_url(movie_name)
            keyboard = [
                [InlineKeyboardButton("🎬 Watch Now", url=movie_url)]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            message = movie_searcher.format_movie_message(movie_data)
            
            # Delete searching message
            await searching_msg.delete()
            
            # Send movie result
            if movie_data.get('thumbnail'):
                await update.message.reply_photo(
                    photo=movie_data['thumbnail'],
                    caption=message,
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
            else:
                await update.message.reply_text(
                    text=message,
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
        else:
            await searching_msg.edit_text(MOVIE_NOT_FOUND_MESSAGE.format(movie_name=movie_name))
            
    except Exception as e:
        logger.error(f"Error in movie search: {e}")
        await update.message.reply_text(SEARCH_ERROR_MESSAGE)

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
        # Setup bot if not already done
        setup_bot()
        
        # Get update data
        update_data = request.get_json()
        
        if update_data:
            logger.info(f"Received webhook update: {update_data.get('update_id', 'unknown')}")
            
            # Create Update object
            update = Update.de_json(update_data, bot_application.bot)
            
            # Process update in a new event loop
            def process_update():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    loop.run_until_complete(bot_application.process_update(update))
                finally:
                    loop.close()
            
            # Run in a separate thread to avoid blocking
            thread = threading.Thread(target=process_update)
            thread.start()
            
        return jsonify({"status": "ok"})
    except Exception as e:
        logger.error(f"Error processing webhook: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/set_webhook', methods=['POST'])
def set_webhook():
    """Set webhook URL for the bot"""
    try:
        webhook_url = f"{request.host_url}webhook"
        
        # Setup bot
        setup_bot()
        
        # Set webhook
        def _set_webhook():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(bot_application.bot.set_webhook(url=webhook_url))
                return result
            finally:
                loop.close()
        
        result = _set_webhook()
        
        if result:
            return jsonify({
                "status": "success",
                "message": f"Webhook set to {webhook_url}"
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Failed to set webhook"
            }), 500
            
    except Exception as e:
        logger.error(f"Error setting webhook: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    # Setup bot
    setup_bot()
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)

