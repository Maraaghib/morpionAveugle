from grid import *

import socket 
import select 
import threading

PORT = 2017

"""
Le socket du client est crée et la connexion au serveur est établie.
Le protocole textuel doit encore être crée, et géré dans une boucle infinie.
"""

def start(addresse):
	so = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
	so.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	so.connect((addresse, PORT))
	grid = grid()
	
	#while 1:
	
	
"""
Attend que l'utilisateur tape une commande pour l'envoyer au serveur
"""

def command(socket):
	cmd = input()
	if not cmd.strip():
		print("Veuillez entrer une commande")
	socket.send(bytearray(cmd, "utf-8")
	
#def exec(): Fonction qui gèrera les messages reçus du serveur pour afficher en conséquence du texte ou l'état de la grille