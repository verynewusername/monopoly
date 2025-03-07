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

    def calculate_rent(self, dice_roll, has_both_utilities):
        if self.is_mortgaged:
            return 0
        elif self.name in ["Electric Company", "Water Works"]:
            return 4 * dice_roll if has_both_utilities else 10 * dice_roll
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
            player.get_money(self.mortgage_value)
            print(f"{player.name} mortgaged {self.name} for ${self.mortgage_value}.")

    def unmortgage(self, player: Player):
        if not self.is_mortgaged:
            raise ValueError(f"{self.name} is not mortgaged.")
        else:
            self.is_mortgaged = False
            player.deduct_money(self.mortgage_value)
            print(f"{player.name} unmortgaged {self.name} for ${self.mortgage_value}.")

    def build_house(self, player: Player):
        # TODO: Implement this method
        # get the price for a house
        # if self.houses < 5:
        #     player.deduct_money(self.price)
        #     self.houses += 1
        #     print(f"{player.name} built a house on {self.name} for ${self.price}.")
        # else:
        #     raise ValueError(f"{player.name} cannot build a house on {self.name}.")
        pass

    def sell_house(self):
        # TODO
        pass

    # def buy_property(self, player):
    #     if self.owner is None and player.money >= self.price:
    #         self.owner = player
    #         player.money -= self.price
    #         player.properties.append(self)
    #         print(f"{player.name} bought {self.name}.")
    #     else:
    #         raise ValueError(f"{player.name} cannot buy {self.name}.")
