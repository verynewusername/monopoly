# FILE: piece.py
# Date: 2025-03-08
# Author: Efe Gorkem Sirin
# Description: This file contains the Piece class which represents a piece in the game.

class Piece:
    # Class variable to keep track of existing pieces by name
    _instances = {}

    def __new__(cls, name):
        # Check if the piece with the given name already exists
        if name in cls._instances:
            raise ValueError(f"Piece with name '{name}' already exists.")
        else:
            # Create a new instance if it doesn't exist
            instance = super().__new__(cls)
            cls._instances[name] = instance  # Store the instance by name
            return instance

    def __init__(self, name):
        # Initialize the instance only if it's not already initialized
        if not hasattr(self, 'name'):  # To avoid re-initialization
            self.name = name
            self.position = 0

    def move_to(self, position):
        self.position = position
        print(f"{self.name} moved to position {position}.")

    @classmethod
    def reset(cls):
        """Deletes all stored instances and allows recreation."""
        cls._instances.clear()

# END OF FILE - piece.py