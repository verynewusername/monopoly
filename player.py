from constants import START_MONEY, PROPERTY_NAMES, NUM_SQUARES
from piece import Piece

class Player:
    def __init__(self, name, pieceName):
        self.name = name
        self.piece = Piece(pieceName)
        self.money = START_MONEY
        self.properties = []
        self.in_jail = False
        self.jail_turns = 0
        self.bankrupt = False
        self.logic = "DEFAULT"
    
    def has_both_utilities(self) -> bool:
        return all(prop in self.properties for prop in [PROPERTY_NAMES[7], PROPERTY_NAMES[22]])

    def deduct_money(self, amount) -> bool:
        self.money -= amount
        if self.money < 0:
            if self.handle_bankruptcy(amount):
                assert self.money >= 0
                return True
            else:
                print(f"{self.name} is bankrupt!")
                self.bankrupt = True
                return False
        return True
    
    def is_bankrupt(self) -> bool:
        return self.bankrupt
    
    def handle_bankruptcy(self, needed_money) -> bool:
        # TODO implement this method
        return False
    
    def get_money(self, amount):
        self.money += amount

    def move(self, steps):
        self.piece.position = (self.piece.position + steps) % NUM_SQUARES

    def calculate_rent(self, property_name, dice_roll):
        for property in self.properties:
            if property.name == property_name:
                return property.calculate_rent(dice_roll, self.has_both_utilities())
        raise ValueError(f"{self.name} does not own {property_name}.")

    def get_position(self):
        return self.piece.position
    
    def wants_to_buy_property(self, property_name,property_price) -> bool:
        if self.logic == "DEFAULT":
            if self.money >= property_price:
                return True
            else:
                return False
        else:
            raise ValueError("Invalid logic type.")

    def go_to_jail(self):
        self.piece.position = 10
        self.in_jail = True
        self.jail_turns = 0

    def has_properties(self) -> bool:
        return len(self.properties) > 0

    def remove_all_properties(self) -> []:
        properties = self.properties
        self.properties = []
        return properties

