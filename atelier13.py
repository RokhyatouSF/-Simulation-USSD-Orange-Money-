import time

# PARAMÈTRES DU COMPTE ORANGE MONEY

compte_om_solde = 50000
code_secret_client = "1234"
limite_tentatives_pin = 3

journal_operations_om = []
memoire_transfert_recent = None

duree_max_session_ussd = 180
horodatage_derniere_action = time.time()


# FONCTIONS UTILITAIRES USSD
def verifier_delai_session_ussd():
    global horodatage_derniere_action
    if time.time() - horodatage_derniere_action > duree_max_session_ussd:
        print("\n Session USSD expirée. Recomposez #144#")
        return True
    horodatage_derniere_action = time.time()
    return False


def authentifier_utilisateur():
    tentatives = 0
    while tentatives < limite_tentatives_pin:
        pin_saisi = input("Entrez votre code secret : ")
        if pin_saisi == code_secret_client:
            return True
        print("Code secret incorrect.")
        tentatives += 1
    print(" Accès bloqué.")
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
    choix = input("1. Confirmer\n 2. Annuler\nVotre choix : ")
    return choix == "1"


def verifier_format_numero_msisdn(msisdn):
    prefixes_autorises = ("77", "78", "75")
    return msisdn.isdigit() and len(msisdn) == 9 and msisdn.startswith(prefixes_autorises)


def enregistrer_operation_journal(type_op, montant, libelle):
    journal_operations_om.append({
        "operation": type_op,
        "montant": montant,
        "detail": libelle
    })



# SERVICES ORANGE MONEY
def afficher_solde_compte_om():
    print(f"\n Solde disponible : {compte_om_solde} F CFA")


def executer_achat_credit_om():
    global compte_om_solde

    montant = saisir_montant_transaction()
    if montant is None or montant > compte_om_solde:
        print("Solde insuffisant.")
        return

    if confirmer_operation_client() and authentifier_utilisateur():
        compte_om_solde -= montant
        enregistrer_operation_journal("ACHAT_CRÉDIT", montant, "Recharge crédit")
        print(f"Achat effectué. Nouveau solde : {compte_om_solde} F")


def executer_transfert_om():
    global compte_om_solde, memoire_transfert_recent

    numero_cible = input("Numéro du bénéficiaire : ")
    if not verifier_format_numero_msisdn(numero_cible):
        print("Numéro non valide.")
        return

    montant = saisir_montant_transaction()
    if montant is None or montant > compte_om_solde:
        print("Solde insuffisant.")
        return

    print(f"Transfert de {montant} F vers {numero_cible}")
    if confirmer_operation_client() and authentifier_utilisateur():
        compte_om_solde -= montant
        memoire_transfert_recent = montant
        enregistrer_operation_journal("TRANSFERT", montant, f"Vers {numero_cible}")
        print(f"Transfert réussi. Solde : {compte_om_solde} F")


def proposer_forfaits_internet_om():
    global compte_om_solde

    catalogue_forfaits = {
        1: ("Pass Internet 100 Mo", 500),
        2: ("Pass Internet 500 Mo", 1000),
        3: ("Pass Internet 1 Go", 2000)
    }

    print("\n FORFAITS INTERNET")
    for code, forfait in catalogue_forfaits.items():
        print(f"{code}. {forfait[0]} - {forfait[1]} F")

    try:
        choix = int(input("Sélectionnez un forfait : "))
        if choix not in catalogue_forfaits:
            print("Choix incorrect.")
            return

        prix = catalogue_forfaits[choix][1]
        if prix > compte_om_solde:
            print("Solde insuffisant.")
            return

        if confirmer_operation_client() and authentifier_utilisateur():
            compte_om_solde -= prix
            enregistrer_operation_journal("FORFAIT", prix, catalogue_forfaits[choix][0])
            print(f"Forfait activé. Solde : {compte_om_solde} F")

    except ValueError:
        print("Erreur de sélection.")


def annuler_transfert_recent_om():
    global compte_om_solde, memoire_transfert_recent

    if memoire_transfert_recent is None:
        print("Aucun transfert à annuler.")
        return

    print(f"Annuler le transfert de {memoire_transfert_recent} F ?")
    if confirmer_operation_client() and authentifier_utilisateur():
        compte_om_solde += memoire_transfert_recent
        enregistrer_operation_journal("ANNULATION", memoire_transfert_recent, "Annulation transfert")
        memoire_transfert_recent = None
        print(f"Transfert annulé. Solde : {compte_om_solde} F")


def afficher_journal_operations():
    if not journal_operations_om:
        print("Aucune opération enregistrée.")
        return

    print("\n JOURNAL DES OPÉRATIONS")
    for index, op in enumerate(journal_operations_om, start=1):
        print(f"{index}. {op['operation']} - {op['montant']} F ({op['detail']})")


# INTERFACE USSD PRINCIPALE


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

print("Composer #144#")

while True:
    if verifier_delai_session_ussd():
        break

    afficher_menu_ussd_om()
    selection = input("Votre choix : ")

    if selection == "1":
        afficher_solde_compte_om()
    elif selection == "2":
        executer_achat_credit_om()
    elif selection == "3":
        executer_transfert_om()
    elif selection == "4":
        proposer_forfaits_internet_om()
    elif selection == "5":
        annuler_transfert_recent_om()
    elif selection == "6":
        afficher_journal_operations()
    elif selection == "0":
        print("Merci d’avoir utilisé Orange Money.")
        break
    else:
        print("Choix non reconnu.")
