import math
import random

# Définition des valeurs des JOUEURs (le JOUEUR et l'ORDINATEUR )
JOUEUR = -1
ORDINATEUR  = 1


# Cette fonction affiche le tableau de jeu sur la console
# Input: un tableau  de 3x3 avec des éléments JOUEUR, ORDINATEUR  ou vide
# Output: N/A
def print_board(board):
    print("-------------")
    # Pour chaque ligne dans le tableau
    for row in board:
        print("|", end=" ")
        # Pour chaque colonne dans la ligne
        for col in row:
            # Si la colonne contient le marqueur JOUEUR, afficher X
            if (col == JOUEUR):
                print("X", end=" | ")
            # Sinon, si la colonne contient le marqueur ORDINATEUR , afficher O
            elif col == ORDINATEUR :
                print("O", end=" | ")
            # Sinon, la colonne est vide, afficher un espace vide
            else:
                print(" ", end=" | ")
        # Aller à la ligne et afficher une ligne de séparation
        print("\n-------------")



###########################################################################################################################
# Cette fonction évalue le tableau de jeu pour déterminer s'il y a un gagnant

# Input: un tableau de 3x3 avec des éléments JOUEUR, ORDINATEUR  ou vide
# Output: 1 si l'ORDINATEUR gagne, -1 si le JOUEUR gagne, 0 s'il n'y a pas de gagnant


def evaluate(board):
    # On définit toutes les configurations gagnantes possibles
    winning_configs = [        [board[0][0], board[0][1], board[0][2]],  # première rangée
        [board[1][0], board[1][1], board[1][2]],  # deuxième rangée
        [board[2][0], board[2][1], board[2][2]],  # troisième rangée
        [board[0][0], board[1][0], board[2][0]],  # première colonne
        [board[0][1], board[1][1], board[2][1]],  # deuxième colonne
        [board[0][2], board[1][2], board[2][2]],  # troisième colonne
        [board[0][0], board[1][1], board[2][2]],  # diagonale 
        [board[0][2], board[1][1], board[2][0]]   # antidiagonale
    ]

    # parcourir toutes les configurations gagnantes possibles
    for config in winning_configs:

        # Si l'ORDINATEUR a gagné, renvoyer 1
        if all(cell == ORDINATEUR  for cell in config):
            return 1

        # Sinon, si le JOUEUR a gagné, renvoyer -1
        elif all(cell == JOUEUR for cell in config):
            return -1

    # Si aucun JOUEUR n'a gagné, renvoyer 0
    return 0


###############################################################################################################################
# Fonction qui vérifie si le plateau est rempli


# Input: un tableau de 3x3 avec des éléments JOUEUR, ORDINATEUR  ou vide
# Output: True si le plateau est rempli, False sinon


def full(board):
    for row in board:
        for col in row:
            if col == 0:
                return False
    return True

###############################################################################################################################
# Fonction qui renvoie tous les coups possibles


# Input: un tableau de 3x3 avec des éléments JOUEUR, ORDINATEUR  ou vide
# Output: une liste de tuples contenant les indices des cases vides sur le tableau


def get_possible_moves(board):
    moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0: 
                moves.append((i, j))
    return moves

###############################################################################################################################
# Fonction pour créer un nouveau tableau de jeu vide
# Output: un tableau de 3x3 rempli de zéros


def create_board():
  return [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

##############################################################################################################################
# Fonction qui vérifie si le jeu est terminé


# Input: un tableau de 3x3 avec des éléments JOUEUR, ORDINATEUR  ou vide
# Output: True si le jeu est terminé (gagné ou plateau rempli), False sinon

def game_over(board):
  return evaluate(board) != 0 or full(board)


#########################################################################################################################
  # Fonction pour demander au JOUEUR de choisir une case vide


# Input: un tableau de 3x3 avec des éléments JOUEUR, ORDINATEUR  ou vide
# Output: un tuple contenant les indices de la case choisie par le JOUEUR


def get_player_move(board):
  while True:
    row = int(input("Choisissez une ligne (0, 1 ou 2) : "))
    col = int(input("Choisissez une colonne (0, 1 ou 2) : "))
    if board[row][col] == 0: # si elle n'est pas deja prise 
      return (row, col)
    else:
      print("Cette case est déjà occupée. Choisissez une autre case.")

##########################################################################################################################


# Fonction qui effectue un mouvement sur le tableau


# Input: un tableau de 3x3 avec des éléments JOUEUR, ORDINATEUR  ou vide, un tuple contenant les indices de la case choisie et un JOUEUR (JOUEUR ou ORDINATEUR )
# Output: un nouveau tableau avec le mouvement effectué


def make_move(board, move, player):
  new_board = [row[:] for row in board]
  row, col = move
  if player == 'X':
    new_board[row][col] = ORDINATEUR 
  else:
    new_board[row][col] = JOUEUR
  return new_board

########################################################################################################################
# Fonction qui renvoie le résultat du jeu


# Input: un tableau de 3x3 avec des éléments JOUEUR, ORDINATEUR  ou vide
# Output: une chaîne de caractères qui indique le résultat du jeu (ORDINATEUR gagnant, JOUEUR gagnant ou match nul)

def get_game_result(board):
  if evaluate(board) == 1:
    return "L'ORDINATEUR a gagné !"
  elif evaluate(board) == -1:
    return "Vous avez gagné !"
  else:
    return "Match nul !" 


#######################################################################################################################

def minimax(board, depth, maximizing_player, alpha, beta):

    # l'algorithme Minimax avec élagage Alpha-Beta ( défini dans le rapport)
    
    # Si le jeu est terminé ou si le plateau est plein, retourne l'évaluation du plateau
    if full(board) or game_over(board):
        return evaluate(board)

    if maximizing_player:
        # Si le JOUEUR est en train de maximiser, initialise max_eval à moins l'infini
        max_eval = float('-inf')

        # Pour chaque coup possible, effectue le coup et appelle la fonction minimax d'une maniere recursive avec le nouveau plateau

        for move in get_possible_moves(board):
            new_board = make_move(board, move, 'X')
            evaluation = minimax(new_board, depth+1, False, alpha, beta) # évaluation du plateau pour le JOUEUR minimisant
            max_eval = max(max_eval, evaluation) # Met à jour max_eval avec la valeur la plus grande trouvée
            alpha = max(alpha, max_eval) # Met à jour alpha avec la valeur max_eval si elle est plus grande que la valeur actuelle d'alpha
            if beta <= alpha:
                # Si beta est inférieur ou égal à alpha, il n'y a pas besoin d'explorer plus en profondeur
                break

        return max_eval # Retourne la meilleure évaluation trouvée

    else:
        # Si le JOUEUR est en train de minimiser, initialiser min_eval à l'infini
        min_eval = float('inf')
        # Pour chaque cas possible, effectue le coup et appelle la fonction minimax récursivement avec le nouveau plateau
        for move in get_possible_moves(board):
            new_board = make_move(board, move, 'O')
            evaluation = minimax(new_board, depth+1, True, alpha, beta) # évaluation du plateau pour le JOUEUR maximisant
            min_eval = min(min_eval, evaluation) # Met à jour min_eval avec la valeur la plus petite trouvée
            beta = min(beta, min_eval) # Met à jour beta avec la valeur min_eval si elle est plus petite que la valeur actuelle de beta
            if beta <= alpha:
                # Si beta est inférieur ou égal à alpha, il n'y a pas besoin d'explorer plus en profondeur
                break
        return min_eval # Retourne la meilleure évaluation trouvée



#######################################################################################################################

def get_ORDINATEUR_move(board): 

    #Retourne le meilleur coup pour l'ORDINATEUR en utilisant l'algorithme Minimax avec élagage Alpha-Beta

    best_move = None # Initialise le meilleur coup à None
    max_eval = float('-inf') # Initialise la meilleure évaluation à moins l'infini
    alpha = float('-inf') # Initialise alpha à moins l'infini
    beta = float('inf') # Initialise beta à l'infini

    # Pour chaque coup possible, effectue le coup et évalue le plateau en appelant la fonction minimax avec le nouveau plateau
    for move in get_possible_moves(board):
        new_board = make_move(board, move, 'X')
        evaluation = minimax(new_board, 0, False, alpha, beta) # évaluation du plateau pour le JOUEUR minimisant
        if evaluation > max_eval:
            # Si l'évaluation actuelle est supérieure à la meilleure évaluation trouvée jusqu'à présent, met à jour la meilleure évaluation et le meilleur coup
            max_eval = evaluation
            best_move = move
        alpha = max(alpha, evaluation) # Met à jour alpha avec l'évaluation actuelle si elle est plus grande que la valeur actuelle d'alpha
    return best_move # Retourne le meilleur coup trouvé


# Initialise la variable de jeu pour continuer à jouer jusqu'à ce que le JOUEUR décide d'arrêter
play_again = "oui"

##########################################################################################################################

# Boucle principale pour jouer plusieurs parties


while play_again == "oui":
    # Initialise un nouveau plateau de jeu
    board = create_board()
    # Affiche le plateau de jeu initial
    print_board(board) 
    # Accueille les JOUEURs
    print("Bienvenue au jeu Tic Tac Toe !")
    player1 = input("Nom du JOUEUR 1 : ")

    # Boucle pour jouer une partie complète
    while not game_over(board):
        # Le JOUEUR humain joue
        player_move = get_player_move(board)
        board = make_move(board, player_move, 'O') # Met à jour le plateau avec le coup du JOUEUR humain
        print_board(board) # Affiche le plateau après que le JOUEUR humain ait joué

        # Vérifie si le jeu est terminé avant de laisser l'ORDINATEUR jouer
        if not game_over(board):
            # L'ORDINATEUR joue
            ORDINATEUR_move = get_ORDINATEUR_move(board)
            board = make_move(board, ORDINATEUR_move, 'X') # Met à jour le plateau avec le coup de l'ORDINATEUR
            print_board(board) # Affiche le plateau après que l'ORDINATEUR ait joué





    # Affiche le résultat de la partie
    result = get_game_result(board)
    print(result)







    # Demande si le JOUEUR souhaite jouer une autre partie
    play_again = input("Voulez-vous jouer une autre partie ? (Oui/Non)").lower()








# Affiche un message de fin une fois que le JOUEUR a terminé de jouer
print("Merci d'avoir joué !")