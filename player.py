from constants import START_MONEY, PROPERTY_NAMES, NUM_SQUARES, GO_MONEY, EXTRA_GO_MONEY
from piece import Piece
import copy

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
        self.get_out_of_jail_free = 0
        self.type = "BOT"
    
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
    
    def add_money(self, amount):
        if self.bankrupt:
            raise ValueError(f"{self.name} is bankrupt and cannot receive money., amount: {amount}")
        self.money += amount

    def move(self, steps):
        self.piece.position = (self.piece.position + steps) % NUM_SQUARES

    def get_number_of_stations_owned(self):
        # 5, 15, 25, 35
        for property in self.properties:
            if property.name in ["Kings Cross Station", "Marylebone Station", "Fenchurch St Station", "Liverpool Street Station"]:
                return self.properties.count(property)
        return 0

    def calculate_rent(self, property_name, dice_roll):
        for property in self.properties:
            if property.name == property_name:
                return property.calculate_rent(dice_roll, self.has_both_utilities(), self.get_number_of_stations_owned())
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

    def has_the_property(self, property_name) -> bool:
        return property_name in [property.name for property in self.properties]

    def has_properties(self) -> bool:
        if self.bankrupt:
            return False
        return len(self.properties) > 0

    def remove_all_properties(self):
        properties = copy.deepcopy(self.properties)  # Creates a deep copy
        self.properties.clear()
        return properties
    
    def increment_jail_turns(self):
        self.jail_turns += 1
    
    def release_from_jail(self):
        self.jail_turns = 0
        self.in_jail = False

    def chance_move_to(self, position, extra_money=0):
        self.move(position - self.get_position())
        self.add_money(extra_money)

    def get_get_out_of_jail_card(self):
        self.get_out_of_jail_free += 1

    def use_get_out_of_jail_card(self):
        if self.get_out_of_jail_free > 0:
            self.get_out_of_jail_free -= 1
            self.release_from_jail()
            return True
        return False
    
    def move_back(self, steps):
        self.move(-steps)

    def chance_pay_repairs(self):
        for property in self.properties:
            if property.houses == 5:
                self.deduct_money(100)
            elif property.houses > 0 and property.houses < 5:
                self.deduct_money(25 * property.houses)
        return True
    
    def community_chest_pay_repairs(self):
        for property in self.properties:
            if property.houses == 5:
                self.deduct_money(115)
            elif property.houses > 0 and property.houses < 5:
                self.deduct_money(40 * property.houses)
        return True
    
    def get_to_nearest_utility(self):
        # Utilities are at positions 12 and 28
        if self.get_position() < 12 or self.get_position() > 28:
            self.move(12 - self.get_position())
        else:
            self.move(28 - self.get_position())
        return True
    
    def get_to_nearest_railroad(self):
        # Railroads are at positions 5, 15, 25, 35
        # go to the closest
        if self.get_position() < 5 or self.get_position() > 35:
            self.move(5 - self.get_position())
        elif self.get_position() < 15:
            self.move(15 - self.get_position())
        elif self.get_position() < 25:
            self.move(25 - self.get_position())
        else:
            self.move(35 - self.get_position())
        return True

    def get_money(self):
        return self.money
    
    def get_house_price_for_property(self, property_name):
        for property in self.properties:
            if property.name == property_name:
                return property.get_house_building_price()
        raise ValueError(f"{self.name} does not own {property_name}.")
    
    def build_a_house(self, property_name) -> bool:
        price = self.get_house_price_for_property(property_name)
        assert price is not None or price != 0
        if self.money >= price:
            for property in self.properties:
                if property.name == property_name:
                    property.build_a_house(self)
                    return True
        return False
    
    def sell_a_house(self, property_name) -> bool:
        money_back = self.get_house_price_for_property(property_name) // 2
        for property in self.properties:
            if property.name == property_name:
                property.remove_a_house(self)
                self.add_money(money_back)
                return True
        return False
    
    def get_mortgage_value(self, property_name) -> int:
        for property in self.properties:
            if property.name == property_name:
                return property.mortgage_value
        raise ValueError(f"{self.name} does not own {property_name}.")
    
    def mortgage_property(self, property_name) -> bool:
        mortgage_value = self.get_mortgage_value(property_name)
        for property in self.properties:
            if property.name == property_name:
                if property.mortgage(self):
                    self.add_money(mortgage_value)
                    return True
        return False

    def unmortgage_property(self, property_name) -> bool:
        mortgage_value = self.get_mortgage_value(property_name)
        for property in self.properties:
            if property.name == property_name:
                if property.unmortgage(self):
                    self.deduct_money(mortgage_value * 1.1) # 10% interest
                    return True
        return False
