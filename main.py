#!/usr/bin/python3

from grid import *
import  random

def main():
    grids = [grid(), grid(), grid()] # Un tableau de trois grilles
    current_player = J1
    grids[J1].display() #Affichage de la grille du joueur J1
    while grids[0].gameOver() == -1: # Tant que le jeu n'est pas terminé
        if current_player == J1: # Si le joueur actuel est J1
            shot = -1 # On initialise shot à -1
            while shot < 0 or shot >= NB_CELLS: # Tant que shot n'est pas compris entre 0 et NB_CELLS compris, demander au joueur la case qu'il veut jouer
                shot = int(input ("quel case allez-vous jouer ?"))
        else: # SI c'est à la machine de jouer
            shot = random.randint(0,8) # 
            while grids[current_player].cells[shot] != EMPTY: # Tant que la case où on doit jouer n'est pas vide, on choisit une autre case
                shot = random.randint(0,8)

        if (grids[0].cells[shot] != EMPTY): # Si la case n'était pas vide
            grids[current_player].cells[shot] = grids[0].cells[shot] # On recopie la valeur qui y était
        else:
            grids[current_player].cells[shot] = current_player
            grids[0].play(current_player, shot)
            current_player = current_player%2+1 # Pour donner la main à l'autre joueur

        if current_player == J1:
            grids[J1].display()
    #while End
    print("game over")
    grids[0].display()
    if grids[0].gameOver() == J1:
        print("You win !")
    else:
        print("you loose !")

main()
