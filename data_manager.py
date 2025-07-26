import json
import os
from typing import Dict, List, Any, Optional

class DataManager:
    """Manages data storage and retrieval for movies and partners"""
    
    def __init__(self, movies_file: str, partners_file: str):
        self.movies_file = movies_file
        self.partners_file = partners_file
        self._initialize_files()
    
    def _initialize_files(self):
        """Initialize JSON files if they don't exist"""
        if not os.path.exists(self.movies_file):
            self._save_json(self.movies_file, {})
        
        if not os.path.exists(self.partners_file):
            self._save_json(self.partners_file, [])
    
    def _load_json(self, file_path: str) -> Any:
        """Load data from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {} if file_path == self.movies_file else []
    
    def _save_json(self, file_path: str, data: Any):
        """Save data to JSON file"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    # Movie methods
    def get_movie(self, code: str) -> Optional[Dict[str, Any]]:
        """Get movie by code"""
        movies = self._load_json(self.movies_file)
        return movies.get(code)
    
    def add_movie(self, code: str, title: str, poster: str, episodes: List[str]):
        """Add new movie"""
        movies = self._load_json(self.movies_file)
        movies[code] = {
            "title": title,
            "poster": poster,
            "episodes": episodes
        }
        self._save_json(self.movies_file, movies)
    
    def delete_movie(self, code: str) -> bool:
        """Delete movie by code"""
        movies = self._load_json(self.movies_file)
        if code in movies:
            del movies[code]
            self._save_json(self.movies_file, movies)
            return True
        return False
    
    def get_movies_count(self) -> int:
        """Get total number of movies"""
        movies = self._load_json(self.movies_file)
        return len(movies)
    
    # Partner methods
    def get_partners(self) -> List[str]:
        """Get all partners"""
        return self._load_json(self.partners_file)
    
    def add_partner(self, partner: str):
        """Add new partner"""
        partners = self._load_json(self.partners_file)
        if partner not in partners:
            partners.append(partner)
            self._save_json(self.partners_file, partners)
    
    def delete_partner(self, partner: str) -> bool:
        """Delete partner"""
        partners = self._load_json(self.partners_file)
        if partner in partners:
            partners.remove(partner)
            self._save_json(self.partners_file, partners)
            return True
        return False
    
    def get_partners_count(self) -> int:
        """Get total number of partners"""
        partners = self._load_json(self.partners_file)
        return len(partners)

# Global instance
from config import MOVIES_FILE, PARTNERS_FILE
data_manager = DataManager(MOVIES_FILE, PARTNERS_FILE)
