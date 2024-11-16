# -*- coding: utf-8 -*-
import random
from copy import deepcopy
import time  # utiliser ici pour ajouter du délai pour une meilleure lisibilité
from termcolor import colored  # print en couleur dans la console

## Code du jeu de cartes Trio

# Mémoire des cartes révélées
cartes_revelees = {
}  # Dictionnaire avec position comme clé et valeur de la carte


# Création d'un jeu de cartes mélangé
def creer_jeu_cartes():
    """
    Crée et mélange un jeu de cartes avec des valeurs de 1 à 12,
    chaque valeur apparaissant 3 fois.

    Returns:
        list: Un jeu de 36 cartes mélangées.
    """
    ensemble_jeu = []
    for i in range(1, 13):
        for j in range(3):
            ensemble_jeu.append(i)
    random.shuffle(ensemble_jeu)
    return ensemble_jeu


# Distribution des cartes aux joueurs et au centre
def repartir_cartes(nbj, nbcartes, ensemble_jeu):
    """
    Distribue un nombre spécifique de cartes à chaque joueur et place le reste au centre.

    Args:
        nbj (int): Nombre de joueurs.
        nbcartes (int): Nombre de cartes à distribuer à chaque joueur.
        ensemble_jeu (list): Le jeu de cartes mélangé.

    Returns:
        dict: Un dictionnaire contenant les mains des joueurs et les cartes du centre.
    """
    dico = {}
    for i in range(1, nbj + 1):
        main_joueur_i = []
        for j in range(nbcartes):
            main_joueur_i.append(ensemble_jeu.pop(0))
        main_joueur_i.sort()
        dico[i] = main_joueur_i
    # Les cartes restantes sont mises au centre, indexées par leur position
    dico[0] = dict(zip([k for k in range(len(ensemble_jeu))], ensemble_jeu))
    return dico


# Trouve la valeur maximale et son index dans une liste
def maximum(liste):
    """
    Retourne la valeur maximale d'une liste et son index.

    Args:
        liste (list): Liste de valeurs numériques.

    Returns:
        tuple: Valeur maximale et son index.
    """
    vmax = liste[0]
    imax = 0
    for i in range(len(liste)):
        if liste[i] >= vmax:
            vmax = liste[i]
            imax = i
    return vmax, imax


# Détermine quel joueur joue lors d'un tour donné
def autour_de(nbjoueurs, tour):
    """
    Identifie le joueur actif en fonction du numéro de tour.

    Args:
        nbjoueurs (int): Nombre total de joueurs.
        tour (int): Numéro du tour actuel.

    Returns:
        int: Numéro du joueur qui doit jouer.
    """
    joueur = ((tour - 1) % nbjoueurs) + 1
    return joueur


# Fonction pour déterminer la carte cible de l'IA
def carte_cible(dico, joueur):
    """
    Détermine la carte cible que l'IA va essayer de compléter en trio.

    Args:
        dico (dict): Dictionnaire des mains des joueurs et des cartes du centre.
        joueur (int): Numéro du joueur IA.

    Returns:
        int: La valeur de la carte cible.
    """
    # Obtenir les cartes du joueur
    main_joueur = dico[joueur]

    # Cartes accessibles (révélées au centre ou comme min/max des joueurs)
    cartes_accessibles = []

    # Cartes révélées au centre
    for position, carte in cartes_revelees.items():
        if position[0] == 'centre':
            cartes_accessibles.append(carte)
        elif position[0] == 'joueur':
            # Ajouter toutes les cartes révélées des joueurs
            cartes_accessibles.append(carte)

    # Si aucune carte accessible, choisir aléatoirement entre sa propre carte min ou max
    if not cartes_accessibles:
        min_card = main_joueur[0]
        max_card = main_joueur[-1]
        carte_cible = random.choice([min_card, max_card])
        return carte_cible

    # Choisir une carte cible aléatoire parmi les cartes accessibles
    carte_cible = random.choice(cartes_accessibles)
    return carte_cible


# Gère les actions d'un tour complet d'un joueur
def action(dico, joueur):
    """
    Permet au joueur de révéler des cartes et attribue des points si un trio est trouvé.

    Args:
        dico (dict): Dictionnaire des mains des joueurs et des cartes du centre.
        joueur (int): Numéro du joueur actuel.

    Returns:
        tuple: Points gagnés lors du tour et le dictionnaire mis à jour.
    """
    global cartes_revelees
    cartes_revelees_tour = []  # Cartes révélées lors de ce tour
    positions_revelees_tour = [
    ]  # Positions des cartes révélées lors de ce tour

    # Pour les joueurs IA, déterminer la carte cible initiale
    carte_cible_ia = None
    if joueur != 1:
        carte_cible_ia = carte_cible(dico, joueur)
        print(
            f"Le joueur {joueur} cherche à compléter le trio de {carte_cible_ia}"
        )

    carte1, dico_temporaire1, position1 = choix(dico, joueur, carte_cible_ia,
                                                positions_revelees_tour)
    if carte1 is None:
        print("Aucune carte n'a été révélée. Votre tour est terminé.")
        return 0, dico
    cartes_revelees_tour.append(carte1)
    positions_revelees_tour.append(position1)

    # Si la première carte révélée n'est pas la carte cible, ajuster la cible
    if joueur != 1 and carte1 != carte_cible_ia:
        carte_cible_ia = carte1
        print(
            f"Le joueur {joueur} change sa cible pour compléter le trio de {carte_cible_ia}"
        )

    carte2, dico_temporaire2, position2 = choix(dico_temporaire1, joueur,
                                                carte_cible_ia,
                                                positions_revelees_tour)
    if carte2 is None:
        print("Aucune carte n'a été révélée. Votre tour est terminé.")
        return 0, dico
    cartes_revelees_tour.append(carte2)
    positions_revelees_tour.append(position2)

    if carte1 == carte2:
        carte3, dico_temporaire3, position3 = choix(dico_temporaire2, joueur,
                                                    carte_cible_ia,
                                                    positions_revelees_tour)
        if carte3 is None:
            print("Aucune carte n'a été révélée. Votre tour est terminé.")
            return 0, dico
        cartes_revelees_tour.append(carte3)
        positions_revelees_tour.append(position3)
        if carte3 == carte1:
            # Le trio est complété, on supprime les cartes de leur emplacement
            dico_final = supprimer_cartes(dico, positions_revelees_tour)
            # Ajouter les cartes révélées à la mémoire permanente
            for idx, pos in enumerate(positions_revelees_tour):
                cartes_revelees[pos] = cartes_revelees_tour[idx]
            if carte1 == 7:
                print(
                    colored("Trio de 7, Partie Gagnée ! Bravo !",
                            'green',
                            attrs=['bold']))
                return 7, dico_final
            else:
                print(
                    colored("Trio gagnant ! Un point pour le joueur ", 'green')
                    + colored(str(joueur), 'blue'))
                print(
                    colored("Tour terminé, c'est au joueur suivant.",
                            'yellow'))
                return 1, dico_final
        else:
            print(colored("Le tour est terminé, c'est au suivant.", 'yellow'))
            return 0, dico  # On retourne le dico initial car les cartes sont remises en place
    else:
        print(colored("Le tour est terminé, c'est au suivant.", 'yellow'))
        return 0, dico  # On retourne le dico initial car les cartes sont remises en place


# Supprime les cartes révélées si un trio est formé
def supprimer_cartes(dico, positions_revelees):
    """
    Supprime les cartes révélées de leur emplacement d'origine si un trio est formé.

    Args:
        dico (dict): Dictionnaire des mains des joueurs et des cartes du centre.
        positions_revelees (list): Liste des positions des cartes révélées.

    Returns:
        dict: Le dictionnaire mis à jour.
    """
    dico = deepcopy(dico)  # Créer une copie pour éviter de modifier l'original

    # Regrouper les positions par lieu et par joueur
    positions_centre = []
    positions_joueurs = {}

    for position in positions_revelees:
        lieu = position[0]
        if lieu == 'centre':
            index = position[1]
            positions_centre.append(index)
        elif lieu == 'joueur':
            joueur = position[1]
            index = position[2]
            if joueur not in positions_joueurs:
                positions_joueurs[joueur] = []
            positions_joueurs[joueur].append(index)

    # Supprimer les doublons
    positions_centre = list(set(positions_centre))
    for joueur in positions_joueurs:
        positions_joueurs[joueur] = list(set(positions_joueurs[joueur]))

    # Supprimer les cartes du centre en commençant par les indices les plus élevés
    for index in sorted(positions_centre, reverse=True):
        del dico[0][index]

    # Supprimer les cartes des mains des joueurs en commençant par les indices les plus élevés
    for joueur, indices in positions_joueurs.items():
        for index in sorted(indices, reverse=True):
            del dico[joueur][index]

    return dico


# Fonction pour que l'ordinateur fasse un choix intelligent
def choix_ia(dico, joueur, actions_possibles, carte_cible_ia,
             positions_revelees_tour):
    """
    Prend des décisions pour les joueurs contrôlés par l'ordinateur en tentant de compléter un trio.

    Args:
        dico (dict): Dictionnaire des mains des joueurs et des cartes du centre.
        joueur (int): Numéro du joueur actuel.
        actions_possibles (list): Liste des actions possibles pour ce tour.
        carte_cible_ia (int): La carte que l'IA cherche à obtenir.
        positions_revelees_tour (list): Positions déjà révélées lors de ce tour.

    Returns:
        tuple: L'action choisie par l'IA. Pour 'c', retourne 'c'.
               Pour 'min' ou 'max', retourne (action, numéro_du_joueur).
    """
    # Vérifier si la carte cible est au centre et n'a pas été révélée ce tour
    for pos, carte in dico[0].items():
        if carte == carte_cible_ia and ('centre',
                                        pos) not in positions_revelees_tour:
            if 'c' in actions_possibles:
                return 'c'

    # Vérifier si la carte cible a été révélée comme min ou max d'un joueur précédemment
    for position, carte in cartes_revelees.items():
        if carte == carte_cible_ia and position[0] == 'joueur':
            if 'min' in actions_possibles or 'max' in actions_possibles:
                return ('min',
                        position[1]) if position[2] == 0 else ('max',
                                                               position[1])

    # Si la carte cible est notre propre min ou max, on tente de trouver cette carte chez les autres
    if carte_cible_ia == dico[joueur][0] and 'min' in actions_possibles:
        action = 'min'
    elif carte_cible_ia == dico[joueur][-1] and 'max' in actions_possibles:
        action = 'max'
    else:
        action = random.choice(actions_possibles)

    if action in ['min', 'max']:
        # Trouver les joueurs qui ont des cartes non révélées
        joueurs_possibles = [
            k for k in dico.keys() if k != 0 and len(dico[k]) > 0 and any(
                ('joueur', k, i) not in positions_revelees_tour and
                ('joueur', k, i) not in cartes_revelees
                for i in range(len(dico[k])))
        ]
        if not joueurs_possibles:
            if 'c' in actions_possibles:
                return 'c'
            else:
                return None  # Aucun joueur disponible pour cette action
        choix_joueur = random.choice(joueurs_possibles)
        return (action, choix_joueur)
    else:
        return action


# Permet au joueur de choisir une action durant son tour
def choix(dico,
          joueur,
          carte_cible_ia=None,
          positions_revelees_tour=[],
          choix_joueur=None):
    """
    Offre au joueur des options pour révéler une carte au centre,
    la plus grande ou la plus petite d'un joueur (y compris vous-même).

    Arguments:
        dico (dict): Dictionnaire des mains des joueurs et des cartes du centre.
        joueur (int): Numéro du joueur actuel.
        carte_cible_ia (int): La carte que l'IA cherche à obtenir (pour les joueurs IA).
        positions_revelees_tour (list): Liste des positions déjà révélées lors de ce tour.
        choix_joueur (int): Numéro du joueur dont on veut révéler la carte (pour l'IA).

    Returns:
        tuple: La carte révélée, le dictionnaire mis à jour, et la position de la carte.
    """
    actions_possibles = []
    if len(dico[0]) > 0:
        actions_possibles.append('c')
    joueurs_disponibles = [
        k for k in dico.keys() if k != 0 and len(dico[k]) > 0
    ]  # Inclure le joueur actuel

    if joueurs_disponibles:
        actions_possibles.extend(['min', 'max'])

    if not actions_possibles:
        # Aucun choix possible
        print("Aucun choix possible pour le joueur", joueur)
        return None, dico, None

    while True:
        if joueur == 1:
            choix_act = input(
                'Saisissez "c" pour révéler une carte au centre, "max" pour révéler la carte la plus grande d\'un joueur, "min" pour révéler la carte la plus petite d\'un joueur : '
            ).strip()
            if choix_act not in actions_possibles:
                print(
                    "Choix invalide. Veuillez choisir une action valide parmi :",
                    actions_possibles)
                continue  # Choix invalide, on repropose au joueur son choix
        else:
            # Appel à la fonction d'intelligence artificielle
            action_ia = choix_ia(dico, joueur, actions_possibles,
                                 carte_cible_ia, positions_revelees_tour)
            if action_ia is None:
                print(f"Aucune action possible pour le joueur {joueur}")
                return None, dico, None
            if isinstance(action_ia, tuple):
                choix_act, choix_joueur = action_ia
            else:
                choix_act = action_ia
                choix_joueur = None
            print(f"Le joueur {joueur} choisit : {choix_act}")

        if choix_act == "c":
            if len(dico[0]) == 0:
                print("Il n'y a plus de cartes au centre.")
                continue  # Choix invalide, on repropose au joueur son choix
            else:
                positions_possibles = [
                    pos for pos in dico[0].keys()
                    if ('centre', pos) not in positions_revelees_tour
                ]
                if not positions_possibles:
                    print("Il n'y a plus de cartes au centre disponibles.")
                    continue  # Choix invalide, on repropose au joueur son choix
                if joueur == 1:
                    print("Il reste au centre les cartes de position",
                          positions_possibles, ".")
                    try:
                        choix_carte_centre = int(
                            input(
                                "Saisissez le numéro de la carte que vous voulez révéler : "
                            ).strip())
                    except ValueError:
                        print(
                            "Entrée invalide. Veuillez entrer un numéro de carte valide."
                        )
                        continue  # Choix invalide, on repropose au joueur son choix
                    if choix_carte_centre not in positions_possibles:
                        print(
                            "Cette carte a déjà été révélée ou n'est pas disponible. Veuillez en choisir une autre."
                        )
                        continue
                else:
                    choix_carte_centre = random.choice(positions_possibles)
                    print(
                        f"Le joueur {joueur} choisit de révéler la carte en position {choix_carte_centre}"
                    )
                carte = dico[0][choix_carte_centre]
                print("La carte retournée est : ", carte)
                # Enregistrer la position de la carte révélée
                position = ('centre', choix_carte_centre)
                dico_bis = deepcopy(dico)
                break  # Choix valide fait, on sort de la boucle while

        elif choix_act == "min":
            joueurs_possibles = [
                k for k in joueurs_disponibles
                if any(('joueur', k, i) not in positions_revelees_tour and (
                    'joueur', k, i) not in cartes_revelees
                       for i in range(len(dico[k])))
            ]
            if not joueurs_possibles:
                print("Aucun joueur disponible pour cette action.")
                continue
            if joueur == 1:
                try:
                    choix_j = int(
                        input(
                            "Saisissez le numéro du joueur dont vous voulez révéler la carte (vous pouvez choisir votre propre numéro) : "
                        ).strip())
                except ValueError:
                    print(
                        "Entrée invalide. Veuillez entrer un numéro de joueur valide."
                    )
                    continue  # Choix invalide, on repropose au joueur son choix
                if choix_j not in joueurs_possibles:
                    print("Ce joueur n'est pas disponible pour cette action.")
                    continue
            else:
                if choix_joueur is not None:
                    choix_j = choix_joueur
                    print(
                        f"Le joueur {joueur} choisit de révéler la carte minimale du joueur {choix_j}"
                    )
                else:
                    choix_j = random.choice(joueurs_possibles)
                    print(
                        f"Le joueur {joueur} choisit de révéler la carte minimale du joueur {choix_j}"
                    )
            indices_non_reveles = [
                i for i in range(len(dico[choix_j]))
                if ('joueur', choix_j, i) not in positions_revelees_tour and (
                    'joueur', choix_j, i) not in cartes_revelees
            ]
            if not indices_non_reveles:
                print(f"Le joueur {choix_j} n'a plus de cartes non révélées.")
                continue
            index_min = indices_non_reveles[0]  # Plus petit indice non révélé
            carte = dico[choix_j][index_min]
            print(f"La carte révélée du joueur {choix_j} est : {carte}")
            # Enregistrer la position de la carte révélée
            position = ('joueur', choix_j, index_min)
            dico_bis = deepcopy(dico)
            break

        elif choix_act == "max":
            joueurs_possibles = [
                k for k in joueurs_disponibles
                if any(('joueur', k, i) not in positions_revelees_tour and (
                    'joueur', k, i) not in cartes_revelees
                       for i in range(len(dico[k])))
            ]
            if not joueurs_possibles:
                print("Aucun joueur disponible pour cette action.")
                continue
            if joueur == 1:
                try:
                    choix_j = int(
                        input(
                            "Saisissez le numéro du joueur dont vous voulez révéler la carte (vous pouvez choisir votre propre numéro) : "
                        ).strip())
                except ValueError:
                    print(
                        "Entrée invalide. Veuillez entrer un numéro de joueur valide."
                    )
                    continue
                if choix_j not in joueurs_possibles:
                    print("Ce joueur n'est pas disponible pour cette action.")
                    continue
            else:
                if choix_joueur is not None:
                    choix_j = choix_joueur
                    print(
                        f"Le joueur {joueur} choisit de révéler la carte maximale du joueur {choix_j}"
                    )
                else:
                    choix_j = random.choice(joueurs_possibles)
                    print(
                        f"Le joueur {joueur} choisit de révéler la carte maximale du joueur {choix_j}"
                    )
            indices_non_reveles = [
                i for i in range(len(dico[choix_j]) - 1, -1, -1)
                if ('joueur', choix_j, i) not in positions_revelees_tour and (
                    'joueur', choix_j, i) not in cartes_revelees
            ]
            if not indices_non_reveles:
                print(f"Le joueur {choix_j} n'a plus de cartes non révélées.")
                continue
            index_max = indices_non_reveles[0]  # Plus grand indice non révélé
            carte = dico[choix_j][index_max]
            print(f"La carte révélée du joueur {choix_j} est : {carte}")
            # Enregistrer la position de la carte révélée
            position = ('joueur', choix_j, index_max)
            dico_bis = deepcopy(dico)
            break

        else:
            print("Choix invalide. Veuillez choisir une action valide parmi :",
                  actions_possibles)
            continue  # Choix invalide, on repropose au joueur son choix

    return carte, dico_bis, position


# Initialise le jeu en demandant le nombre de joueurs et en distribuant les cartes
def demarrer():
    """
    Initialise le jeu en configurant le nombre de joueurs et en distribuant les cartes.

    Returns:
        tuple: Le dictionnaire des mains des joueurs et le nombre de joueurs.
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
    cartes = creer_jeu_cartes()
    dico = {}
    if nombre_joueurs == 3:
        dico = repartir_cartes(3, 9, cartes)
    elif nombre_joueurs == 4:
        dico = repartir_cartes(4, 7, cartes)
    elif nombre_joueurs == 5:
        dico = repartir_cartes(5, 6, cartes)
    elif nombre_joueurs == 6:
        dico = repartir_cartes(6, 5, cartes)
    return dico, nombre_joueurs


    # Fonction principale qui gère le déroulement du jeu
def code_central():
    """
        Exécute la boucle principale du jeu jusqu'à ce qu'un joueur gagne.
        """
    dico, nb_joueurs = demarrer()
    points = [0 for _ in range(nb_joueurs)]
    vmax = 0
    imax = 0
    tour = 1
    while vmax < 3:
        joueur = autour_de(nb_joueurs, tour)
        print("\n" * 2)
        print(colored("Cartes disponibles au centre : ", 'cyan'),
              list(dico[0].keys()))
        print("Scores actuels : ", points)
        print("\n")
        print("C'est au joueur", colored(str(joueur), 'blue'), "de jouer.")

        if joueur != 1:
            print("Ce joueur est géré par l'ordinateur.")
            print(
                "Cartes de l'ordinateur :", dico[joueur]
            )  #Le print des cartes du joueur géré de manière automatique permet de vérifier si les choix faits paraissent logiques ou non, ligne à retirer pour rendre le jeu à nouveau compétitif

        if len(dico[joueur]) == 0 and joueur == 1:
            print(
                colored("Le joueur ", 'red') + colored(str(joueur), 'blue') +
                " n'a plus de cartes.")
        elif joueur == 1:
            print("Vos cartes sont :", colored(str(dico[joueur]), 'blue'))

        print("\n")
        points_gagnes, dico = action(dico, joueur)

        if joueur <= len(points):
            points[joueur - 1] += points_gagnes

        vmax, imax = maximum(points)
        tour += 1

        if tour % nb_joueurs == 1:
            print("\n")
            print(
                colored('*-----*-----*-----*-----*-----*-----*-----*-----*',
                        'yellow'))

        time.sleep(3)

    print("\n")
    print("Le joueur", colored(str(imax + 1), 'green'), "est le gagnant !")


# Démarrage du jeu
if __name__ == "__main__":
    code_central()
