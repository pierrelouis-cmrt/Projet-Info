from math import *
from random import *
from copy import deepcopy
import time

## Code du jeu de carte Trio


# Création d'un jeu de cartes mélangé
def crea_jeu_carte():
    """
    Crée et mélange un jeu de cartes avec des valeurs de 1 à 12, 
    chaque valeur apparaissant 3 fois.
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
def action(dico, joueur):
    """
    Permet au joueur de révéler des cartes et attribue des points si un trio est trouvé.
    """
    carte1, dicotemporaire1 = choix(dico, joueur)
    if carte1 is None:
        print("Aucune carte n'a été révélée. Votre tour est terminé.")
        return 0, dico
    carte2, dicotemporaire2 = choix(dicotemporaire1, joueur)
    if carte2 is None:
        print("Aucune carte n'a été révélée. Votre tour est terminé.")
        return 0, dico
    if carte1 == carte2:
        carte3, dicotemporaire3 = choix(dicotemporaire2, joueur)
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
def choix(dico, joueur):
    """
    Offre au joueur des options pour révéler une carte au centre, 
    la plus grande ou la plus petite d'un joueur. Si le joueur n'est pas le joueur 1,
    les choix sont effectués aléatoirement par l'ordinateur.

    Si un choix impossible est fait, cela n'est pas compté comme un des choix du joueur,
    et le joueur est invité à choisir à nouveau.
    """
    actions_possibles = []
    if len(dico[0]) > 0:
        actions_possibles.append('c')
    joueurs_disponibles = [
        k for k in dico.keys() if k != 0 and len(dico[k]) > 0
    ]
    if joueurs_disponibles:
        actions_possibles.extend(['min', 'max'])

    if not actions_possibles:
        # Aucun choix possible
        print("Aucun choix possible pour le joueur", joueur)
        return None, dico

    while True:
        if joueur == 1:
            choix_act = input(
                'Saisissez "c" pour révéler une carte au centre, "max" pour révéler la carte la plus grande d\'un joueur, "min" pour révéler la carte la plus petite d\'un joueur : '
            )
            if choix_act not in actions_possibles:
                print(
                    "Choix invalide. Veuillez choisir une action valide parmi :",
                    actions_possibles)
                continue  # Choix invalide, on repropose au joueur son choix
        else:
            choix_act = choice(actions_possibles)
            print(f"Le joueur {joueur} choisit : {choix_act}")

        if choix_act == "c":
            if len(dico[0]) == 0:
                print("Il n'y a plus de cartes au centre.")
                continue  # Choix invalide, on repropose au joueur son choix
            else:
                print("Il reste au centre les cartes de position",
                      list(dico[0].keys()), ".")
                if joueur == 1:
                    try:
                        choix_carte_centre = int(
                            input(
                                "Saisissez le numéro de la carte que vous voulez révéler : "
                            ))
                    except ValueError:
                        print(
                            "Entrée invalide. Veuillez entrer un numéro de carte valide."
                        )
                        continue  # Choix invalide, on repropose au joueur son choix
                else:
                    choix_carte_centre = choice(list(dico[0].keys()))
                    print(
                        f"Le joueur {joueur} choisit de révéler la carte en position {choix_carte_centre}"
                    )
                if choix_carte_centre in dico[0]:
                    carte = dico[0][choix_carte_centre]
                    print("La carte retournée est : ", carte)
                    dicobis = deepcopy(dico)
                    del dicobis[0][choix_carte_centre]
                    break  # Choix valide fait, on sort de la boucle while
                else:
                    print(
                        "Position invalide. Veuillez choisir une carte valide."
                    )
                    continue  # Choix invalide, on repropose au joueur son choix

        elif choix_act == "min":
            if not joueurs_disponibles:
                print("Aucun joueur disponible pour cette action.")
                continue  # Choix invalide, on repropose au joueur son choix
            if joueur == 1:
                try:
                    choix_j = int(
                        input(
                            "Saisissez le numéro du joueur dont vous voulez révéler la carte : "
                        ))
                except ValueError:
                    print(
                        "Entrée invalide. Veuillez entrer un numéro de joueur valide."
                    )
                    continue  # Choix invalide, on repropose au joueur son choix
            else:
                choix_j = choice(joueurs_disponibles)
                print(
                    f"Le joueur {joueur} choisit de révéler la carte la plus petite du joueur {choix_j}"
                )
            if choix_j in dico and len(dico[choix_j]) > 0:
                carte = dico[choix_j][0]
                print(
                    f"La carte la plus petite du joueur {choix_j} est : {carte}"
                )
                dicobis = deepcopy(dico)
                del dicobis[choix_j][0]
                break  # Choix valide fait, on sort de la boucle while
            else:
                print("Le joueur", choix_j,
                      "n'a plus de cartes ou n'existe pas.")
                continue  # Choix invalide, on repropose au joueur son choix

        elif choix_act == "max":
            if not joueurs_disponibles:
                print("Aucun joueur disponible pour cette action.")
                continue  # Choix invalide, on repropose au joueur son choix
            if joueur == 1:
                try:
                    choix_j = int(
                        input(
                            "Saisissez le numéro du joueur dont vous voulez révéler la carte : "
                        ))
                except ValueError:
                    print(
                        "Entrée invalide. Veuillez entrer un numéro de joueur valide."
                    )
                    continue  # Invalid input, loop back
            else:
                choix_j = choice(joueurs_disponibles)
                print(
                    f"Le joueur {joueur} choisit de révéler la carte la plus grande du joueur {choix_j}"
                )
            if choix_j in dico and len(dico[choix_j]) > 0:
                carte = dico[choix_j][-1]
                print(
                    f"La carte la plus grande du joueur {choix_j} est : {carte}"
                )
                dicobis = deepcopy(dico)
                del dicobis[choix_j][-1]
                break  # Choix valide fait, on sort de la boucle while
            else:
                print("Le joueur", choix_j,
                      "n'a plus de cartes ou n'existe pas.")
                continue  # Choix invalide, on repropose au joueur son choix

        else:
            print("Choix invalide. Veuillez choisir une action valide parmi :",
                  actions_possibles)
            continue  # Choix invalide, on repropose au joueur son choix

    return carte, dicobis


# Initialise le jeu en demandant le nombre de joueurs et en distribuant les cartes
def start():
    """
    Initialise le jeu en configurant le nombre de joueurs et en distribuant les cartes.
    """
    while True:
        try:
            nombre_joueurs = int(input("Combien de joueurs ? (3, 4, 5 ou 6) "))
            if nombre_joueurs in [3, 4, 5, 6]:
                break
            else:
                print(
                    "Nombre de joueurs incorrect. Veuillez saisir 3, 4, 5 ou 6."
                )
        except ValueError:
            print("Entrée invalide. Veuillez entrer un nombre entier.")
    cartes = crea_jeu_carte()
    if nombre_joueurs == 3:
        dico = repar_cartes(3, 9, cartes)
    elif nombre_joueurs == 4:
        dico = repar_cartes(4, 7, cartes)
    elif nombre_joueurs == 5:
        dico = repar_cartes(5, 6, cartes)
    elif nombre_joueurs == 6:
        dico = repar_cartes(6, 5, cartes)
    return dico, nombre_joueurs


# Fonction principale qui gère le déroulement du jeu
def codecentral():
    """
    Exécute la boucle principale du jeu jusqu'à ce qu'un joueur gagne.
    """
    dico, nbjoueurs = start()
    points = [0 for _ in range(nbjoueurs)]
    vmax = 0
    tour = 1
    while vmax < 3:
        joueur = autourde(nbjoueurs, tour)
        print("\n" * 2)
        print("Cartes disponibles au centre : ", list(dico[0].keys()))
        print("Scores actuels : ", points)
        print("\n")
        print("C'est au joueur", joueur, "de jouer.")
        if joueur != 1:
            print("Ce joueur est géré par l'ordinateur.")
        if len(dico[joueur]) == 0 and joueur == 1:
            print("Vous n'avez plus de cartes.")
        elif joueur == 1:
            print("Vos cartes sont : ", dico[joueur])
        print("\n")
        points_gagnes, dico = action(dico, joueur)
        if joueur <= len(points):
            points[joueur - 1] += points_gagnes
        vmax, imax = maximum(points)
        tour += 1
        if tour == nbjoueurs + 1:
            print(
                "-----------------------------------------------------------------------------"
            )
        time.sleep(3)
    print("\n")
    print("Le joueur", imax + 1, "est le gagnant !")


# Démarrage du jeu
codecentral()
