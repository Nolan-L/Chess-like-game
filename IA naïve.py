# -*- coding: utf-8 -*-
    # Creation of the IA
    
def AI(units, boardsize):
    """
    Basic AI that search for the best move and return a decision.
    
    Parameters:
    -----------
    units: the list of units and information related. (dict)
    boardsize: the size of the board. (int)
    
    Returns:
    --------
    Decision: a string of the next move played by the AI. (str)
        
    Notes:
    ------
    None
    
    Version:
    --------
    specification: Nolan Lefèvre 
    implementaion: Nolan Lefèvre 
    """    
    # Imports    
          
import random

     # Creation of dictionnary
     
possible_moves = []
possible_attacks = []
      
for i in range(0,8) :
    for j in range(0,8) :
        for k in range(0,8) :
            for l in range(0,8) : 
                possible_moves.append ("0"+str(i)+"-0"+str(j)+ " -m> "+"0"+ str(k)+"-0"+str(l)+"   ")
                possible_attacks.append ("0"+str(i)+"-0"+str(j)+ " -a> "+"0"+ str(k)+"-0"+str(l)+"   ")


    # Random actions
number_of_actions = 0
while number_of_actions < 8:
        random_possibilities = random.randint(0, 1)
        if random_possibilities == 0:
            print (random.choice(possible_moves))
        else:
            print (random.choice(possible_attacks))
        number_of_actions = number_of_actions + 1
