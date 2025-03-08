# FILE: bank.py
# Date: 2025-03-08
# Author: Efe Gorkem Sirin
# Description: This file contains the Bank class which represents the bank in the Monopoly game.

import random 
from constants import CHANCE_CARDS, COMMUNITY_CHEST_CARDS, PROPERTY_NAMES
from property import Property

class Bank:
    def __init__(self, seed=None):
        self.type = "BANK"
        self.tax_accumulated = 0
        self.unowned_properties = [Property(name) for name in PROPERTY_NAMES]
        self.chance_cards = CHANCE_CARDS.copy()
        self.community_chest_cards = COMMUNITY_CHEST_CARDS.copy()

        if seed is not None:
            random.seed(seed)

        random.shuffle(self.chance_cards)
        random.shuffle(self.community_chest_cards)

        # print("Bank created.")
        # print(f"Chance cards: {self.chance_cards}")
        # print(f"Community chest cards: {self.community_chest_cards}")
        # print(f"Unowned properties: {self.unowned_properties}")

    def reset(self):
        self.tax_accumulated = 0
        self.unowned_properties = [Property(name) for name in PROPERTY_NAMES]
        random.shuffle(self.chance_cards)
        random.shuffle(self.community_chest_cards)

    def collected_taxes(self, amount):
        self.tax_accumulated += amount

    def get_accumulated_tax(self):
        return self.tax_accumulated
    
    def reset_accumulated_tax(self):
        self.tax_accumulated = 0

    def has_the_property(self, name) -> bool:
        return name in [property.name for property in self.unowned_properties]
    
    def get_property_price(self, name):
        for property in self.unowned_properties:
            if property.name == name:
                return property.price
        raise ValueError(f"Property {name} not found in the bank.")
    
    def take_property(self, name):
        for property in self.unowned_properties:
            if property.name == name:
                self.unowned_properties.remove(property)
                return property
        raise ValueError(f"Property {name} not found in the bank.")

    def get_a_chance_card(self, player):
        # Return the top card from the deck and put it at the bottom
        card = self.chance_cards.pop(0)
        self.chance_cards.append(card)
        # Return it
        return card

    def get_a_community_chest_card(self, player):
        # Return the top card from the deck and put it at the bottom
        card = self.community_chest_cards.pop(0)
        self.community_chest_cards.append(card)
        # Return it
        return card
    
    def get_property_deck(self):
        properties = self.unowned_properties.copy()
        self.unowned_properties = []
        return properties
    
    def print_information(self):
        print("Bank information:")
        print(f"\tTax accumulated: {self.tax_accumulated}")
        # for card in self.chance_cards:
        #     print(f"Chance card: {card['text']}")
        # for card in self.community_chest_cards:
        #     print(f"Community chest card: {card['text']}")
        print("\tUnowned properties:")
        for property in self.unowned_properties:
            print(f"\tUnowned property: {property.print_information()}")
        print()

# END OF FILE - bank.py