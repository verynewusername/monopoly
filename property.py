from player import Player
from constants import PROPERTY_DATA, COLOR_GROUPS

class Property:
    def __init__(self, name, print_flag=False):
        self.name = name
        self.price = PROPERTY_DATA[name]["price"]
        self.rents = PROPERTY_DATA[name]["rent"]
        self.mortgage_value = PROPERTY_DATA[name]["mortgage"]
        self.is_mortgaged = False
        self.houses = 0
        self.color = self.get_color_group()
        self.print_flag = print_flag

    def get_color_group(self):
        for color, properties in COLOR_GROUPS.items():
            if self.name in properties:
                return color
        return None  # If the property is not found in any color group
    
    def calculate_rent(self, dice_roll, has_both_utilities, number_of_stations_owned, has_all_same_color_properties):
        if self.is_mortgaged:
            return 0
        elif self.name in ["Kings Cross Station", "Marylebone Station", "Fenchurch St Station", "Liverpool Street Station"]:
            return 25 * number_of_stations_owned
        elif self.name in ["Electric Company", "Water Works"]:
            return 4 * dice_roll if has_both_utilities else 10 * dice_roll
        elif has_all_same_color_properties:
            if self.houses == 0:
                return self.rents[0] * 2
            elif 1 <= self.houses <= 5:
                return self.rents[self.houses]
        else:
            return self.rents[0]
        
    def mortgage(self, player: Player):
        if self.is_mortgaged:
            raise ValueError(f"{self.name} is already mortgaged.")
        else:
            self.is_mortgaged = True
            player.add_money(self.mortgage_value)
            if self.print_flag:
                print(f"{player.name} mortgaged {self.name} for ${self.mortgage_value}.")

    def unmortgage(self, player: Player):
        if not self.is_mortgaged:
            raise ValueError(f"{self.name} is not mortgaged.")
        else:
            self.is_mortgaged = False
            player.deduct_money(self.mortgage_value)
            if self.print_flag:
                print(f"{player.name} unmortgaged {self.name} for ${self.mortgage_value}.")

    def get_house_building_price(self):
        # Get idx of the property in the list of properties
        keys = list(PROPERTY_DATA.keys())  
        idx = keys.index(self.name)        
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

    def print_information(self):
        print(f"Property: {self.name}")
        print(f"\tPrice: {self.price}")
        print(f"\tRents: {self.rents}")
        print(f"\tMortgage value: {self.mortgage_value}")
        print(f"\tMortgaged: {self.is_mortgaged}")
        print(f"\tHouses: {self.houses}")
        print(f"\tColor: {self.color}")