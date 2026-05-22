import json
import os
from settings import HIGHSCORE_FILE

class ScoreManager:
    """Handles saving and loading high scores to/from JSON"""

    MAX_SCORES = 5 

    def __init__(self):
        self.scores = self._load()

    #public API
    def save(self, name:str, score:int) -> None:
        """Add a new score, keep top MAX_SCORES, persist. """
        entry = {"name": name, "score": score}
        self.scores.append(entry)
        self.scores.sort(key=lambda e: e["score"], reverse=True)
        self.scores = self.scores[:self.MAX_SCORES]
        self._persist() 
    
    def get_top(self) -> list:
        return self.scores
    def get_high(self) -> int:
        return self.scores[0]["score"] if self.scores else 0
    
    #private
    def _load(self) -> list:
        """Read scores from JSON. Returns [] on any error """
        try:
            if not os.path.exists(HIGHSCORE_FILE):
                return[]
            with open(HIGHSCORE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    raise ValueError("Unexpected format")
                return data 
        except (json.JSONDecodeError, ValueError, OSError) as e:
            print(f"[ScoreManager] Could not load scores: {e}")
            return []
        
    def _persist(self) -> None:
        """Write scores to JSON. Silently handles errors. """
        try:
            os.makedirs(os.path.dirname(HIGHSCORE_FILE), exist_ok=True)
            with open(HIGHSCORE_FILE, "w", encoding="utf-8") as f:
                json.dump(self.scores, f, indent=2, ensure_ascii=False)
        except OSError as e:
            print(f"[ScoreManager]Could not save scores: {e}")

        

