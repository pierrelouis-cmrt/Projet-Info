import os


def choisir_et_executer_script():
    fichiers = sorted(f for f in os.listdir()
                      if f.endswith('.py') and f != 'main.py')
    if not fichiers:
        return print("\033[91m\nAucun script disponible.\033[0m")

    print("\n\033[96m===== Scripts Disponibles =====\033[0m")
    for i, f in enumerate(fichiers, 1):
        print(f"\033[93m{i}.\033[0m \033[92m{f}\033[0m")
    print("\033[96m===============================\033[0m")

    try:
        choix = int(
            input("\n\033[94mEntrez le numéro du script à exécuter : \033[0m")
        ) - 1
        if choix < 0 or choix >= len(fichiers):
            raise ValueError
        print(f"\n\033[95mExécution de {fichiers[choix]}...\033[0m\n")
        os.system(f'python3 "{fichiers[choix]}"')
    except (ValueError, IndexError):
        print("\033[91m\nEntrée invalide. Veuillez réessayer.\033[0m")


if __name__ == "__main__":
    choisir_et_executer_script()
