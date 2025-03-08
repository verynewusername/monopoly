
# Constants
START_MONEY = 1950
NUM_SQUARES = 40
JAIL_POSITION = 10
GO_POSITION = 0
CHANCE_POSITIONS = [7, 22, 36]
COMMUNITY_CHEST_POSITIONS = [2, 17, 33]
TAX_POSITIONS = [4, 38] # Income Tax 200, Super Tax 100

# EXTRA_GO_MONEY = 200
# GO_MONEY = 200

# ! DEBUGING PURPOSES 20 
EXTRA_GO_MONEY = 20
GO_MONEY = 20
# ! DEBUGING PURPOSES 20 END

PROPERTY_NAMES = [
    "Old Kent Road", "Whitechapel Road", "Kings Cross Station", "The Angel Islington", "Euston Road",
    "Pentonville Road", "Pall Mall", "Electric Company", "Whitehall", "Northumberland Avenue",
    "Marylebone Station", "Bow Street", "Marlborough Street", "Vine Street", "The Strand",
    "Fleet Street", "Trafalgar Square", "Fenchurch St Station", "Leicester Square", "Coventry Street",
    "Water Works", "Piccadilly", "Regent Street", "Oxford Street", "Bond Street",
    "Liverpool Street Station", "Park Lane", "Mayfair"
]

'''
The following cards Depend on owning themselves
Kings Cross Station
Marylebone Station
Fenchurch St Station
Liverpool Street Station
'''

# Property Prices, Rents, and Mortgage Values
PROPERTY_DATA = {
    "Old Kent Road": {"price": 60, "rent": [2, 10, 30, 90, 160, 250], "mortgage": 30},
    "Whitechapel Road": {"price": 60, "rent": [4, 20, 60, 180, 320, 450], "mortgage": 30},
    "Kings Cross Station": {"price": 200, "rent": [], "mortgage": 100},
    "The Angel Islington": {"price": 100, "rent": [6, 30, 90, 270, 400, 550], "mortgage": 50},
    "Euston Road": {"price": 100, "rent": [6, 30, 90, 270, 400, 550], "mortgage": 50},
    "Pentonville Road": {"price": 120, "rent": [8, 40, 100, 300, 450, 600], "mortgage": 60},
    "Pall Mall": {"price": 140, "rent": [10, 50, 150, 450, 625, 750], "mortgage": 70},
    "Electric Company": {"price": 150, "rent": [], "mortgage": 75},  # Rent depends on dice roll
    "Whitehall": {"price": 140, "rent": [10, 50, 150, 450, 625, 750], "mortgage": 70},
    "Northumberland Avenue": {"price": 160, "rent": [12, 60, 180, 500, 700, 900], "mortgage": 80},
    "Marylebone Station": {"price": 200, "rent": [], "mortgage": 100},
    "Bow Street": {"price": 180, "rent": [14, 70, 200, 550, 750, 950], "mortgage": 90},
    "Marlborough Street": {"price": 180, "rent": [14, 70, 200, 550, 750, 950], "mortgage": 90},
    "Vine Street": {"price": 200, "rent": [16, 80, 220, 600, 800, 1000], "mortgage": 100},
    "The Strand": {"price": 220, "rent": [18, 90, 250, 700, 875, 1050], "mortgage": 110},
    "Fleet Street": {"price": 220, "rent": [18, 90, 250, 700, 875, 1050], "mortgage": 110},
    "Trafalgar Square": {"price": 240, "rent": [20, 100, 300, 750, 925, 1100], "mortgage": 120},
    "Fenchurch St Station": {"price": 200, "rent": [], "mortgage": 100},
    "Leicester Square": {"price": 260, "rent": [22, 110, 330, 800, 975, 1150], "mortgage": 130},
    "Coventry Street": {"price": 260, "rent": [22, 110, 330, 800, 975, 1150], "mortgage": 130},
    "Water Works": {"price": 150, "rent": [], "mortgage": 75},  # Rent depends on dice roll
    "Piccadilly": {"price": 280, "rent": [22, 120, 360, 850, 1025, 1200], "mortgage": 140},
    "Regent Street": {"price": 300, "rent": [26, 130, 390, 900, 1100, 1275], "mortgage": 150},
    "Oxford Street": {"price": 300, "rent": [26, 130, 390, 900, 1100, 1275], "mortgage": 150},
    "Bond Street": {"price": 320, "rent": [28, 150, 450, 1000, 1200, 1400], "mortgage": 160},
    "Liverpool Street Station": {"price": 200, "rent": [], "mortgage": 100},
    "Park Lane": {"price": 350, "rent": [35, 175, 500, 1100, 1300, 1500], "mortgage": 175},
    "Mayfair": {"price": 400, "rent": [50, 200, 600, 1400, 1700, 2000], "mortgage": 200}
}


# Chance and Community Chest Cards
CHANCE_CARDS = [
    {"text": "Advance to Go (Collect $200)", "action": lambda self, player: player.chance_move_to(GO_POSITION, 200)},
    {"text": "Go to Jail. Go directly to Jail, do not pass Go, do not collect $200.", "action": lambda self, player: player.go_to_jail()},
    {"text": "Advance to Illinois Avenue", "action": lambda self, player: player.chance_move_to(24)},
    {"text": "Advance to St. Charles Place", "action": lambda self, player: player.chance_move_to(11)},
    {"text": "Advance to Boardwalk", "action": lambda self, player: player.chance_move_to(39)},
    {"text": "Bank pays you dividend of $50", "action": lambda self, player: player.add_money(50)},
    {"text": "Get Out of Jail Free", "action": lambda self, player: player.get_get_out_of_jail_card()},
    {"text": "Go back 3 spaces", "action": lambda self, player: player.move_back(3)},
    {"text": "Make general repairs on all your property. For each house pay $25. For each hotel pay $100.", "action": lambda self, player: player.chance_pay_repairs()},
    {"text": "Pay poor tax of $15", "action": lambda self, player: player.deduct_money(15)},
    {"text": "Take a trip to Reading Railroad. If you pass Go, collect $200.", "action": lambda self, player: player.chance_move_to(5)},
    {"text": "You have been elected chairman of the board. Pay each player $50.", "action": lambda self, player: player.deduct_money(50 * (len(self.players) - 1))},
    {"text": "Your building loan matures. Collect $150.", "action": lambda self, player: player.add_money(150)},
    {"text": "You have won a crossword competition. Collect $100.", "action": lambda self, player: player.add_money(100)},
    {"text": "Advance to nearest Utility. If unowned, you may buy it from the bank. If owned, throw dice and pay owner a total ten times amount thrown.", "action": lambda self, player: self.player_advances_to_nearest_utility(player)},
    {"text": "Advance to nearest Railroad. If unowned, you may buy it from the bank. If owned, pay owner rent equal to ten times amount thrown.", "action": lambda self, player: self.player_advances_to_nearest_railroad(player)},
    {"text": "Take a walk on the Boardwalk. Advance to Boardwalk.", "action": lambda self, player: player.chance_move_to(39)}
]

COMMUNITY_CHEST_CARDS = [
    {"text": "Advance to Go (Collect $200)", "action": lambda self, player: player.chance_move_to(GO_POSITION, 200)},
    {"text": "Go to Jail. Go directly to Jail, do not pass Go, do not collect $200.", "action": lambda self, player: player.go_to_jail()},
    {"text": "Bank error in your favor. Collect $200.", "action": lambda self, player: player.add_money(200)},
    {"text": "Doctor's fees. Pay $50.", "action": lambda self, player: player.deduct_money(50)},
    {"text": "From sale of stock you get $50.", "action": lambda self, player: player.add_money(50)},
    {"text": "Get Out of Jail Free", "action": lambda self, player: player.get_get_out_of_jail_card()},
    {"text": "Go to Jail. Go directly to Jail, do not pass Go, do not collect $200.", "action": lambda self, player: player.go_to_jail()},
    {"text": "Grand Opera Night. Collect $50 from every player for opening night seats.", "action": lambda self, player: player.collect_from_all_players(player, 50)},
    {"text": "Holiday Fund matures. Receive $100.", "action": lambda self, player: player.add_money(100)},
    {"text": "Income tax refund. Collect $20.", "action": lambda self, player: player.add_money(20)},
    {"text": "It is your birthday. Collect $10 from every player.", "action": lambda self, player: player.collect_from_all_players( player, 10)},
    {"text": "Life insurance matures. Collect $100.", "action": lambda self, player: player.add_money(100)},
    {"text": "Pay hospital fees of $100.", "action": lambda self, player: player.deduct_money(100)},
    {"text": "Pay school fees of $150.", "action": lambda self, player: player.deduct_money(150)},
    {"text": "Receive $25 consultancy fee.", "action": lambda self, player: player.add_money(25)},
    {"text": "You are assessed for street repairs: pay $40 per house and $115 per hotel you own.", "action": lambda self, player: player.community_chest_pay_repairs()},
    {"text": "You have won second prize in a beauty contest. Collect $10.", "action": lambda self, player: player.add_money(10)},
    {"text": "You inherit $100.", "action": lambda self, player: player.add_money(100)}
]

MONOPOLY_PIECES = [
    "Battleship",
    "Car",
    "Hat",
    "Scottie Dog",
    "Cat",
    "Dog",
    "Duck",
    "Thimble",
    "Penguin"
]

SEED = 42