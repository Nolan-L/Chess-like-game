# -*- coding: UTF-8 -*-
import random
import remote_play


def play(first_player, second_player, boardsize=7, randomize_turn=False, remote_IP='127.0.0.1'):
    """
    Start the game.
    
    Parameters:
    -----------
    first_player: The type of the first player (str)
    second_player: The type of the second player (str)
    boardsize: the size of the board.(int, optionnal)
    randomize_turn: True if the first player is randomized, False if the player define who starts. (bool, optionnal)
    remote_ip: The ip address of the distant player. (str, optionnal)
    
    Returns:
    --------
    None
    
    Notes:
    ------
    Size has to be between 7 and 20. If out of the boundaries, 
    the value will be set by the min or the max.
    
    Raises:
    -------
    ValueError: if boardsize is not an integer.
    
    Version:
    --------
    specification: Nolan Lefèvre
    implementation: Nolan Lefèvre
    """

    # Set variables
    
    game_state  = True
    counter = 0
    
    # Check boardsize.
    
    if type(boardsize) is not int:
        raise ValueError("boardsize has to be an integer.")
        
    if boardsize < 7:
        boardsize = 7
    elif boardsize > 20:
        boardsize = 20
     
    # Create the board and the data structure.
    
    units = data_creation(boardsize)
    
    # Display the logo and the rules
    
    logo_and_rules_display()   
 
    # Display the board.
    
    display_board(units, boardsize)
    
    # Choose the first player.
    if randomize_turn == True:    
        if random.randint(0, 1)== 0:
            player1 = first_player
            player_turn = 0
        
        else:
            player1 = second_player
            player_turn = 1
    else:
        player1 = first_player
        player_turn = 0
        
    print ('player 1 is %s') % player1
     
    #connecting to the remote player
    connected = False
    if remote_IP != '127.0.0.1':
        if player1 == 'distant':
            connection = remote_play.connect_to_player(1, remote_IP, verbose=False)
        else:
            connection = remote_play.connect_to_player(2, remote_IP, verbose=False)
        connected = True

    
    # Main loop of the game.
        
    while game_state:
          
        orders = ''
        if player_turn == 0:
            if first_player == 'AI':
                orders = AI(units, boardsize, 1)
                if connected:
                    remote_play.notify_remote_orders(connection, orders)
            elif first_player == 'distant':
                orders = remote_play.get_remote_orders(connection)
            else:
                orders = raw_input('What do you want to play? ')
                if connected:
                    remote_play.notify_remote_orders(connection, orders)
            
            print ('player 1 turn')
            #print 'player %d turn' % (1 if player1 == 'player' else 2)
            #orders = AI(units, boardsize, 1 if player1 == 'player' else 2)
            actions = split_and_sort_input(orders, 1, units)
            player_turn = 1
        else:
            if second_player == 'AI':
                orders = AI(units, boardsize, 2)
                if connected:
                    remote_play.notify_remote_orders(connection, orders)
            elif second_player == 'distant':
                orders = remote_play.get_remote_orders(connection)
            else:
                orders = raw_input('What do you want to play? ')
                if connected:
                    remote_play.notify_remote_orders(connection, orders)
            
            print ('player 2 turn')
            #print 'player %d turn' % (1 if player1 == 'IA' else 2)
            #orders = AI(units, boardsize, 1 if player1 == 'IA' else 2)
            actions = split_and_sort_input(orders, 2, units)
            player_turn = 0
                        
        units, time_update = perform_actions(actions,units, boardsize)
               
        if time_update:
            counter += 0.5
        else:
            counter = 0
        
        display_board(units, boardsize)
        game_state = score_computing(units,counter,player1)
        
    remote_play.disconnect_from_player(connection)
        
"""--------------------------------------------------------------------------"""
def data_creation(boardsize=7):
    """
    Creation of the gameboard.
     
    Parameters:
    -----------
    boardsize: size of the board (int)(optionnal)
     
    Returns:
    --------
    units: The list of the units and informations related. (dict)
     
    Notes:
    ------
    Size has to be between 7 and 20. If out of the boundaries, 
    the value will be set by the min or the max.
     
    Version:
    --------
    specification: Nolan Lefèvre
    implementation: Nolan Lefèvre
 
    """
     
    player_1 = {'elf_1':{'type':'E', 'life': 4, 'coordinates':[0,0]}, 'elf_2':{'type':'E', 'life': 4, 'coordinates':[0,1]}, 'elf_3':{'type':'E', 'life': 4, 'coordinates':[0,2]}, 'elf_4':{'type':'E', 'life': 4, 'coordinates':[1,0]}, 'elf_5':{'type':'E', 'life': 4, 'coordinates':[2,0]}, 'dwarf_1':{'type':'D', 'life': 10, 'coordinates':[1,1]}, 'dwarf_2':{'type':'D', 'life': 10, 'coordinates':[1,2]}, 'dwarf_3':{'type':'D', 'life': 10, 'coordinates':[2,1]}}
    player_2 = {'elf_1':{'type':'E', 'life': 4, 'coordinates':[4 + (boardsize - 7),6 + (boardsize - 7)]}, 'elf_2':{'type':'E', 'life': 4, 'coordinates':[5 + (boardsize - 7),6 + (boardsize - 7)]}, 'elf_3':{'type':'E', 'life': 4, 'coordinates':[6 + (boardsize - 7),4 + (boardsize - 7)]}, 'elf_4':{'type':'E', 'life': 4, 'coordinates':[6 + (boardsize - 7),5 + (boardsize - 7)]}, 'elf_5':{'type':'E', 'life': 4, 'coordinates':[6 + (boardsize - 7),6 + (boardsize - 7)]}, 'dwarf_1':{'type':'D', 'life': 10, 'coordinates':[4 + (boardsize - 7),5 + (boardsize - 7)]}, 'dwarf_2':{'type':'D', 'life': 10, 'coordinates':[5 + (boardsize - 7),4 + (boardsize - 7)]}, 'dwarf_3':{'type':'D', 'life': 10, 'coordinates':[5 + (boardsize - 7),5 + (boardsize - 7)]}}
     
    units = {'player_1':player_1, 'player_2':player_2}
     
    return units
 
"""--------------------------------------------------------------------------"""
 
def display_board(units, boardsize=7):
    """
    Displaying the gameboard.
     
    Parameters:
    -----------    
    units: The list of the units and informations related. (dict)
    boardsize: size of the board (int)(optionnal)
     
    Returns:
    --------
    None
     
    Version:
    --------
    specification: Nolan Lefèvre
    implementation: Nolan Lefèvre
 
    """
     
    board = '\ ' 
    for n in range(boardsize):
        board += '%d ' % n if n < 10 else '%d' % n
    board += '\n'
    piece = False
     
    for line in range(boardsize):
        board += '%d ' % line if line < 10 else '%d' % line
        for column in range(boardsize): 
            for player in (1, 2):
                for unit in units['player_%d' % player]:
                    if [column, line] == units['player_%d' % player][unit]['coordinates']:
                        board += '%s%s \033[0m' % (get_color(player, units['player_%d' % player][unit]['type'], units['player_%d' % player][unit]['life']), units['player_%d' % player][unit]['type'])
                        piece = True
            if piece == False:
                board += '- '
            piece = False
        board += '\n' 
    print ('units: '+'\033[%smD  \033[%smD  \033[%smD  \033[%smD\033[30m'%('34','32','33','31') + ' and \033[%smE \033[%smE \033[%smE \033[%smE \033[30m'%('34','32','33','31'))
    print ('life: >7 >4 >2 <2 and 4 3 2 1')
    print (board)
 
"""--------------------------------------------------------------------------"""
 
def get_color(player, race, hp):
    """
    Return the color symbol of the unit on the board related to it's race and hp
    and the background color related to the player ( to whom belongs the unit ).
     
    Parameters:
    -----------
    player: the player to whom belongs the unit. (int)
    race:  the race of the unit. (str)
    hp : the health of the unit. (str)
     
    Returns:
    --------
    Color: the color code that fit to the unit.(str)
         
    Raises:
    -------
    ValueError: if the dwarf's health is not between 1 and 10 or if the
    elf's health is not between 1 and 4.
    ValueError: if player doesn't exist.
    ValueError: if race doesn't exist.
     
    Note:
    -----
    None
     
    Version:
    --------
    specification: Nolan Lefèvre
    implementation: Nolan Lefèvre
     
    """
    if player == 1:
        player_color = '46'
    else:
        player_color = '47'
         
    if race == 'E':
        if hp > 3:
            hp_color = '34'
        elif hp > 2:
            hp_color = '32'
        elif hp > 1:
            hp_color = '33'
        else:
            hp_color = '31'   
    else:
        if hp > 7:
            hp_color = '34'
        elif hp > 4:
            hp_color = '32'
        elif hp > 2:
            hp_color = '33'
        else:
            hp_color = '31'
             
    color = '\033[%s;%sm' % (player_color, hp_color)
     
    return color
     
"""--------------------------------------------------------------------------"""
 
def split_and_sort_input(p_input, player, units):
    """
    Take the player's input, split it in different string for each action and
    put it into lists.
     
    Parameters:
    -----------
    p_input: the player's input. (str)
    player: the player to whom belongs the unit. (int)
    units: The list of the units and informations related. (dict)
     
    Returns:
    --------
    Act_list: A list of all actions sorted.
     
    Note:
    -----
    None
     
    Version:
    --------
    specification: Nolan Lefèvre
    implementation: Nolan Lefèvre
     
    """
     
    act_list = []
     
    while len(p_input) > 0:
        action = p_input[0:19]
        p_input = p_input[19:len(p_input)]
             
        if action != '':                            
            act_list.append([[int(action[0:2]), int(action[3:5])], [int(action[11:13]), int(action[14:16])], action[7]])
     
    index = 0
                     
    while index < len(act_list):
        belong_to_player = False
        ally = False
        for unit in units['player_%d' % player]:
            if units['player_%d' % player][unit]['coordinates'] == act_list[index][0]:
                belong_to_player = True
                
        if not belong_to_player:
            print ('The unit on %s does not belong to the player') % str(act_list[index][0])
 
            if units['player_%d' % player][unit]['coordinates'] == act_list[index][1] and act_list[index][2] == 'a':
                ally = True
                print ('The unit you try to attack on %s is an ally') % act_list[index][1]
                 
        if not belong_to_player or ally:
            del act_list[index]
        else:
            index += 1
             
    index = 0
 
    while index < len(act_list):
        can_do_action = True
        for unit in range(index):
            if act_list[index][0] == act_list[unit][1] or (act_list[index][0] == act_list[unit][0] and act_list[unit][2] == 'a'):
                can_do_action = False
     
        if not can_do_action:
            del act_list[index]
        else:
            index += 1
         
    return act_list
 
     
"""--------------------------------------------------------------------------"""
 
def move(origin,destination, units, boardsize):
    """
    Verify if the move is possible and move the unit.
     
    Parameters:
    -----------
    origin: the square where the unit stands. (str)
    destination: the square the unit wants to reach. (str)  
    units: the list of the units and informations related. (dict)
    boardsize: the size of the board.(int)
     
    Returns:
    --------
    units:the list of the units and informations related. (dict)
     
    Notes:
    ------
    An unit cannot move out of the board or on an occupied square.
    A dwarf can only move one square straight ahead in all direction but not in diagonals.
    An elf can move one square in all directions. (diagonals included)
     
    Version:
    --------
    specification: Nolan Lefèvre
    implementation: Nolan Lefèvre
     
    """
     
    can_move = True
     
    for player in ('player_1', 'player_2'):
        for unit in units[player]:
            if units[player][unit]['coordinates'] == destination:
                can_move = False
     
    if destination[0] < 0 or destination[0] >= boardsize or destination[1] < 0 or destination[1] >= boardsize:
        can_move = False
                                                     
    if can_move:
        for player in units:
            for unit in units[player]:
                if units[player][unit]['coordinates'] == origin:
                    if units[player][unit]['type'] == 'E':
                        if (-1 <= destination[0] - origin[0] <= 1) and (-1 <= destination[1] - origin[1] <= 1):
                            units[player][unit]['coordinates'] = destination
                        else:
                            print ("cannot move %s to %s") % (str(origin), str(destination))
                         
                    elif units[player][unit]['type'] == 'D':
                        if ((-1 <= destination[0] - origin[0] <= 1) and destination[1] - origin[1] == 0) or (destination[0] - origin[0] == 0 and (-1 <= destination[1] - origin[1] <= 1)):
                            units[player][unit]['coordinates'] = destination
                        else:
                            print ("cannot move %s to %s") % (str(origin), str(destination))
                            
    else:
        print ("cannot move %s to %s") % (str(origin), str(destination))
                         
    return units   

"""--------------------------------------------------------------------------"""

def perform_actions(actions,units, boardsize):
    """
    Perform a move and/or attacks following the player's decision.
        
    Parameters:
    -----------
    actions: player's input sorted in a list. (list)
    units: the list of units and information related. (dict)
    boardsize: the size of the board.(int)
    
    Returns:
    --------
    units: The list of the units and informations related. (dict)
    time_update: if an attack has been performed. (bool) 
    
    Notes:
    ------
    None
    
    Version:
    --------
    specification: Nolan Lefèvre
    implementation: Nolan Lefèvre
    """

    time_update = True

    for element in actions:    
        if element[2] == "m":
            units = move(element[0],element[1],units, boardsize)
                
        else:
            units,state = attack(element[0],element[1],units)
                
            if state:
                time_update = False
                
        
    return units, time_update
    
"""--------------------------------------------------------------------------"""

def score_computing(units,counter,player1):
    """
    Compute the score in case of 20 turns without any action/fight.
    
    Parameters:
    -----------
    units: the list of the units and information related. (dict)
    counter: the amount turns without any fight. (int)
    player1: the player that has played the first. (str)
    
    Returns:
    --------
    game_state: False if the game is ended. (Bool)
    
    Notes:
    ------
    None
    
    Version:
    --------
    specification: Nolan Lefèvre
    implementation: Nolan Lefèvre
     
    """
    players =["Player 1","Player 2"]
    life_total = [0,0]
    winner = ""
    
    
    
    if counter != 20:
        if units["player_1"] !={} and units["player_2"] != {}:
            return True
        elif units["player_1"] == {}:
            winner = players[1]
        elif units["player_2"] == {}:
            winner = players[0]
        
    else:
        if len(units["player_1"]) == len(units["player_2"]):
                       
            for unit in units["player_1"]:
                life_total[0] +=  units["player_1"][unit]["life"]
            for unit in units["player_2"]:
                life_total[1] +=  units["player_2"][unit]["life"]
            
            if life_total[0] > life_total[1]:
                winner = players[0]
            elif life_total [0] < life_total[1] :
                winner = players[1]
            else:   
                if player1 == "AI":
                    winner = players[0]
                else:
                    winner = players[1]
                    
        elif len(units["player_1"])> len(units["player_2"]):
            winner = players[0]        
        else:
            winner = players[1]
    
    print ("Congratulation, %s has won!")%(winner)       
    return False
    
def attack(origin, destination, units):
    """
    Verify if an attack is possible and do it.
    
    Parameters:
    -----------
    origin: the square where the unit stands. (str)
    destination: the square the unit wants to attack. (str)  
    units: The list of the units and informations related. (dict)
    
    Returns:
    --------
    units: The new list of units and information related. (dict)
    state: True if the unit has attacked else False. (bool)
    
    Notes:
    ------
    A dwarf can only attack adjacent units (diagonals included).
    An elf can attack up to two squares around it (diagonals included).
    
    Version:
    --------
    specification: Nolan Lefèvre
    
    """
    
    #Gathering informations
    
    unit_d_info = None
    
    for player in ('player_1', 'player_2'):
        for unit in units[player]:
            if units[player][unit]['coordinates'] == origin:
                unit_o_owner = player
                unit_o_info = units[player][unit]
            if units[player][unit]['coordinates'] == destination:
                unit_d_owner = player
                unit_d = unit
                unit_d_info = units[player][unit]
                
    
    #Checking if the unit can attack
    
    can_attack = True
    
    if unit_d_info == None:
        can_attack = False
    else:
        dist_x = abs(unit_o_info["coordinates"][0] - unit_d_info["coordinates"][0])
        dist_y = abs(unit_o_info["coordinates"][1] - unit_d_info["coordinates"][1])
    

        if unit_o_owner == unit_d_owner:
            can_attack = False
        
        if unit_o_info['type'] == 'D':
            if dist_x > 1 or dist_y > 1:
                can_attack = False
            
        else:
            if dist_x >2 or dist_y > 2:
                can_attack = False
    
    
    #Performing the attack
    
    if can_attack:
        if unit_o_info['type'] == 'D':
            units[unit_d_owner][unit_d]['life'] -= 2
        else:
            units[unit_d_owner][unit_d]['life'] -= 1    
        
        if units[unit_d_owner][unit_d]['life'] <= 0:
                del(units[unit_d_owner][unit_d])
        state = True
    else:
        state = False
        
    return units, state
     
    
def AI(units, boardsize, player):
    """
    Basic AI that search for the best move and return a decision.
    
    Parameters:
    -----------
    units: the list of units and information related. (dict)
    boardsize: the size of the board. (int)
    player: the player to whom belongs the unit. (int)
    
    Returns:
    --------
    Decision: a string of the next move played by the AI. (str)
        
    Notes:
    ------
    None
    
    Version:
    --------
    specification: Nolan Lefèvre
    implementation: Nolan Lefèvre
    
    """
 
    orders = ""
    
    #Defining the possibles movement of each units
    
    all_moves = []
    
    for unit in units["player_%d" % player]:
        possible_moves = [] 
        possible_attacks = []
         
        x,y = units["player_%d" % player][unit]["coordinates"][0],units["player_%d" % player][unit]["coordinates"][1]
        
        #Defining all possible moves
        
        if y-1 >= 0:
            possible_moves.append([x,y-1])
        if y+1 < boardsize:
            possible_moves.append([x,y+1])
        if x-1 >= 0:
            possible_moves.append([x-1,y])
        if x+1 < boardsize:
            possible_moves.append([x+1,y])
        if units["player_%d" % player][unit]["type"] == "E":
            if  x-1 >= 0 and y-1 >= 0:
                possible_moves.append([x-1,y-1])
            if  x+1 < boardsize and y-1 >= 0:
                possible_moves.append([x+1,y-1])
            if  x-1 >= 0 and y+1 < boardsize:
                possible_moves.append([x-1,y+1])  
            if  x+1 < boardsize and y+1 < boardsize:
                possible_moves.append([x+1,y+1])
        
        #Defining all possible attacks
        
        if y-1 >= 0:
            possible_attacks.append([x,y-1])
        if y+1 < boardsize:
            possible_attacks.append([x,y+1])
        if x-1 >= 0:
            possible_attacks.append([x-1,y])
        if x+1 < boardsize:
            possible_attacks.append([x+1,y])
        if  x-1 >= 0 and y-1 >= 0:
            possible_attacks.append([x-1,y-1])
        if  x+1 < boardsize and y-1 >= 0:
            possible_attacks.append([x+1,y-1])
        if  x-1 >= 0 and y+1 < boardsize:
            possible_attacks.append([x-1,y+1])  
        if  x+1 < boardsize and y+1 < boardsize:
            possible_attacks.append([x+1,y+1])
        
        if units["player_%d" % player][unit]["type"] == "E":   
            if y-2 >= 0:
                possible_attacks.append([x,y-2])
            if y+2 < boardsize:
                possible_attacks.append([x,y+2])
            if x-2 >= 0:
                possible_attacks.append([x-2,y])
            if x+2 < boardsize:
                possible_attacks.append([x+2,y])
            if x-2 >= 0 and y-2 >= 0:
                possible_attacks.append([x-2,y-2])
            if x-2 >= 0 and y-1 >= 0:
                possible_attacks.append([x-2,y-1])
            if x-2 >= 0 and y+2 < boardsize:
                possible_attacks.append([x-2,y+2])
            if x-2 >= 0 and y+1 < boardsize:
                possible_attacks.append([x-2,y+1])
            if x-1 >= 0 and y-2 >= 0:
                possible_attacks.append([x-1,y-2])
            if x-1 >= 0 and y+2 < boardsize:
                possible_attacks.append([x-1,y+2])
            if x+1 < boardsize and y-2 >= 0:
                possible_attacks.append([x+1,y-2])
            if x+1 < boardsize and y+2 < boardsize:   
                possible_attacks.append([x+1,y+2])
            if x+2 < boardsize and y-2 >= 0:
                possible_attacks.append([x+2,y-2])
            if x+2 < boardsize and y-1 >= 0:
                possible_attacks.append([x+2,y-1])
            if x+2 < boardsize and y+1 < boardsize:
                possible_attacks.append([x+2,y+1])
            if x+2 < boardsize and y+2 < boardsize:
                possible_attacks.append([x+2,y+2])
                
        #Choosing the action to do (move or attack) 
        
        if random.randint(0, 1) == 0:
            random_move = possible_moves[random.randint(0, len(possible_moves) - 1)]
            
            can_move = True
            
            if random_move in all_moves:
                can_move = False
     
            for players in ('player_1', 'player_2'):
                for unit in units[players]:
                    if units[players][unit]['coordinates'] == random_move:
                        can_move = False
            
            if can_move:
                all_moves.append(random_move)
                orders += "%.2d-%.2d -m-> %.2d-%.2d   " % (x, y, random_move[0], random_move[1])
        
        else:
            random_attack = possible_attacks[random.randint(0, len(possible_attacks) - 1)]
            
            can_attack = True
            not_empty_square = False
            
            for players in units:
                for unit in units[players]:
                    if units[players][unit]['coordinates'] == random_attack:
                        not_empty_square = True
                
            for unit in units["player_%d" % player]:
                if units["player_%d" % player][unit]['coordinates'] == random_attack:
                    can_attack = False
                    
            if can_attack and not_empty_square:
                orders += "%s-%s -a-> %s-%s   " % (str(x) if x > 10 else '0'+str(x), str(y) if y > 10 else '0'+str(y), str(random_attack[0]) if random_attack[0] > 10 else '0'+str(random_attack[0]), str(random_attack[1]) if random_attack[1] > 10 else '0'+str(random_attack[1]))
    print (orders)
    return orders

def logo_and_rules_display():
    """
    Display the logo of the game gradually and rules.
    
    Parameters:
    -----------
    None
    
    Returns:
    --------
    None
    
    Notes:
    ------
    None
    
    Version:
    --------
    specification: Nolan Lefèvre
    implementation: Nolan Lefèvre 
    
    """
    print ("""
███████╗██╗    ██╗   ██╗███████╗███████╗     █████╗ ███╗   ██╗██████╗     ██████╗ ██╗    ██╗ █████╗ ██████╗ ███████╗███████╗
██╔════╝██║    ██║   ██║██╔════╝██╔════╝    ██╔══██╗████╗  ██║██╔══██╗    ██╔══██╗██║    ██║██╔══██╗██╔══██╗██╔════╝██╔════╝
█████╗  ██║    ██║   ██║█████╗  ███████╗    ███████║██╔██╗ ██║██║  ██║    ██║  ██║██║ █╗ ██║███████║██████╔╝█████╗  ███████╗
██╔══╝  ██║    ╚██╗ ██╔╝██╔══╝  ╚════██║    ██╔══██║██║╚██╗██║██║  ██║    ██║  ██║██║███╗██║██╔══██║██╔══██╗██╔══╝  ╚════██║
███████╗███████╗╚████╔╝ ███████╗███████║    ██║  ██║██║ ╚████║██████╔╝    ██████╔╝╚███╔███╔╝██║  ██║██║  ██║██║     ███████║
╚══════╝╚══════╝ ╚═══╝  ╚══════╝╚══════╝    ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝     ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝
                                                                                                                                """)

    # Introduction text creation
                                                                                                                                                                                                                                                                      
    import time  
    
    raw_input("Press Enter to continue...")
    print ("")
    introduction_text = ["Elves and Dwarves is a boardgame where each player has 5 elves and 3 dwarves.", 
                         "Each player can give orders to all his units turn per turn.",
                         "A unit can attack or move but never at the same turn.",
                         "A square can only be occupied by 1 unit at the same time.",
                         "A unit can't attack an allied unit.",
                         "Each unit has health points and can remove health points from an other unit.",
                         "A unit which has 0 health point is removed from de tray.",
                         "A unit can't move out of the board or on an occupied square.",
                         "A dwarf can only move one square straight ahead in all direction but not in diagonals.",
                         "A dwarf can only attack adjacent units (diagonals included).",
                         "An elf can move one square in all direction (diagonals included).",
                         "An elf can attack up to two squares around it (diagonals included).",
                         "The game end if a player has no more unit (victory for the other player).",
                         "If there is no attack during 20 turns, the player who has killed the most units wins.",
                         "In case of equality for the number of units, we calculated the total health points of each units to decide of the winner.",
                         "If it still has an equality, the player who starts to play looses the game."]
    for element in introduction_text:
        time.sleep(0.1)
        print (element )
        
        