#Description générale
Ce programme est une simulation du service Orange Money via USSD (#144#) écrite en Python.
Il permet de gérer un compte virtuel avec solde, transferts, achats, journal des opérations et persistance des données dans un fichier JSON.

#Fonctionnalités principales
##Gestion du compte
    Initialisation d’un solde de départ.
    Consultation du solde actuel.
    Mise à jour automatique du solde après chaque opération.

##Authentification sécurisée
    Vérification du code secret (PIN).
    Limitation du nombre de tentatives (3 essais maximum).
    Blocage de l’accès après dépassement du nombre d’essais.

##Gestion de la session USSD
    Simulation d’une durée maximale de session (180 secondes).
    Déconnexion automatique en cas d’inactivité.
    Message indiquant l’expiration de la session.

##Achat de crédit
    Saisie du montant à acheter.
    Vérification du solde disponible.
    Confirmation de l’opération par l’utilisateur.
    Authentification par code secret.
    Débit du solde après validation.
    Enregistrement de l’opération dans le journal.
    Sauvegarde automatique des données.

##Transfert d’argent
    Saisie du numéro du bénéficiaire.
    Vérification du format du numéro (9 chiffres avec préfixes autorisés seulement 77 78 75 ).
    Saisie du montant à transférer.
    Vérification du solde.
    Confirmation + authentification.
    Débit du solde.
    Mémorisation du dernier transfert effectué.
    Enregistrement de l’opération dans le journal.
    Sauvegarde des données dans un fichier JSON.

##Annulation du transfert récent
    Vérification de l’existence d’un transfert récent.
    Confirmation de l’utilisateur.
    Authentification par code secret.
    Remboursement du montant annulé.
    Réinitialisation du transfert récent.
    Enregistrement de l’annulation dans le journal.
    Sauvegarde des données.

##Achat de forfaits Internet
    Affichage d’une liste de forfaits disponibles.
    Choix du forfait par l’utilisateur.
    Vérification du solde.
    Confirmation et authentification.
    Débit du solde.
    Enregistrement de l’opération dans le journal.
    Sauvegarde automatique.

##Journal des opérations
    Enregistrement de toutes les opérations :
    Achat de crédit
    Transfert
    Annulation
    Forfaits Internet

##Chaque opération contient :
    Type d’opération
    Montant
    Détail
    Date et heure

###Affichage du journal du plus récent au plus ancien.
###Persistance des données (JSON)
###Sauvegarde automatique dans le fichier compte_om.json.

##Données sauvegardées :
    Solde du compte
    Journal des opérations
    Transfert récent
    Chargement automatique des données au démarrage du programme.
    Conservation des informations après redémarrage.

##Gestion des erreurs
###Gestion du fichier JSON :
    Fichier inexistant
    Fichier vide
    Fichier mal formé

##Gestion des saisies incorrectes :
    Montant invalide
    Choix de menu incorrect
    Numéro non valide
    Messages clairs pour guider l’utilisateur.

##Fichiers utilisés
compte_om.json : stockage permanent des données du compte.
Script Python principal : logique de l’application.

```bash

https://github.com/RokhyatouSF/-Simulation-USSD-Orange-Money-.git
