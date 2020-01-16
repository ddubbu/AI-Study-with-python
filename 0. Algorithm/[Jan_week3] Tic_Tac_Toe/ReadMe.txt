0. Problem
- Assume that "X" has priority 
	and 2 Player does their best (= same stratege/skill)
- Find who does win? (or "TIE")

1. format of Input file
- ( "X", " O",  "." ) is split with blank
- "X" and "O" is capital letter

2. format of output file
- express among ( "TIE", "X", "O" ) considering who does win?

3. I use Class object attribution or method
- different with last assign1, I define many method
- It is useful for managing object and using method often
	Q. How about this? It's better coding skill than before?

4. Check stone map with Console
- I added Time Stamp such as turn round in stone map.
	init condition is added with "s" 
- for Example, 
	. . .
	. . X
	. O .
it can convert under and start to program
	.s .s .s 
	.s .s Xs
	.s Os .s
and if push "X" on [0,0] and "O" on [1,1], These add in map with time stamp
	X1 .s .s 
	.s O2 Xs
	.s Os .s

5. Finally, How to implement this program?
- I use "Minimax" Algorithm"
- I refer to this website. 
https://github.com/CodingTrain/website/tree/master/CodingChallenges/CC_154_Tic_Tac_Toe_Minimax

6. What did you apply?
- There's java-script code. I converted it with python.
- And well-made program is for game with AI (= "X" Player). 
	In other words,  I added a code for "O" Player which can be controlled with different score board in same minimax function.
	if "X" turn, score board needs that "X" is +1
	(likewise) if "O" turn, score board needs that "O" is +1 
- I define Class for Map. so, I can manage useful function and attribution easily.
- For check, I draw the (stone) map_status on console not website.


7. What is difficult ?
- I don't have idea for the problem. for thinking, I spent around 2 days. 
	Eventually, I refer to other code. but I want to apply it for making my code.
- what is "minimax" algorithm ?
	In [Algorithm] subject, I learned NP-Complete.
	This is only 3X3 . but it has 9! cases..... so I think it's a np-complete to me.. kk

	It researchs all cases that we can lay the stone.
		( if it has too many cases, we can use branching with upper and lower limit )
		( I don't use this )
	If we choose final case, we can get choose tree and scores (at the external node).
	finally, we choose case with toggling between min/max score in each depth.

# I solved under problem. With differenct score board, I can use same minimax function!
- function maximin() is not for minimize. It's same with minimax(). 
	but maximin() is for finding the location to lay for "O"  like that minimax() for "X"
	so I think that simply if turn == "O", use minimax() in researching for minimum score.  
	anyway, I think it can more simply.

- It's difficult to "tic-tae-toe", but how complex the "Alpha-Go" is for "Baduk"
- anyway, I'd like to receive your feedback :-)