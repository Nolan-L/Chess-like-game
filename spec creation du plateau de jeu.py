def play(game_size):
    """ Fonction wich ables you to play the game at the size you want.
    
    Parameters:
    -----------
    game_size: the size of the game (string)
    
    Raises: 
    -------
    ValueError: if a game already exist.
    ValueError: the size of the game must be between 7x7 and 20x20.
    
    Returns:
    --------
    game_size: the size of the game (string)
    """
    try:
        return play(game_size)
    except ValueError:
        print ("sorry a game already exist you can't create another one")