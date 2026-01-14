import time
import json
import os

# PARAMÈTRES DU COMPTE ORANGE MONEY
compte_om_solde = 50000
code_secret_client = "1234"
limite_tentatives_pin = 3

journal_operations_om = []
memoire_transfert_recent = None

duree_max_session_ussd = 180
horodatage_derniere_action = time.time()

FICHIER_DONNEES = "compte_om.json"


# PERSISTANCE DES DONNÉES

def sauvegarder_donnees():
    try:
        donnees = {
            "solde": compte_om_solde,
            "journal": journal_operations_om,
            "transfert_recent": memoire_transfert_recent
        }

        with open(FICHIER_DONNEES, "w", encoding="utf-8") as f:
            json.dump(donnees, f, indent=4)

    except IOError:
        print("Erreur lors de la sauvegarde des données.")


def charger_donnees():
    global compte_om_solde, journal_operations_om, memoire_transfert_recent

    try:
        if not os.path.exists(FICHIER_DONNEES):
            return 

        with open(FICHIER_DONNEES, "r", encoding="utf-8") as f:
            donnees = json.load(f)

            compte_om_solde = donnees.get("solde", 50000)
            journal_operations_om = donnees.get("journal", [])
            memoire_transfert_recent = donnees.get("transfert_recent", None)

    except (IOError, json.JSONDecodeError):
        print("Erreur lors du chargement des données. Données réinitialisées.")


# FONCTIONS  USSD
def verifier_delai_session_ussd():
    global horodatage_derniere_action
    if time.time() - horodatage_derniere_action > duree_max_session_ussd:
        print("\nSession USSD expirée. Recomposez #144#")
        return True
    horodatage_derniere_action = time.time()
    return False


def authentifier_utilisateur():
    tentatives = 0
    while tentatives < limite_tentatives_pin:
        pin = input("Entrez votre code secret : ")
        if pin == code_secret_client:
            return True
        print("Code secret incorrect.")
        tentatives += 1
    print("Accès bloqué.")
    return False


def saisir_montant_transaction():
    try:
        montant = int(input("Saisissez le montant : "))
        if montant <= 0:
            print("Montant non valide.")
            return None
        return montant
    except ValueError:
        print("Erreur de saisie du montant.")
        return None


def confirmer_operation_client():
    choix = input("1. Confirmer\n2. Annuler\nVotre choix : ")
    return choix == "1"


def verifier_format_numero_msisdn(msisdn):
    prefixes_autorises = ("77", "78", "75")
    return msisdn.isdigit() and len(msisdn) == 9 and msisdn.startswith(prefixes_autorises)


def enregistrer_operation_journal(type_op, montant, libelle):
    journal_operations_om.insert(0, {  
        "operation": type_op,
        "montant": montant,
        "detail": libelle,
        "date": time.strftime("%d/%m/%Y %H:%M:%S")
    })



# SERVICES ORANGE MONEY
def afficher_solde_compte_om():
    print(f"\nSolde disponible : {compte_om_solde} F CFA")


def executer_achat_credit_om():
    global compte_om_solde

    montant = saisir_montant_transaction()
    if montant is None or montant > compte_om_solde:
        print("Solde insuffisant.")
        return

    if confirmer_operation_client() and authentifier_utilisateur():
        compte_om_solde -= montant
        enregistrer_operation_journal("ACHAT_CREDIT", montant, "Recharge credit")
        sauvegarder_donnees()
        print(f"Achat effectué. Nouveau solde : {compte_om_solde} F")


def executer_transfert_om():
    global compte_om_solde, memoire_transfert_recent

    numero = input("Numéro du bénéficiaire : ")
    if not verifier_format_numero_msisdn(numero):
        print("Numéro non valide.")
        return

    montant = saisir_montant_transaction()
    if montant is None or montant > compte_om_solde:
        print("Solde insuffisant.")
        return

    if confirmer_operation_client() and authentifier_utilisateur():
        compte_om_solde -= montant
        memoire_transfert_recent = montant
        enregistrer_operation_journal("TRANSFERT", montant, f"Vers {numero}")
        sauvegarder_donnees()
        print(f"Transfert réussi. Solde : {compte_om_solde} F")


def proposer_forfaits_internet_om():
    global compte_om_solde

    forfaits = {
        1: ("Pass Internet 100 Mo", 500),
        2: ("Pass Internet 500 Mo", 1000),
        3: ("Pass Internet 1 Go", 2000)
    }

    for k, v in forfaits.items():
        print(f"{k}. {v[0]} - {v[1]} F")

    try:
        choix = int(input("Sélectionnez un forfait : "))
        if choix not in forfaits:
            print("Choix invalide.")
            return

        prix = forfaits[choix][1]
        if prix > compte_om_solde:
            print("Solde insuffisant.")
            return

        if confirmer_operation_client() and authentifier_utilisateur():
            compte_om_solde -= prix
            enregistrer_operation_journal("FORFAIT", prix, forfaits[choix][0])
            sauvegarder_donnees()
            print(f"Forfait activé. Solde : {compte_om_solde} F")

    except ValueError:
        print("Erreur de saisie.")


def annuler_transfert_recent_om():
    global compte_om_solde, memoire_transfert_recent

    if memoire_transfert_recent is None:
        print("Aucun transfert à annuler.")
        return

    if confirmer_operation_client() and authentifier_utilisateur():
        compte_om_solde += memoire_transfert_recent
        enregistrer_operation_journal("ANNULATION", memoire_transfert_recent, "Annulation transfert")
        memoire_transfert_recent = None
        sauvegarder_donnees()
        print(f"Transfert annulé. Solde : {compte_om_solde} F")


def afficher_journal_operations():
    if not journal_operations_om:
        print("Aucune opération enregistrée.")
        return

    for i, op in enumerate(journal_operations_om, start=1):
        print(f"{i}. {op['date']} - {op['operation']} - {op['montant']} F ({op['detail']})")



# MENU USSD

def afficher_menu_ussd_om():
    print("""
ORANGE MONEY - #144#
1. Consulter le solde
2. Achat de crédit
3. Transfert d'argent
4. Forfaits Internet
5. Annulation transfert
6. Journal des opérations
0. Quitter
""")


# PROGRAMME PRINCIPAL

charger_donnees()
print("Composer #144#")

while True:
    if verifier_delai_session_ussd():
        break

    afficher_menu_ussd_om()
    choix = input("Votre choix : ")

    if choix == "1":
        afficher_solde_compte_om()
    elif choix == "2":
        executer_achat_credit_om()
    elif choix == "3":
        executer_transfert_om()
    elif choix == "4":
        proposer_forfaits_internet_om()
    elif choix == "5":
        annuler_transfert_recent_om()
    elif choix == "6":
        afficher_journal_operations()
    elif choix == "0":
        print("Merci d’avoir utilisé Orange Money.")
        break
    else:
        print("Choix non reconnu.")
