#!/usr/bin/python3
import socket
import select
import threading
import random
import sys
from grid import *

PORT = 2017

def serveur():
    connexionServeur = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)

    connexionServeur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connexionServeur.bind(('', 2017))

    connexionServeur.listen(1) # pour indiquer au systeme qu on va accepter des rlist

    listConnexions = [connexionServeur] # Liste contenant que la socket serveur

    JOUEUR1 = "1"
    JOUEUR2 = "2"
    SPECTATEUR = "0"

    while 1:
        rlist, _, _ = select.select(listConnexions, [], [])
        for connexion in rlist:
            if connexion == connexionServeur: # Si c est la socket d ecoute
                (connexionJoueur, infoJoueur) = connexionServeur.accept() # Accepter une connexion entrante
                listConnexions.append(connexionJoueur) # Ajout du nouveau joueur dans la liste
                
                if(len(listConnexions) == 2): # Si le premier joueur s'est connecté
                    print("Le joueur 1 ("+str(infoJoueur)+") vient de se connecter")
                    connexionJoueur.send(JOUEUR1.encode()) # Notifier de la connexion du joueur 

                elif(len(listConnexions) == 3): # Si un second joueur s'est connecté
                    print("Le joueur 2 ("+str(infoJoueur)+") vient de se connecter")
                    connexionJoueur.send(JOUEUR2.encode()) # Notifier de la connexion du joueur 

                else: # Si un spectateur s'est connecté
                    print("Un spectateur ("+str(infoJoueur)+") vient de se connecter")
                    connexionJoueur.send(SPECTATEUR.encode()) # Notifier de la connexion du spectateur

            else: # Un joueur nous a envoye le numéro de la case où il joue
                try:
                    shot = connexion.recv(1500).decode() # Pour receptionner des donnees
                except ConnectionError:
                    print("Erreur de connexion !")

                if len(shot.strip()) == 0: # Si un joueur a envoyé un message vide ou des espaces
                    info = infoJoueur
                    listConnexions.remove(connexion) # Supprimer le joueur de la liste
                    if (len(listConnexions)-1) == 1: # s'il reste un joueur
                        print("Le joueur "+str(info)+" s'est déconnecté !")
                        listConnexions[1].send("ADVERSAIRE_DECONNECTE".encode()) # Informer le joueur restant de la déconnexion de son adversaire

                    if (len(listConnexions)-1) >= 2: # s'il reste toujours deux joueurs
                        print("Le spectateur "+str(info)+" est parti !")

                    connexion.close() # Fermer la socket
                else:
                    # Envoyer le message à tous ceux qui se sont connectés sauf le serveur et l'expéditeur
                    for i in range(len(listConnexions)):
                        if listConnexions[i] != connexionServeur and listConnexions[i] != connexion:
                            listConnexions[i].send(shot.encode())

                    #End_for
                #End_if
            #End_if
        #End_for
    #End_while

    connexionServeur.close()


def client(hote):
    connexionClient = socket.socket(socket.AF_INET6,socket.SOCK_STREAM,proto=0)
    connexionClient.connect((hote, PORT))
    grids = [grid(), grid()]
    joueur = ""
    rcvspect = ""
    i = 0
    s1 = s2 = null = 0
    joueur = connexionClient.recv(1024).decode()

    if(int(joueur) != J1 and int(joueur) != J2): # S'il s'agit d'un spectateur
        print("Vous êtes un spectateur")
        grids[0].display() # Afficher la grille complète

    if int(joueur) == J1: # S'il s'agit du premier joueur
        print("Attente d'un Adversaire...")
        data = connexionClient.recv(1024).decode() # Atente de réception du coup du deuxième joueur
        grids[0].play(J2, int(data)) # Le deuxième joueur joue

    # if int(joueur) != 0:  
    grids[1].display() # Affichage de la grille pour le joueur

    while True:     
        if(joueur != "ADVERSAIRE_DECONNECTE"):
            while grids[0].gameOver() == -1:
                shot = -1
                if(int(joueur) != 0):
                    while shot < 0 or shot >= NB_CELLS:
                        while shot < 0 or shot >= NB_CELLS:
                            shot = int(input ("Quelle case allez-vous jouer ? "))

                        if (grids[0].cells[shot] != EMPTY): # si la case n'est pas vide
                            print("Case déjà prise %d" %shot)
                            grids[1].cells[shot] = grids[0].cells[shot] # On recopie la valeur qui y était
                            grids[1].display() # Affichage à nouveau de la carte
                            shot = -1
                        else: # Si la case est vide 
                            grids[0].play(J1, shot)
                            grids[1].play(J1, shot)
                            grids[1].display()

                    # Fin de jeu chez le premier joueur
                    connexionClient.send(str(shot).encode()) # Envoi au serveur la case choisie
                    if grids[0].gameOver() != -1:
                        print("Game over")
                        grids[0].display()
                        if grids[0].gameOver() == 1:
                            print("Bravo, vous avez gagné !")
                            break
                        elif grids[0].gameOver() == 2:
                            print("vous avez perdu !")
                            break   
                        else:
                            print("Match nul !")
                            break

                    # Fin de jeu cvhez le second joueur
                    shot = connexionClient.recv(1024).decode()      
                    grids[0].play(J2, int(shot))
                    if grids[0].gameOver() != -1:
                        print("Game over")
                        grids[0].display()
                        if grids[0].gameOver() == 1:
                            print("vous avez perdu !")
                            break
                        elif grids[0].gameOver() == 2:
                            print("vous avez perdu !")
                            break       
                        else:
                            print("Match nul !")
                            break   
                else:
                    # Affichage des coups joués par les joueurs cez le spectateur
                    rcvspect = connexionClient.recv(1024).decode()
                    r = int(rcvspect)
                    if(r >= 0 and r < 9):
                        if(i % 2 == 0):
                            i += 1
                            grids[0].play(1, int(rcvspect))
                            grids[0].display()
                        else:
                            grids[0].play(2, int(rcvspect))
                            grids[0].display()
                            i += 1  


                    # Fin de jeu chez le spectateur
                    if grids[0].gameOver() != -1:
                        print("Game over")
                        grids[0].display()
                        if grids[0].gameOver() == 1:
                            s1 += 1
                            print("Le joueur 2 a gagné la partie !")
                            break
                        elif grids[0].gameOver() == 2:
                            s2 += 1
                            print("Le Joueur 1 a gagné la partie !!")
                            null += 1
                            break   
                        else:
                            print("Match nul !")
                            break                                       
        else:   
            print("Adversaire deconnecte,vous avez gagne")
            break
        
    print("Partie terminée")
                        
        
    connexionClient.close()



def main():

    grids = [grid(), grid(), grid()] # Un tableau de trois grilles
    if(len(sys.argv) == 1):
        serveur()
    elif(len(sys.argv) == 2):
        client(sys.argv[1])
    else:
        print("Usage: "+argv[0]+" [hote]")
        sys.exit()


    

main()
