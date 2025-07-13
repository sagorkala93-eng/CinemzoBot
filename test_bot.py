#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script for CINEMZO.COM Bot
"""

import sys
import asyncio
from config import BOT_TOKEN, BOT_NAME, CHANNEL_USERNAME, WEBAPP_URL
from movie_search import MovieSearcher

async def test_bot_functionality():
    """Test bot functionality"""
    try:
        print("🔧 Testing bot configuration...")
        print(f"   Bot Token: {BOT_TOKEN[:10]}...")
        print(f"   Bot Name: {BOT_NAME}")
        print(f"   Channel: {CHANNEL_USERNAME}")
        print(f"   WebApp URL: {WEBAPP_URL}")
        print("✅ Configuration loaded successfully!")
        
        print("\n🔧 Testing movie searcher...")
        movie_searcher = MovieSearcher()
        test_movie = await movie_searcher.search_movie("avatar")
        if test_movie:
            print("✅ Movie searcher working!")
            print(f"   Found: {test_movie['title']} ({test_movie['year']})")
        else:
            print("❌ Movie searcher failed!")
            return False
        
        print("\n🔧 Testing movie URL generation...")
        movie_url = movie_searcher.get_movie_url("avatar")
        print(f"   Generated URL: {movie_url}")
        
        print("\n🔧 Testing message formatting...")
        formatted_message = movie_searcher.format_movie_message(test_movie)
        print(f"   Message preview: {formatted_message[:100]}...")
        
        print("\n🎉 All tests passed! Bot is ready to deploy.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == '__main__':
    result = asyncio.run(test_bot_functionality())
    sys.exit(0 if result else 1)

