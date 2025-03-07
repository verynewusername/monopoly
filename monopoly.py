from constants import CHANCE_POSITIONS, COMMUNITY_CHEST_POSITIONS, JAIL_POSITION, GO_POSITION, TAX_POSITIONS, PROPERTY_NAMES, SEED
from player import Player
from bank import Bank
import random

# Set Seed
# random.seed(SEED)

class Game:
    def __init__(self, players):
        self.players = [Player(name, pieceName) for name, pieceName in players]
        self.bank = Bank()
        self.current_player_index = 0
        self.dice1 = 0
        self.dice2 = 0
        self.double_count = 0

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

    def next_turn(self):
        player = self.players[self.current_player_index]
        self.dice1, self.dice2 = self.roll_dice()
        if player.in_jail:
            self.handle_jail(player)
            if not player.in_jail:
                self.default_handle_turn(player)
            else:
                self.current_player_index = (self.current_player_index + 1) % len(self.players)
        else:
            self.default_handle_turn(player)
        
    def default_handle_turn(self, player):
        if self.dice1 == self.dice2:
                self.double_count += 1
        if self.double_count == 3:
            print(f"{player.name} rolled doubles 3 times in a row and goes to jail!")
            player.go_to_jail()
        else:
            print(f"{player.name} rolled {self.dice1} and {self.dice2}.")
            player.move(self.dice1 + self.dice2)
            self.handle_landing(player)
            if self.dice1 != self.dice2:
                self.current_player_index = (self.current_player_index + 1) % len(self.players)
                self.double_count = 0

    def handle_jail(self, player):
        if player.jail_turns >= 3:
            print(f"{player.name} is released from jail.")
            player.in_jail = False
            player.jail_turns = 0
        else:
            dice1, dice2 = self.roll_dice()
            if dice1 == dice2:
                print(f"{player.name} rolled doubles and is released from jail!")
                player.in_jail = False
            else:
                print(f"{player.name} remains in jail.")
                player.jail_turns += 1

    def handle_landing(self, player: Player):
        position = player.get_position()
        # Check if the player passed go
        if position < self.dice1 + self.dice2:
            player.money += 50 # ! CHECK HERE - temporarily 10
            print(f"{player.name} passed GO and collected $200!")

        if position in CHANCE_POSITIONS:
            print(f"{player.name} landed on a Chance space.")
            # TODO: Implement Chance card logic
        elif position in COMMUNITY_CHEST_POSITIONS:
            print(f"{player.name} landed on a Community Chest space.")
            # TODO Implement Community Chest logic here
        elif position == JAIL_POSITION:
            print(f"{player.name} is just visiting jail.")
        elif position == GO_POSITION:
            print(f"{player.name} landed on GO.")
            player.money += 200
        elif position in TAX_POSITIONS:
            print(f"{player.name} landed on a Tax space.")
            if position == 4:
                player.deduct_money(200)
                self.bank.collected_taxes(200)
            elif position == 38:
                player.deduct_money(100)
                self.bank.collected_taxes(100)
        elif position == 30:
            print(f"{player.name} landed on Go to Jail space.")
            player.go_to_jail()
        else:
            # Check if the property is owned by another player
            # check if bank has the property
            property_name = PROPERTY_NAMES[position % len(PROPERTY_NAMES)]
            print(f"{player.name} landed on {property_name}.")

            if self.bank.has_the_property(property_name):
                property_price = self.bank.get_property_price(property_name)
                if player.wants_to_buy_property(property_name, property_price):
                    player.deduct_money(property_price)
                    player.properties.append(self.bank.take_property(property_name))
                    print(f"{player.name} bought {property_name} for ${property_price}.")
            else:
                owner_of_property = self.get_owner_of_property(property_name)
                rent = owner_of_property.calculate_rent(property_name, self.dice1 + self.dice2)
                player.deduct_money(rent)
                if player.is_bankrupt():
                    owner_of_property.get_money(player.money)
                    player.money = 0
                    # Give properties to the owner
                    properties = player.remove_all_properties()
                    for property in properties:
                        owner_of_property.properties.append(property)
                    print(f"{player.name} went bankrupt to {owner_of_property.name}.")
                    
                else:
                    owner_of_property.get_money(rent)
                    print(f"{player.name} paid ${rent} to {owner_of_property.name}.")
                

    def get_owner_of_property(self, property_name):
        for player in self.players:
            if property_name in [property.name for property in player.properties]:
                return player
        raise ValueError(f"No player owns {property_name}.")
                    
    def play_game(self):
        while(True):
            self.next_turn()
            active_players = [player for player in self.players if not player.bankrupt]
            # print the number of active players
            print(f"Number of active players: {len(active_players)}")
            if len(active_players) == 1:
                print(f"{active_players[0].name} wins the game!")
                self.print_money_of_players()
                break
            print("-" * 40)

def main():
    try:
        game = Game([["Efe", "Hat"], ["Oza", "Dog"], ["Sude", "Duck"], ["Can", "Car"]])
        game.play_game()
    except KeyboardInterrupt:
        game.handle_exit(None, None)
    except Exception as e:
        print(e)
        game.handle_exit(None, None)

if __name__ == "__main__":
    main()