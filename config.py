#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration file for CINEMZO.COM Telegram Bot
"""

# Bot Configuration
BOT_TOKEN = "8198058710:AAFoWHaC2qgsTwMX_DQV9-XXdUnlV-l-cao"
BOT_NAME = "CINEMZO.COM"
BOT_USERNAME = "CINEMZOBOT"
BOT_LINK = "https://t.me/CINEMZOBOT"
BOT_DESCRIPTION = "Stream free movies & series on Cinemzo.com — updated daily for nonstop entertainment on all devices!"

# Channel Configuration
CHANNEL_USERNAME = "@cinemzo_com"  # Channel username with @
CHANNEL_LINK = "https://t.me/cinemzo_com"

# Web App Configuration
WEBAPP_URL = "https://cinemzo-com.blogspot.com/?m=1#home-page"

# Messages
WELCOME_MESSAGE = """🎬 **Welcome to CINEMZO.COM Bot!**

{description}

📢 To access all features, please join our channel first:
👇 Click the button below to join"""

MAIN_INTERFACE_MESSAGE = """🎉 **Welcome to CINEMZO.COM!**

{description}

🎬 Click 'Watch' to browse movies and series
🔍 Or send me a movie name to search for it!"""

JOIN_REQUIRED_MESSAGE = """❌ You need to join our channel first to use this bot!

Please join: {channel_link}
Then click 'I Joined' button."""

MOVIE_NOT_FOUND_MESSAGE = "❌ Sorry, couldn't find '{movie_name}'. Try a different title!"

SEARCH_ERROR_MESSAGE = "❌ An error occurred while searching. Please try again!"

# Movie Search Configuration
ENABLE_MOCK_SEARCH = True  # Set to False when implementing real search
DEFAULT_MOVIE_THUMBNAIL = "https://via.placeholder.com/300x450/1a1a1a/ffffff?text=CINEMZO.COM"

