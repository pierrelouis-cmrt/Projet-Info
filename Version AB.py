from math import *
from random import *
from copy import deepcopy

## Code du jeu de carte Trio


# Création d'un jeu de cartes mélangé
def crea_jeu_carte():
    """
    Crée et mélange un jeu de cartes avec des valeurs de 1 à 12, chaque valeur apparaissant 3 fois.
    """
    ensemble_jeu = []
    for i in range(1, 13):
        for j in range(3):
            ensemble_jeu.append(i)
    shuffle(ensemble_jeu)
    return ensemble_jeu


# Distribution des cartes aux joueurs et au centre
def repar_cartes(nbj, nbcartes, ensemble_jeu):
    """
    Distribue un nombre spécifique de cartes à chaque joueur et place le reste au centre.
    """
    dico = {}
    for i in range(1, nbj + 1):
        joueuri_list = []
        for j in range(nbcartes):
            joueuri_list.append(ensemble_jeu.pop(0))
        joueuri_list.sort()
        dico[i] = joueuri_list
    dico[0] = dict(zip([k for k in range(len(ensemble_jeu))], ensemble_jeu))
    return dico


# Trouve la valeur maximale et son index dans une liste
def maximum(liste):
    """
    Retourne la valeur maximale d'une liste et son index.
    """
    vmax = liste[0]
    imax = 0
    for i in range(len(liste)):
        if liste[i] >= vmax:
            vmax = liste[i]
            imax = i
    return vmax, imax


# Détermine quel joueur joue lors d'un tour donné
def autourde(nbjoueurs, tour):
    """
    Identifie le joueur actif en fonction du numéro de tour. 
    Utilise un modulo pour éviter 50 répétitions.
    """
    joueur = ((tour - 1) % nbjoueurs) + 1
    return joueur


# Gère les actions d'un tour complet d'un joueur
def action(dico):
    """
    Permet au joueur de révéler des cartes et attribue des points si un trio est trouvé.
    """
    carte1, dicotemporaire1 = choix(dico)
    if carte1 is None:
        print("Aucune carte n'a été révélée. Votre tour est terminé.")
        return 0, dico
    carte2, dicotemporaire2 = choix(dicotemporaire1)
    if carte2 is None:
        print("Aucune carte n'a été révélée. Votre tour est terminé.")
        return 0, dico
    if carte1 == carte2:
        carte3, dicotemporaire3 = choix(dicotemporaire2)
        if carte3 is None:
            print("Aucune carte n'a été révélée. Votre tour est terminé.")
            return 0, dico
        if carte3 == carte1:
            if carte1 == 7:
                print(
                    "Vous avez trouvé le trio de 7, vous avez gagné la partie ! Bravo !"
                )
                return 7, dicotemporaire3
            else:
                print("Trio gagnant! Vous gagnez un point")
                print("Votre tour est fini.")
                return 1, dicotemporaire3
    print("Votre tour est fini")
    return 0, dico


# Permet au joueur de choisir une action durant son tour
def choix(dico):
    """
    Offre au joueur des options pour révéler une carte au centre, 
    la plus grande ou la plus petite d'un joueur.
    """
    choix_act = input(
        'Saisissez "c" pour révéler une carte au centre, "max" pour révéler la carte la plus grande d\'un joueur, "min" pour révéler la carte la plus petite d\'un joueur : '
    )
    if choix_act == "c":
        if len(dico[0]) == 0:
            print("Il n'y a plus de cartes au centre.")
            carte = None
            dicobis = dico
        else:
            print("Il reste au centre les cartes de position",
                  list(dico[0].keys()), ".")
            choix_carte_centre = int(
                input(
                    "Saisissez le numéro de la carte que vous voulez révéler : "
                ))
            if choix_carte_centre in dico[0]:
                carte = dico[0][choix_carte_centre]
                print("La carte retournée est : ", carte)
                dicobis = deepcopy(dico)
                del dicobis[0][choix_carte_centre]
            else:
                print("Position invalide. Aucune carte révélée.")
                carte = None
                dicobis = dico

    elif choix_act == "min":
        choix_j = int(
            input(
                "Saisissez le numéro du joueur dont vous voulez révéler la carte : "
            ))
        if choix_j in dico and len(dico[choix_j]) > 0:
            carte = dico[choix_j][0]
            print("La carte la plus petite du joueur est : ", carte)
            dicobis = deepcopy(dico)
            del dicobis[choix_j][0]
        else:
            print("Le joueur", choix_j, "n'a plus de cartes ou n'existe pas.")
            carte = None
            dicobis = dico

    elif choix_act == "max":
        choix_j = int(
            input(
                "Saisissez le numéro du joueur dont vous voulez révéler la carte : "
            ))
        if choix_j in dico and len(dico[choix_j]) > 0:
            carte = dico[choix_j][-1]
            print("La carte la plus grande du joueur est : ", carte)
            dicobis = deepcopy(dico)
            del dicobis[choix_j][-1]
        else:
            print("Le joueur", choix_j, "n'a plus de cartes ou n'existe pas.")
            carte = None
            dicobis = dico

    else:
        print("Choix invalide. Aucune carte révélée.")
        carte = None
        dicobis = dico

    return carte, dicobis


# Initialise le jeu en demandant le nombre de joueurs et en distribuant les cartes
def start():
    """
    Initialise le jeu en configurant le nombre de joueurs et en distribuant les cartes.
    """
    nombre_joueurs = int(input("Combien de joueurs ? (3, 4, 5 ou 6) "))
    cartes = crea_jeu_carte()
    if nombre_joueurs == 3:
        dico = repar_cartes(3, 9, cartes)
    elif nombre_joueurs == 4:
        dico = repar_cartes(4, 7, cartes)
    elif nombre_joueurs == 5:
        dico = repar_cartes(5, 6, cartes)
    elif nombre_joueurs == 6:
        dico = repar_cartes(6, 5, cartes)
    else:
        print("Nombre de joueurs incorrect")
        dico = {}
    return dico, nombre_joueurs


# Fonction principale qui gère le déroulement du jeu
def codecentral():
    """
    Exécute la boucle principale du jeu jusqu'à ce qu'un joueur gagne.
    """
    dico, nbjoueurs = start()
    point = [0 for _ in range(nbjoueurs)]
    vmax = 0
    tour = 1
    while vmax < 3:
        joueur = autourde(nbjoueurs, tour)
        print("\n" * 2)
        print("Cartes disponibles au centre : ", list(dico[0].keys()))
        print("Scores actuels : ", point)
        print("\n")
        print("C'est au joueur", joueur, "de jouer.")
        if len(dico[joueur]) == 0:
            print("Vous n'avez plus de cartes.")
        else:
            print("Vos cartes sont : ", dico[joueur])
        print("\n")
        pt, dico = action(dico)
        if joueur <= len(point):
            point[joueur - 1] += pt
        vmax, imax = maximum(point)
        tour += 1
    print("\n")
    print("Le joueur", imax + 1, "est le gagnant !")


# Démarrage du jeu
codecentral()
