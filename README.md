This Python script analyzes chess games from PGN files using the python-chess library and the Stockfish chess engine, calculating the accuracy and blunder rate for both White and Black players in each game.<br>
<br>

<b>Dependencies</b><br>
python-chess: pip install chess<br>
pandas: pip install pandas<br>

<b>How to use</b><br>
Install Stockfish:<br>
You need to have the Stockfish chess engine installed on your system. You can download it from the official Stockfish website.<br>

<b>Setup</b>:<br>

Place your PGN file containing the chess games in the same directory as the script.<br>
Edit the script to set the correct path for the Stockfish binary in the stockfish variable.<br>
If needed, adjust the blunder_threshold and analysis_time parameters.<br>
Run the Script:<br>
Run the Python script in a terminal or an IDE.<br>

<b> USAGE </b> <br>
python your_script_name.py<br>
Script Parameters<br>
file (str): Path to the PGN file containing the chess games<br>
stockfish (str): Path to the Stockfish binary.<br>
blunder_threshold (int, optional): The threshold for the evaluation difference to consider a move as a blunder. Defaults to -100.<br>
analysis_time (float, optional): The time in seconds that Stockfish will spend analyzing each move. Defaults to 0.1.<br>
Output<br>
The script outputs a CSV file named chess.csv containing the analysis results, including accuracy and blunder counts for both White and Black in each game.<br>
<br>
<b>Example</b><br>
accuracy("path_to_your_pgn_file.pgn", "path_to_your_stockfish_binary")<br>
Important Notes<br>
Ensure that you have the necessary permissions to read the PGN file and write the output CSV file to the specified locations.
The script processes each game in the PGN file one by one and appends the results to the output CSV file, so it can handle large PGN files efficiently.
The script may take a considerable amount of time to run, depending on the analysis_time parameter and the number of games in the PGN file.
Remember to replace placeholder texts like your_script_name.py, path_to_your_pgn_file.pgn, and path_to_your_stockfish_binary with the actual names/paths in your project.
