from constants import CHANCE_POSITIONS, COMMUNITY_CHEST_POSITIONS, JAIL_POSITION, GO_POSITION, TAX_POSITIONS, PROPERTY_NAMES, SEED, EXTRA_GO_MONEY, GO_MONEY
from player import Player
from bank import Bank
import random

class Game:

    def __init__(self, seed=None):
        self.players = None
        self.bank = None
        self.current_player_index = 0
        self.dice1 = 0
        self.dice2 = 0
        self.double_count = 0
        self.print_flag = False
        self.seed = seed

        self.initComplete = False

    def load_players_npl(self, players, print_flag=False, analysis_flag=False):
        self.players = []
        for name, piece, logic in players:
            player = Player()
            player.basic_initialize(name, piece, logic, print_flag)
            self.players.append(player)
        self.bank = Bank(self.seed)
        self.current_player_index = 0
        self.dice1 = 0
        self.dice2 = 0
        self.double_count = 0
        self.print_flag = print_flag

        self.initComplete = True

    def load_from_json(self, game_data):
        if not self.validate_game_data(game_data):
            return
        
        self.bank = Bank(self.seed)  # Create the bank
        all_properties = self.bank.get_property_deck()
        # print(all_properties)
        
        self.players = []
        for player_data in game_data["players"]:
            # Remove the 'properties' key from player_data for loading
            properties_data = player_data.pop("properties", [])
            
            player = Player(print_flag=self.print_flag)  # Create a new player
            player.load_from_json(player_data)  # Pass the rest of player_data
            player_properties = []
            
            for property_item in properties_data:
                name_of_property = property_item["name"]
                mortgage_status = property_item["mortgaged"]
                houses = property_item.get("houses", 0)  
                
                # Find the matching property and update it
                for property in all_properties:
                    if property.name == name_of_property:
                        # Assign the property and modify its attributes
                        player_properties.append(property)
                        property.houses = houses
                        property.mortgaged = mortgage_status
                        all_properties.remove(property)  # Remove it from all_properties
                        break
            
            # Assign the properties to the player
            player.properties = player_properties
            self.players.append(player)


        # Give remaining properties to the bank
        for property in all_properties:
            self.bank.unowned_properties.append(property)


        # PRINT EVERY PLAYER EVERYTHING
        # for player in self.players:
        #     print(f"{player.name} has ${player.money}.")
        #     print(f"{player.name} has the following properties:")
        #     for property in player.properties:
        #         print(f"  - {property.name}")
        #     print()

        # print("Bank has the following properties:")
        # for property in self.bank.unowned_properties:
        #     print(f"  - {property.name}")
        # print()

        # self.bank.print_information()

        # for player in self.players:
        #     player.print_information()

        self.initComplete = True


    def validate_game_data(self,game_data):
        # Store the properties each player owns in a set to ensure uniqueness
        owned_properties = set()
        
        # Iterate through players to check all conditions
        for player in game_data["players"]:
            # Check that the position is less than 40
            if player["position"] >= 40:
                if self.print_flag:
                    print(f"Error: {player['name']} has an invalid position: {player['position']} (must be less than 40).")
                return False
            
            # Check the properties for duplicates and that stations/utilities have no houses
            for property in player["properties"]:
                # Check that stations and utilities do not have houses
                if "houses" in property and property["houses"] > 0:
                    if property["name"] in ["Kings Cross Station", "Marylebone Station", "Fenchurch Street Station", "Liverpool Street Station", "Electric Company", "Water Works"]:
                        if self.print_flag:
                            print(f"Error: {property['name']} cannot have houses.")
                        return False
                
                # Check that no two players have the same property
                property_name = property["name"]
                if property_name in owned_properties:
                    if self.print_flag:
                        print(f"Error: Property '{property_name}' is owned by more than one player.")
                    return False
                owned_properties.add(property_name)

        print("All validations passed!")
        return True


    def handle_exit(self, signum, frame):
        print("Exiting the game.")
        self.print_money_of_players()
        exit(0)

    def print_money_of_players(self):
        # print every player's money
        for player in self.players:
            print(f"{player.name} has ${player.money}.")

    def roll_dice(self):
        return random.randint(1, 6), random.randint(1, 6)
    
    def set_next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.double_count = 0

    def next_turn(self):
        player = self.players[self.current_player_index]
        if player.bankrupt:
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            return
        

        # BEFORE ROLLING DICE
        # Player can - if in jail - pay $50 to get out of jail or use card
        player.before_turn_decision() 

        self.dice1, self.dice2 = self.roll_dice()

        if player.in_jail:
            if player.jail_turns >= 3:
                if self.print_flag:
                    print(f"{player.name} is released from jail.")
                player.release_from_jail()
                # CONTINUE THE TURN
            else:
                if self.dice1 == self.dice2:
                    if self.print_flag:
                        print(f"{player.name} rolled doubles and is released from jail!")
                    player.release_from_jail()
                    # CONTINUE THE TURN
                else:
                    if self.print_flag:
                        print(f"{player.name} remains in jail.")
                    player.increment_jail_turns()
                    self.set_next_player()
                    return
                
        if self.dice1 == self.dice2:
            self.double_count += 1
                
        if self.double_count == 3:
            if self.print_flag:
                print(f"{player.name} rolled doubles 3 times in a row and goes to jail!")
            player.go_to_jail()
            self.set_next_player()
            return
        else:
            player.move(self.dice1 + self.dice2)
            self.handle_landing(player)
            if self.dice1 != self.dice2:
                self.set_next_player()
                return
        
    def handle_jail(self, player):
        if player.jail_turns >= 3:
            if self.print_flag:
                print(f"{player.name} is released from jail.")
            player.in_jail = False
            player.jail_turns = 0
        else:
            dice1, dice2 = self.roll_dice()
            if dice1 == dice2:
                if self.print_flag:
                    print(f"{player.name} rolled doubles and is released from jail!")
                player.in_jail = False
            else:
                if self.print_flag:
                    print(f"{player.name} remains in jail.")
                player.jail_turns += 1

    def handle_landing(self, player: Player):
        position = player.get_position()
        # Check if the player passed go
        if position < self.dice1 + self.dice2:
            player.add_money(GO_MONEY)
            if self.print_flag:
                print(f"{player.name} passed GO and collected $200!")

        if position in CHANCE_POSITIONS:
            if self.print_flag:
                print(f"{player.name} landed on a Chance space.")
            card = self.bank.get_a_chance_card(player)
            if self.print_flag:
                print(f"{player.name} picked a Chance card: {card['text']}")
            card["action"](self, player)
            if player.is_bankrupt():
                if self.print_flag:
                    print(f"{player.name} is bankrupt to the bank!")
                if player.money > 0:
                    self.bank.collected_taxes(player.money)
                player.money = 0
                # Give properties to the bank
                properties = player.remove_all_properties()
                for property in properties:
                    self.bank.unowned_properties.append(property)
            else:
                self.handle_landing(player) # Check if the player landed on another special space
        elif position in COMMUNITY_CHEST_POSITIONS:
            if self.print_flag:
                print(f"{player.name} landed on a Community Chest space.")
            card = self.bank.get_a_community_chest_card(player)
            if self.print_flag:
                print(f"{player.name} picked a Community Chest card: {card['text']}")
            card["action"](self, player)
            if player.is_bankrupt():
                if self.print_flag:
                    print(f"{player.name} is bankrupt to the bank!")
                if player.money > 0:
                    self.bank.collected_taxes(player.money)
                player.money = 0
                # Give properties to the bank
                properties = player.remove_all_properties()
                for property in properties:
                    self.bank.unowned_properties.append(property)
            else:
                self.handle_landing(player) # Check if the player landed on another special space
        elif position == JAIL_POSITION:
            if self.print_flag:
                print(f"{player.name} is just visiting jail.")
        elif position == GO_POSITION:
            if self.print_flag:
                print(f"{player.name} landed on GO.")
            player.add_money(EXTRA_GO_MONEY)
        elif position in TAX_POSITIONS:
            if self.print_flag:
                print(f"{player.name} landed on a Tax space.")
            if position == 4:
                self.rent_buy_transaction(self.bank, player, 200)
            elif position == 38:
                self.rent_buy_transaction(self.bank, player, 100)
        elif position == 30:
            if self.print_flag:
                print(f"{player.name} landed on Go to Jail space.")
            player.go_to_jail()
        else:
            self.landed_on_property(player, position)

        if not player.is_bankrupt():
            # AFTER Turn actions
            player.after_turn_decision() 

    def player_advances_to_nearest_utility(self, player: Player):
        '''
        Advance to nearest Utility. If unowned, you may buy it from the bank. If owned, 
        throw dice and pay owner a total ten times amount thrown.
        '''
        before_position = player.get_position()
        player.get_to_nearest_utility()
        after_position = player.get_position()
        if before_position > after_position:
            player.add_money(GO_MONEY)

        # Check if the property is owned by another player
        property_name = PROPERTY_NAMES[after_position % len(PROPERTY_NAMES)]
        property_owner = self.get_owner_of_property(property_name)
        if property_owner is None:
            if player.wants_to_buy_property(property_name, self.bank.get_property_price(property_name)):
                player.deduct_money(self.bank.get_property_price(property_name))
                player.properties.append(self.bank.take_property(property_name))
                if self.print_flag:
                    print(f"{player.name} bought {property_name} for ${self.bank.get_property_price(property_name)}.")
        else:
            if self.print_flag:
                print(f"{player.name} already owns {property_name}.")
            # Pay ten times the thrown amount
            self.rent_buy_transaction(property_owner, player, self.dice1 + self.dice2 * 10)
    
    def rent_buy_transaction(self, owner, player, rent):
        player.deduct_money(rent)
        if player.is_bankrupt():
            if owner.type == "BANK":
                if self.print_flag:
                    print(f"{player.name} is bankrupt to the bank!")
                if player.money > 0:
                    self.bank.collected_taxes(player.money)
                player.money = 0
                # Give properties to the bank
                properties = player.remove_all_properties()
                for property in properties:
                    self.bank.unowned_properties.append(property)
            else:
                if self.print_flag:
                    print(f"{player.name} is bankrupt to {owner.name}!")
                player.money = 0
                # Give properties to the bank
                properties = player.remove_all_properties()
                for property in properties:
                    owner.properties.append(property)
        else:
            if owner.type == "BANK":
                self.bank.collected_taxes(rent)
                if self.print_flag:
                    print(f"{player.name} paid ${rent} to the bank.")
            else:
                owner.add_money(rent)
                if self.print_flag:
                    print(f"{player.name} paid ${rent} to {owner.name}.")

    def player_advances_to_nearest_railroad(self, player):
        '''
        Advance to nearest Railroad. If unowned, you may buy it from the bank. If owned, 
        pay owner rent equal to ten times amount thrown.
        '''
        before_position = player.get_position()
        player.get_to_nearest_railroad()
        after_position = player.get_position()
        if before_position > after_position:
            player.add_money(GO_MONEY)

        # Check if the property is owned by another player
        property_name = PROPERTY_NAMES[after_position % len(PROPERTY_NAMES)]
        property_owner = self.get_owner_of_property(property_name)
        if property_owner is None:
            if player.wants_to_buy_property(property_name, self.bank.get_property_price(property_name)):
                player.deduct_money(self.bank.get_property_price(property_name))
                player.properties.append(self.bank.take_property(property_name))
                print(f"{player.name} bought {property_name} for ${self.bank.get_property_price(property_name)}.")
        else:
            if self.print_flag:
                print(f"{player.name} already owns {property_name}.")
            # Pay ten times the thrown amount
            self.rent_buy_transaction(property_owner, player, self.dice1 + self.dice2 * 10)

    def collect_from_all_players(self, player, amount):
        for other_player in self.players:
            if other_player != player:
                self.rent_buy_transaction(player, other_player, amount)

    def landed_on_property(self, player, position):
        # Check if the property is owned by another player
        # check if bank has the property
        property_name = PROPERTY_NAMES[position % len(PROPERTY_NAMES)]
        if self.print_flag:
            print(f"{player.name} landed on {property_name}.")

        if self.bank.has_the_property(property_name):
            property_price = self.bank.get_property_price(property_name)
            if player.wants_to_buy_property(property_name, property_price):
                if player.get_money() < property_price:
                    if self.print_flag:
                        print(f"{player.name} does not have enough money to buy {property_name}.")
                else:
                    player.deduct_money(property_price)
                    player.properties.append(self.bank.take_property(property_name))
                    if self.print_flag:
                        print(f"{player.name} bought {property_name} for ${property_price}.")
        elif player.has_the_property(property_name):
            if self.print_flag:
                print(f"{player.name} already owns {property_name}.")
        else:
            owner_of_property = self.get_owner_of_property(property_name)
            rent = owner_of_property.calculate_rent(property_name, self.dice1 + self.dice2)
            # print rent
            if self.print_flag:
                print(f"Rent for {property_name} is ${rent}.")
            player.deduct_money(rent)
            if player.is_bankrupt():
                if player.money > 0:
                    owner_of_property.add_money(player.money)
                player.money = 0
                # Give properties to the owner
                properties = player.remove_all_properties()
                for property in properties:
                    owner_of_property.properties.append(property)
                if self.print_flag:
                    print(f"{player.name} went bankrupt to {owner_of_property.name}.")
                
            else:
                owner_of_property.add_money(rent)
                if self.print_flag:
                    print(f"{player.name} paid ${rent} to {owner_of_property.name}.")
            
    def get_owner_of_property(self, property_name):
        for player in self.players:
            # Iterate through the player's properties and check if the property name matches
            for property in player.properties:
                if property.name == property_name:
                    return player
        return self.bank
                    
    def play_game(self):
        if not self.initComplete:
            print("Game not initialized")
            return
        while(True):
            active_players = [player for player in self.players if not player.bankrupt]
            # print the number of active players
            if self.print_flag:
                print(f"Number of active players: {len(active_players)}")
                self.print_money_of_players()
            if len(active_players) == 1:
                # if self.print_flag:
                print(f"{active_players[0].name} wins the game!")
                self.print_money_of_players()
                break
            self.next_turn()
            if self.print_flag:
                print("-" * 40)

