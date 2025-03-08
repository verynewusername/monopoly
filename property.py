from player import Player
from constants import PROPERTY_DATA

class Property:
    def __init__(self, name):
        self.name = name
        self.price = PROPERTY_DATA[name]["price"]
        self.rents = PROPERTY_DATA[name]["rent"]
        self.mortgage_value = PROPERTY_DATA[name]["mortgage"]
        self.is_mortgaged = False
        self.houses = 0

    def calculate_rent(self, dice_roll, has_both_utilities, number_of_stations_owned):
        if self.is_mortgaged:
            return 0
        elif self.name in ["Electric Company", "Water Works"]:
            return 4 * dice_roll if has_both_utilities else 10 * dice_roll
        elif self.name in ["Kings Cross Station", "Marylebone Station", "Fenchurch St Station", "Liverpool Street Station"]:
            return 25 * number_of_stations_owned
        elif self.houses == 0:
            return self.rents[0]
        elif 1 <= self.houses <= 5:
            return self.rents[self.houses]
        else:
            raise ValueError("Invalid number of houses on property.")
        
    def mortgage(self, player: Player):
        if self.is_mortgaged:
            raise ValueError(f"{self.name} is already mortgaged.")
        else:
            self.is_mortgaged = True
            player.add_money(self.mortgage_value)
            print(f"{player.name} mortgaged {self.name} for ${self.mortgage_value}.")

    def unmortgage(self, player: Player):
        if not self.is_mortgaged:
            raise ValueError(f"{self.name} is not mortgaged.")
        else:
            self.is_mortgaged = False
            player.deduct_money(self.mortgage_value)
            print(f"{player.name} unmortgaged {self.name} for ${self.mortgage_value}.")

    def get_house_building_price(self):
        # Get idx of the property in the list of properties
        idx = PROPERTY_DATA.keys().index(self.name)
        # Get the price of the property
        '''
        first 10 - house adding price 50
        second 10 - house adding price 100
        third 10 - house adding price 150
        fourth 10 - house adding price 200
        '''
        if idx < 10:
            return 50
        elif idx < 20:
            return 100
        elif idx < 30:
            return 150
        else:
            return 200

    def build_a_house(self):
        self.houses += 1

    def remove_a_house(self):
        self.houses -= 1