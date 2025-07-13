#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Movie search functionality for CINEMZO.COM Bot
"""

import requests
import json
import logging
from typing import Dict, Optional
from config import ENABLE_MOCK_SEARCH, DEFAULT_MOVIE_THUMBNAIL, WEBAPP_URL

logger = logging.getLogger(__name__)

class MovieSearcher:
    def __init__(self):
        self.mock_movies_db = self._load_mock_movies()
    
    def _load_mock_movies(self) -> Dict:
        """Load mock movie database for testing"""
        return {
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
            },
            "spider-man": {
                "title": "Spider-Man: No Way Home",
                "year": "2021",
                "rating": "8.2/10",
                "genre": "Action, Adventure, Fantasy",
                "description": "With Spider-Man's identity now revealed, Peter asks Doctor Strange for help. When a spell goes wrong, dangerous foes from other worlds start to appear.",
                "thumbnail": "https://m.media-amazon.com/images/M/MV5BZWMyYzFjYTYtNTRjYi00OGExLWE2YzgtOGRmYjAxZTU3NzBiXkEyXkFqcGdeQXVyMzQ0MzA0NTM@._V1_SX300.jpg"
            },
            "batman": {
                "title": "The Batman",
                "year": "2022",
                "rating": "7.8/10",
                "genre": "Action, Crime, Drama",
                "description": "When a sadistic serial killer begins murdering key political figures in Gotham, Batman is forced to investigate the city's hidden corruption.",
                "thumbnail": "https://m.media-amazon.com/images/M/MV5BMDdmMTBiNTYtMDIzNi00NGVlLWIzMDYtZTk3MTQ3NGQxZGEwXkEyXkFqcGdeQXVyMzMwOTU5MDk@._V1_SX300.jpg"
            },
            "john wick": {
                "title": "John Wick: Chapter 4",
                "year": "2023",
                "rating": "7.7/10",
                "genre": "Action, Crime, Thriller",
                "description": "John Wick uncovers a path to defeating The High Table. But before he can earn his freedom, Wick must face off against a new enemy.",
                "thumbnail": "https://m.media-amazon.com/images/M/MV5BMDExZGMyOTMtMDgyYi00NGIwLWJhMTEtOTdkZGFjNmZiMTEwXkEyXkFqcGdeQXVyMjM4NTM5NDY@._V1_SX300.jpg"
            },
            "fast": {
                "title": "Fast X",
                "year": "2023",
                "rating": "5.8/10",
                "genre": "Action, Adventure, Crime",
                "description": "Dom Toretto and his family are targeted by the vengeful son of drug kingpin Hernan Reyes.",
                "thumbnail": "https://m.media-amazon.com/images/M/MV5BNzVlYzk0NDMtYzFhMy00ZGY2LWE3NmEtOWU4OTI3ZGY4NGNlXkEyXkFqcGdeQXVyMTUzNTgzNzM0._V1_SX300.jpg"
            },
            "oppenheimer": {
                "title": "Oppenheimer",
                "year": "2023",
                "rating": "8.3/10",
                "genre": "Biography, Drama, History",
                "description": "The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb.",
                "thumbnail": "https://m.media-amazon.com/images/M/MV5BMDBmYTZjNjUtN2M1MS00MTQ2LTk2ODgtNzc2M2QyZGE5NTVjXkEyXkFqcGdeQXVyNzAwMjU2MTY@._V1_SX300.jpg"
            },
            "barbie": {
                "title": "Barbie",
                "year": "2023",
                "rating": "6.9/10",
                "genre": "Adventure, Comedy, Fantasy",
                "description": "Barbie and Ken are having the time of their lives in the colorful and seemingly perfect world of Barbie Land.",
                "thumbnail": "https://m.media-amazon.com/images/M/MV5BNjU3N2QxNzYtMjk1NC00MTc4LTk1NTQtMmUxNTljM2I0NDA5XkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_SX300.jpg"
            },
            "interstellar": {
                "title": "Interstellar",
                "year": "2014",
                "rating": "8.7/10",
                "genre": "Adventure, Drama, Sci-Fi",
                "description": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
                "thumbnail": "https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg"
            }
        }
    
    async def search_movie(self, movie_name: str) -> Optional[Dict]:
        """Search for a movie by name"""
        try:
            if ENABLE_MOCK_SEARCH:
                return await self._mock_search(movie_name)
            else:
                return await self._real_search(movie_name)
        except Exception as e:
            logger.error(f"Error searching for movie '{movie_name}': {e}")
            return None
    
    async def _mock_search(self, movie_name: str) -> Optional[Dict]:
        """Mock search function for testing"""
        movie_key = movie_name.lower().strip()
        
        # Search in mock database
        for key, movie in self.mock_movies_db.items():
            if key in movie_key or movie_key in key:
                return movie
        
        # Check if any word in movie name matches
        movie_words = movie_key.split()
        for word in movie_words:
            if len(word) > 2:  # Only check words longer than 2 characters
                for key, movie in self.mock_movies_db.items():
                    if word in key or word in movie['title'].lower():
                        return movie
        
        # If no match found, return a generic result
        return {
            "title": movie_name.title(),
            "year": "2023",
            "rating": "8.0/10",
            "genre": "Action, Drama",
            "description": f"Watch {movie_name} and many more movies on Cinemzo.com! Stream unlimited movies and series.",
            "thumbnail": DEFAULT_MOVIE_THUMBNAIL
        }
    
    async def _real_search(self, movie_name: str) -> Optional[Dict]:
        """Real search function - implement actual website scraping/API here"""
        # TODO: Implement actual search logic
        # This could involve:
        # 1. Scraping the cinemzo website
        # 2. Using their API if available
        # 3. Searching their database
        
        # For now, fallback to mock search
        logger.warning("Real search not implemented, falling back to mock search")
        return await self._mock_search(movie_name)
    
    def get_movie_url(self, movie_name: str) -> str:
        """Generate movie URL for the website"""
        search_query = movie_name.replace(' ', '+')
        return f"{WEBAPP_URL}?search={search_query}"
    
    def format_movie_message(self, movie_data: Dict) -> str:
        """Format movie data into a message"""
        return f"🎬 **{movie_data['title']}**\n\n" \
               f"📅 Year: {movie_data['year']}\n" \
               f"⭐ Rating: {movie_data['rating']}\n" \
               f"🎭 Genre: {movie_data['genre']}\n\n" \
               f"📝 {movie_data['description']}"

