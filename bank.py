import random 
from constants import CHANCE_CARDS, COMMUNITY_CHEST_CARDS, PROPERTY_NAMES
from property import Property

class Bank:
    def __init__(self):
        self.tax_accumulated = 0
        self.unowned_properties = [Property(name) for name in PROPERTY_NAMES]
        self.change_cards = CHANCE_CARDS.copy()
        self.community_chest_cards = COMMUNITY_CHEST_CARDS.copy()

        random.shuffle(self.change_cards)
        random.shuffle(self.community_chest_cards)

    def collected_taxes(self, amount):
        self.tax_accumulated += amount

    def get_accumulated_tax(self):
        return self.tax_accumulated
    
    def reset_accumulated_tax(self):
        self.tax_accumulated = 0

    def has_the_property(self, name):
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