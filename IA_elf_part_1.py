# -*- coding: utf-8 -*-

orders = ''

for unit in units["player_%d" % player]:
        possible_moves = [] 
        possible_attacks = []

if player == 1:
            enemy_player = 'player_2'
else:
            enemy_player = 'player_1'  #code de Florian mais à mettre devant pour que notre code fonctionne ensemble


if units["player_%d" % player][unit]["type"] == "E":

    
    if (units[enemy_player][enemy_unit]["coordinates"] - units["player_%d" % player][unit]["coordinates"]) <= 1:
            if  x-1 >= 0 and y-1 >= 0:
                possible_moves.append([x-1,y-1])
            if  x+1 < boardsize and y-1 >= 0:
                possible_moves.append([x+1,y-1])
            if  x-1 >= 0 and y+1 < boardsize:
                possible_moves.append([x-1,y+1])  
            if  x+1 < boardsize and y+1 < boardsize:
                possible_moves.append([x+1,y+1])
    
    

    elif (units[enemy_player][enemy_unit]["coordinates"] - units["player_%d" % player][unit]["coordinates"]) <= 2: 
            for mod_x in range(-2,3):
                for mod_y in range (-2,3):
                    if y + mod_y < boardsize or x + mod_x < boardsize:
                        possible_attacks.append(x+mod_x,y+mod_y)

    else:
            safe_square = False
            index = 0
            while index < len(possible_moves) and safe_square == False:
                
                can_move = True
                for players in units:
                    for player_unit in units[players]:
                        if units[players][player_unit]['coordinates'] == possible_moves[index]:
                            can_move = False
                if can_move:
                    unit_near = False
                    for k in range(-3,4):
                        for l in range (-3,4):
                            for player_unit in units[enemy_player]:
                                if units[enemy_player][player_unit]['coordinates'] == [possible_moves[index][0] + k,possible_moves[index][1] + l]:
                                    unit_near = True
                if not unit_near:
                    safe_square = True
                else:
                    i += 1
                        
            if safe_square:
                orders += "%.2d-%.2d -m-> %.2d-%.2d   " % (x, y, possible_moves[i][0], possible_moves[i][1])
