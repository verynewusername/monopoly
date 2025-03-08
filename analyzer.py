# FILE: analyzer.py
# Date: 2025-03-08
# Author: Efe Gorkem Sirin
# Description: This file contains the MonopolyAnalyzer class which analyzes the game results.

from monopoly import Game
import matplotlib.pyplot as plt
import numpy as np
import random

class MonopolyAnalyzer:
    def __init__(self, game_data, seed=None, number_of_repeats=1000):
        self.game_data = game_data
        self.number_of_repeats = number_of_repeats
        
        if seed is not None:
            random.seed(seed)
    
    def analyze(self):
        player_names = [player["name"] for player in self.game_data["players"]]
        self.win_counts = {player_name: 0 for player_name in player_names}
        
        self.overall_results = []  # Store results of all games
        
        for idx in range(self.number_of_repeats):
            self.game = Game(random.randint(0, 1000000))  # Create a new game
            if not self.game.load_from_json(self.game_data):
                raise ValueError("Invalid JSON data")
            
            results = {player.name: [] for player in self.game.players}  # Dictionary to store results
            
            max_turns = 1000 
            turn_count = 0
            
            while self.game.who_won() is None and turn_count < max_turns:
                for player in self.game.players:
                    results[player.name].append(player.money)
                
                self.game.next_turn()
                turn_count += 1  # Increment turn count
            
            winner = self.game.who_won()
            if winner is not None:
                self.win_counts[winner.name] += 1  # Use player name as key
            
            if winner is not None:
                self.overall_results.append(results)  # Store results after game ends
            
            self.game.reset()
        
        print("Win counts: " + str(self.win_counts))
        
        self.process_results()
        self.plot_win_percentages()
    
    def process_results(self):
        if not self.overall_results:  # Check if list is empty
            print("No results to process.")
            return
        
        # Find the maximum length of any player's money history
        max_turns = 0
        for game_result in self.overall_results:
            for player_name, money_history in game_result.items():
                max_turns = max(max_turns, len(money_history))
        
        # Create aggregated results dictionary
        # Structure: {player_name: [[game1_money_at_turn_0, game2_money_at_turn_0, ...], [game1_money_at_turn_1, ...], ...]}
        aggregated_results = {}
        for player_name in self.overall_results[0].keys():
            aggregated_results[player_name] = [[] for _ in range(max_turns)]
        
        # Fill in the aggregated results
        for game_result in self.overall_results:
            for player_name, money_history in game_result.items():
                for turn, money in enumerate(money_history):
                    aggregated_results[player_name][turn].append(money)
        
        # Calculate means and standard deviations for each turn
        mean_results = {}
        std_results = {}
        for player_name, turn_data in aggregated_results.items():
            mean_results[player_name] = [np.mean(turn) if turn else 0 for turn in turn_data]
            std_results[player_name] = [np.std(turn) if turn and len(turn) > 1 else 0 for turn in turn_data]
        
        # Plotting
        plt.figure(figsize=(10, 6))
        
        for player_name in aggregated_results.keys():
            turns = np.arange(len(mean_results[player_name]))
            means = mean_results[player_name]
            stds = std_results[player_name]
            
            # Plot mean line
            plt.plot(turns, means, label=f"{player_name} (mean at end: {means[-1]:.2f})")
            
            # Plot standard deviation shadow
            plt.fill_between(turns, 
                            [max(0, mean - std) for mean, std in zip(means, stds)], 
                            [mean + std for mean, std in zip(means, stds)], 
                            alpha=0.2)
        
        plt.xlabel("Turns")
        plt.ylabel("Money")
        plt.title("Average Money vs Time (with Standard Deviation)")
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)
        
        plt.savefig("money_vs_time.png")
        plt.show()
    
    def plot_win_percentages(self):
        """
        Creates a bar plot showing the percentage of wins for each player.
        """
        # Calculate total number of completed games
        total_wins = sum(self.win_counts.values())
        
        if total_wins == 0:
            print("No completed games to calculate win percentages.")
            return
        
        # Calculate win percentages
        win_percentages = {player: (count / total_wins * 100) for player, count in self.win_counts.items()}
        
        # Sort players by win percentage (descending)
        sorted_players = sorted(win_percentages.keys(), key=lambda x: win_percentages[x], reverse=True)
        sorted_percentages = [win_percentages[player] for player in sorted_players]
        
        # Create bar plot
        plt.figure(figsize=(10, 6))
        bars = plt.bar(sorted_players, sorted_percentages, color='skyblue', edgecolor='navy')
        
        # Add percentage labels on top of bars
        for bar, percentage in zip(bars, sorted_percentages):
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 1,  # Add a small offset
                f'{percentage:.1f}%',
                ha='center',
                va='bottom',
                fontweight='bold'
            )
        
        plt.xlabel("Players")
        plt.ylabel("Win Percentage (%)")
        plt.title("Percentage of Wins by Player")
        plt.ylim(0, max(sorted_percentages) * 1.15)  # Add some space for labels
        plt.grid(True, linestyle='--', alpha=0.7, axis='y')
        
        # Add the number of wins as a second label
        for i, player in enumerate(sorted_players):
            wins = self.win_counts[player]
            plt.text(
                i,  # x position of bar
                5,  # Fixed position near the bottom of the bar
                f'({wins} wins)',
                ha='center',
                va='bottom',
                color='navy'
            )
        
        plt.tight_layout()
        plt.savefig("win_percentages.png")
        plt.show()

# END OF FILE - analyzer.py