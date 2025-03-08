# Monopoly Game Analyzer

Have you ever wondered who would win a game of Monopoly based on the current game state? This tool allows you to analyze and simulate Monopoly games to determine the winner based on a given game state in JSON format. It can also generate statistical analysis and visualizations of multiple game simulations.

## Features

- Load game state from a JSON file.
- Simulate the game to determine the winner.
- Analyze multiple game simulations to generate win statistics.
- Generate visualizations for average money over time and win percentages.

## Usage

### Command Line Options

- `-h, --help`: Show the help message and exit.
- `-d`: Run in demo mode.
- `-p`: Print the game board.
- `-a`: Print the analysis of the game.
- `-s SEED`: Set the random seed for the game.
- `-f JSON_FILE`: Load the game from a JSON file.

### Example Commands

To run the game in demo mode:
```sh
python main.py -d
```

To load a game from a JSON file and print the game board:

```sh
python main.py -f input.json -p
```

To analyze the game from a JSON file:

```sh
python main.py -f input.json -a
```

JSON File Format
The JSON file should contain the game state, including player information, properties owned, and their status. Below is an example of the JSON format:

```json
{
    "players": [
        {
            "name": "Oza",
            "piece": "Dog",
            "position": 0,
            "money": 300,
            "properties": [
                {
                    "name": "The Angel Islington",
                    "mortgaged": false,
                    "houses": 5
                },
                {
                    "name": "Euston Road",
                    "mortgaged": false,
                    "houses": 5
                }
                // More properties...
            ],
            "logic": "TACTICAL",
            "getOutOfJailCard": 0
        },
        {
            "name": "Efe",
            "piece": "Hat",
            "position": 0,
            "money": 300,
            "properties": [
                {
                    "name": "Old Kent Road",
                    "mortgaged": false,
                    "houses": 5
                },
                {
                    "name": "Whitechapel Road",
                    "mortgaged": false,
                    "houses": 5
                }
                // More properties...
            ],
            "logic": "TACTICAL",
            "getOutOfJailCard": 0
        }
        // More players...
    ]
}
```


## Output
The tool generates two main outputs:

Win Percentages: A bar plot showing the percentage of wins for each player.
Money vs Time: A line plot showing the average money of each player over time with standard deviation.

## Dependencies

No external libraries are required to run the tool.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
```
