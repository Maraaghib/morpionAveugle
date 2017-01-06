import socket
import select
import threading
import sys
from grid import *

connexionServeur = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)

connexionServeur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
connexionServeur.bind(('', 2017))

connexionServeur.listen(1) # pour indiquer au systeme qu on va accepter des rlist

listConnexions = [connexionServeur] # Liste contenant que la socket serveur

JOUEUR1 = "Joueur1"
JOUEUR2 = "Joueur2"
SPECTATEUR = "Spectateur"

while 1:
	rlist, _, _ = select.select(listConnexions, [], [])
	for connexion in rlist:
		if connexion == connexionServeur: # Si c est la socket d ecoute
			(connexionJoueur, infoJoueur) = connexionServeur.accept() # Accepter une connexion entrante
			listConnexions.append(connexionJoueur) # Ajout du nouveau joueur dans la liste
			print("Le joueur "+str(infoJoueur)+" vient de se connecter")

			if(len(listConnexions) == 2): # Si le premier joueur s'est connecté
				connexionJoueur.send(JOUEUR1.encode()) # Notifier de la connexion du joueur 

			elif(len(listConnexions) == 3): # Si usecond joueur s'est connecté
				connexionJoueur.send(JOUEUR2.encode()) # Notifier de la connexion du joueur 

			else: # Si un spectateur s'est connecté
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
					listConnexions[1].send("ADV_DECONNECTED".encode()) # Informer le joueur restant de la déconnexion de son adversaire

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

