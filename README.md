# chess-accuracy
<b> USAGE </b>
<br>
1 Download the code <br>
2 cd /directory of code<br>
3 import accuracy<br>
4 accuracy.accuracy(file, stockfish, blunder_threshold = -100,analysis_time = 0.1)<br>
<br>
where<br>
      file = path of pgn file<br>
      stockfish = path of stockfish binary<br>
      blunder_threshold = blunder threshold in centipawns. you may change if you like<br>
      analysis_time = analysis time of stockfish per move<br>
After completion of code, a file chess.csv containing accuracy calculations is saved in working directory<br>
<br>
<b> Requirements </b>
1 python-chess<br>
2 pandas<br>

<b> License </b>
[**GNU General Public License version 3**] (GPL v3). Essentially,
this means you are free to do almost exactly what you want with the program,
including distributing it among your friends, making it available for download
from your website, selling it (either by itself or as part of some bigger
software package), or using it as the starting point for a software project of
your own.
