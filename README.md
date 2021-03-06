# Game Set (command line version) #

### Rules ###
Each card has four properties: color, shape, fill, count. A card is represented by a symbol representing its shape and fill which is repeated _n_ times depending on its count, and preceeded by a letter indicating its color (e.g. _r_ for _red_). 

A set is a combination of three cards for which each of these individual properties are all the same, or all different. 

Example of a board:
~~~~
g■  	g▣  	g▢
b■■ 	b■■■	r■■■
g■■ 	b▣  	r●●
~~~~

Example of a set on this board: `r■■■ b■■ , g■` (same shape, same fill, different counts, different colors.)
### Usage ###
`python3 play.py`

Play options:

* _set_: to enter a set in tuple format; e.g. `(1, 2), (1, 0), (0, 0)`
* _redraw_: redraw the current board; all current cards on the board are replaced.
* _info_: report number of available sets; in this case 2. 
* _hint_: get a hint; e.g. `b■■` 
* _status_: report current game status in terms of sets found, time passed, hints requested, etc. 
* _quit_: exit the game.
