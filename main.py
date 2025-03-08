# FILE: main.py
# Date: 2025-03-08
# Author: Efe Gorkem Sirin
# Description: This file contains the main function to run the Monopoly game.

from analyzer import MonopolyAnalyzer
from monopoly import Game
import sys
import json

def main():
    try:
        print_flag = False
        analysis_flag = False
        json_load = False
        json_name = None
        demo = False
        seed = None

        args = sys.argv
        for i in range(1, len(args)):
            if args[i] == "-h" or args[i] == "--help":
                print("Usage: python main.py [-h] [-d] [-p] [-a] [-f JSON_FILE]")
                print("Options:")
                print("  -h, --help      show this help message and exit")
                print("  -d              run in demo mode")
                print("  -p              print the game board")
                print("  -a              print the analysis of the game")
                print("  -s SEED         set the random seed for the game")
                print("  -f JSON_FILE    load the game from a JSON file")
                return
            elif args[i] == "-d":
                demo = True
            elif args[i] == "-p":
                print_flag = True
            elif args[i] == "-s":
                if i == len(args) - 1:
                    raise ValueError("Please provide a seed number with the -s flag.")
                seed = int(args[i+1])
            elif args[i] == "-a":
                analysis_flag = True
            elif args[i] == "-f":
                if i == len(args) - 1:
                    raise ValueError("Please provide a JSON file name with the -f flag.")
                json_load = True
                json_name = args[i+1]
                break
        
        if json_load and (not json_name or json_name == ""): 
            raise ValueError("Please provide a JSON file name with the -f flag.")

        game_data = None
        if json_load:
            # Load the JSON content
            with open(json_name, "r") as f:
                game_data = json.load(f)

        if not analysis_flag:

            game = Game(seed)

            if demo:
                game.load_players_npl([["Efe", "Hat", "DEFAULT"], ["Oza", "Dog", "NOSPEND"], ["Sude", "Duck", "NOSPEND"], ["Can", "Car", "NOSPEND"]], print_flag, analysis_flag)
            else:
                assert game_data is not None, "Please provide a JSON file with the -f flag."
                game.load_from_json(game_data)

            game.play_game()

        else:
            analyzer = MonopolyAnalyzer(game_data, seed)
            analyzer.analyze()

    except ValueError as e:
        print(e)
    except KeyboardInterrupt:
        game.handle_exit(None, None)
    except Exception as e:
        print(e)
        game.handle_exit(None, None)

if __name__ == "__main__":
    main()

# END OF FILE - main.py