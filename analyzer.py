from monopoly import Game
import matplotlib.pyplot as plt
import numpy as np
import random 

class MonopolyAnalyzer:
    def __init__(self, game_data, seed = None, number_of_repeats= 1000):
        self.game_data = game_data
        self.number_of_repeats = number_of_repeats

        if seed is not None:
            random.seed(seed)

    def analyze(self):

        self.overall_results = []  # Store results of all games

        for idx in range(self.number_of_repeats):
            self.game = Game(random.randint(0, 1000000))  # Create a new game
            if not self.game.load_from_json(self.game_data):
                raise ValueError("Invalid JSON data")

            results = {player.name: [] for player in self.game.players}  # Dictionary to store results

            max_turns = 20000  
            turn_count = 0

            while self.game.who_won() is None and turn_count < max_turns:
                for player in self.game.players:
                    results[player.name].append(player.money)

                self.game.next_turn()
                turn_count += 1  # Increment turn count

            self.overall_results.append(results)  # Store results after game ends

            self.game.reset()

        self.process_results()


    def process_results(self):
        # Make a graph for money vs time with standard deviation included
        
        plt.figure(figsize=(10, 6))
        for player_name, player_results in self.overall_results[0].items():
            player_results = np.array(player_results)
            mean = np.mean(player_results)
            std = np.std(player_results)
            plt.plot(range(len(player_results)), player_results, label=f"{player_name} (mean: {mean:.2f}, std: {std:.2f})")
        plt.xlabel("Turns")
        plt.ylabel("Money")
        plt.title("Money vs Time")
        plt.legend()
        plt.show()

        # save as out.png
        plt.savefig("out.png")
