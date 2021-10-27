""" This is a simplified BattleShip program made for Unamur bac1 programming lessons. """

#Imports

import os, pickle

#Functions

def game_creation(first_player,second_player):
	""" Create a new game file with players names.
	
	Parameters:
	-----------
	first_player : first player's pseudonyme or name (string)
	second_player : second player's pseudonyme or name (string)
	
	"""
	
	#Generation of a new (pickle) file.
	
	file = open("Battleship game.pkl",mode = "wb")
	
	#Generation of a blank battlefield for both players.
	
	grid_keys = [('A',0),('A',1),('A',2),('A',3),('A',4),('A',5),('A',6),('A',7),('A',8),('A',9),('A',10),
	('B',0),('B',1),('B',2),('B',3),('B',4),('B',5),('B',6),('B',7),('B',8),('B',9),('B',10),
	('C',0),('C',1),('C',2),('C',3),('C',4),('C',5),('C',6),('C',7),('C',8),('C',9),('C',10),
	('D',0),('D',1),('D',2),('D',3),('D',4),('D',5),('D',6),('D',7),('D',8),('D',9),('D',10),
	('E',0),('E',1),('E',2),('E',3),('E',4),('E',5),('E',6),('E',7),('E',8),('E',9),('E',10),
	('F',0),('F',1),('F',2),('F',3),('F',4),('F',5),('F',6),('F',7),('F',8),('F',9),('F',10),
	('G',0),('G',1),('G',2),('G',3),('G',4),('G',5),('G',6),('G',7),('G',8),('G',9),('G',10),
	('H',0),('H',1),('H',2),('H',3),('H',4),('H',5),('H',6),('H',7),('H',8),('H',9),('H',10),
	('I',0),('I',1),('I',2),('I',3),('I',4),('I',5),('I',6),('I',7),('I',8),('I',9),('I',10),
	('J',0),('J',1),('J',2),('J',3),('J',4),('J',5),('J',6),('J',7),('J',8),('J',9),('J',10)]
	
	grid_values= ['A','~','~','~','~','~','~','~','~','~','~',
	'B','~','~','~','~','~','~','~','~','~','~',
	'C','~','~','~','~','~','~','~','~','~','~',
	'D','~','~','~','~','~','~','~','~','~','~',
	'E','~','~','~','~','~','~','~','~','~','~',
	'F','~','~','~','~','~','~','~','~','~','~',
	'G','~','~','~','~','~','~','~','~','~','~',
	'H','~','~','~','~','~','~','~','~','~','~',
	'I','~','~','~','~','~','~','~','~','~','~',
	'J','~','~','~','~','~','~','~','~','~','~']
	
	
	game_data ={first_player:[[grid_keys,grid_values],[grid_keys,grid_values],[]],second_player:[[grid_keys,grid_values],[grid_keys,grid_values],[]],"players":(first_player,second_player),"turn":first_player}
	
	#File save.
	
	pickle.dump(game_data,file)
	file.close()
	
	#Prints.
	
	print "A new game file has been generated with the tag 'Battleship game'. Please send this file to the other player to play by mail.\nEnjoy your game!"
	
# ------------------------------------------------------------------------------------------------------------------------------------------------------------

def ship_creation(player,ship_coords):
	""" Add a new ship on the player's battlefield.

	Parameters:
	-----------
	player: player's name or pseudonyme (str)
	ship_coords: list of tuple of the ship coordinates (list(tuple))
	
	Raises: 
        ------
        ValueError: if the ship isn't in the grid.
	ValueError: if the ship isn't consistent.
	ValueError: if the ship is too close too an other ship.
	ValueError: if the ship already exists.
	ValueError: if there is already a ship on the location.
	
	Notes:
	------
	A ship has to have consistent serial coordinates.
	A ship cannot be next to an other ship (diagonals included).
	
	"""

	#File unpickling and extraction of usefull data.
	
	file = open('Battleship game.pkl', 'rb')
	game_data = pickle.load(file)
	
	player_keys = game_data[player][0][0]
	player_values = game_data[player][0][1]
	
	#Lexical sort of ship coordinates and ship tag.
	
	ship_coords = sorted(ship_coords)
	
	if len(ship_coords) == 2:
		ship_name = "destoyer"
	elif len(ship_coords) == 3:
		ship_name = "submarine"
	elif len(ship_coords) == 4:
		ship_name = "battleship"
	else:
		ship_name = "aircraft carrier"
	
	#Check ship consistency.
	
	for i,e in ship_coords:
		if not e in player_keys:
		#Verification of the existence of the coordinates.
			raise ValueError("The coordinates doesn't exists")
		elif 2 > len(ship_coords) < 5:
		#Verification of the ship size.
			raise ValueError("The ship is not at the right size")
		elif ship_name in game_data[player][2]:
		#Verification of the redundance in the creation.
			raise ValueError("The ", ship_name," already exists")
		elif player_keys.index(e) +1 != player_keys[ship_coords(i+1)] and i != len(ship_coords -1):
		#Verification of the ship coordinates consistency.
			raise ValueError("The ship is not consistent")
		elif player_values[player_keys.index(e)] == 'O':
		#Verification of the ship coordinates validity.
			raise ValueError("There is already a ship in coordinates \i .")
		elif i == 0 and (player_values[player_keys.index(e) -1] == "O" or player_values[player_keys.index(e) +1] == "O" or player_values[player_keys.index(e) -11] == "O" or player_values[player_keys.index(e) + 9] == "O"):
		#Verification of the front of the ship (diagonals included).
			raise ValueError("There is an other ship too close..")
		elif player_values[player_keys.index(e) +10] == "O" or player_values[player_keys.index(e) -10] == "O":
		#Verification of the sides of the ship.
			raise ValueError("There is an other ship too close..")
		elif i == (len(ship_coords)-1) and (player_values[player_keys.index(e) -1] == "O" or player_values[player_keys.index(e) -9] == "O" or player_values[player_keys.index(e) +11] == "O"):
		#Verification of the bottom of the ship (diagonals included).
			raise ValueError("There is an other ship too close...")
		
		#Changement of field state for each ship coordinates.
		
		player_values[player_keys.index(e)] = "O"
		
	#Adding the ship the player's army.
		
	game_data[player][2] += [(ship_name,[ship_coords])]
		
	#File save.
	
	game_data[player][0][1] = player_values
	pickle.dump(game_data,file)
	file.close()
	
	#Prints.
		
	print ("Your boat has been succesfully placed on the battlefield")
	
# ------------------------------------------------------------------------------------------------------------------------------------------------------------

def game_display(player):
	""" Display the battlefield according to the player's point of view.
	
	Parameters:
	-----------
	player: player's name or pseudonyme (str)
	
	"""
	
	#File unpickling.
	
	file = open('Battleship game.pkl', 'rb')
	game_data = pickle.load(file)
	
	#Prints.
	
	ennemy_data = game_data[player][1][1][99:110] + game_data[player][1][1][88:99] + game_data[player][1][1][77:88] + game_data[player][1][1][66:77] + game_data[player][1][1][55:66] + game_data[player][1][1][44:55] + game_data[player][1][1][33:44] + game_data[player][1][1][22:33] + game_data[player][1][1][11:22] + game_data[player][1][1][0:11]
	ennemy_display = ""
	player_display = ""
	
	for i in range(len(game_data[player][1][1])):
		if (i+1) % 11 != 0 and i != 109 :
			ennemy_display += ennemy_data[i] + " "
			player_display += game_data[player][0][1][i] + " "
		elif i == 109:
			ennemy_display += ennemy_data[i]
			player_display += game_data[player][0][1][i]
		else:			
			ennemy_display += ennemy_data[i] + " \n"
			player_display += game_data[player][0][1][i] + " \n"
	
	print ennemy_display
	print "  1 2 3 4 5 6 7 8 9"
	print player_display
	
	file.close()
	
# ------------------------------------------------------------------------------------------------------------------------------------------------------------

def shoot(player,position):
	""" Shoot on a position and print if something has been hit or if it's a miss.
	
	Parameters:
	-----------
	player: player's name or pseudonyme (str)
	position: the aimed spot (tuple)
	
	Raises:
	-------
	ValueError: if the position isn't on the grid.
	valueError: if it's not the player's turn.
	
	"""
	
	#File unpickling.
	
	file = open('Battleship game.pkl', 'rb')
	game_data = pickle.load(file)
	
	ennemy_keys = game_data[player][1][0]
	ennemy_values = game_data[player][1][1]
	
	if game_data[players].index(player) == 0:
		ennemy = game_data["players"][1]
		ennemy_grid = game_data[ennemy][0][1]
	else:
		ennemy = game_data["players"][0]
		ennemy_grid = game_data[ennemy][0][1]
	#Check to whom player is the turn
	
	if game_data["turn"] != player:
		raise ValueError("This is not your turn.")
		
	#Check the position validity
	
	if not position in game_data[player][0][0]:
		raise ValueError("This position is incorrect")
	elif ennemy_values[ennemy_keys.index(position)] == "X":
		raise ValueError("You already shot there.")
		
	#Data modifications and results.
	
	if ennemy_grid[ennemy_keys.index(position)] == "O":
		print ("Hit!")
		ennemy_values[ennemy_keys.index(position)] = "O"
		
		while i != "found":
			x = 0
			while i != "found" and x < len(game_data[ennemy][2][i][1]):
				if position == game_data[ennemy][2][i][1][x]:
					ship = game_data[ennemy][2][i][0]
					del game_data[ennemy][2][i][1][x]
					
					if game_data[ennemy][2][i][1] == "":
						print(ship," was sunk!")
						del game_data[ennemy][2][i]
						
						if game_data[ennemy][2] == "":
							print("Congratulation, you win!")
					i = "found"
				x += 1
			i += 1
	else:
		ennemy_values[ennemy_keys.index(position)] = "X"
		print ("Miss!")
	
	#Save
	
	game_data[player][1][1] = ennemy_values
	pickle.dump(game_data,file)
	file.close()
	
	
	
	
	