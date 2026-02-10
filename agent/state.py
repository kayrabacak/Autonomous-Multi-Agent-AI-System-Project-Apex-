# agent/state.py
from typing import List, Dict, Any

class AgentState:
    def __init__(self):
        self.plan: List[str] = []     # Planner'dan gelen liste
        self.current_step_index: int = 0  # Kaçıncı adımdayız?
        self.memory: Dict[str, Any] = {} # Toplanan veriler (Örn: borsa verisi)
        self.history: List[str] = []  # Yapılan işlemlerin logu

    def get_current_step(self):
        if self.current_step_index < len(self.plan):
            return self.plan[self.current_step_index]
        return None

    def update_memory(self, key, value):
        self.memory[key] = value
        
    def next_step(self):
        self.current_step_index += 1