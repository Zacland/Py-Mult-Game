#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (unicode_literals, absolute_import, print_function, division)

"""
    Interro sur les tables de multiplcation
    On passe la (les) table(s) en paramètre (séparées par une virgule : 6,7,8)
    On note les scores (vrai/faux/total)
    On note les temps (début, fin, temps de réponse)
"""

__author__  = "Zacland"
__version__ = "1.0"
__license__ = "Zacland.net"

#
# IMPORTS
#

import os, sys, logging, time, argparse, string
import random
from datetime import datetime

#
# FONCTIONS
#

def deltaFormat (myTime):
    totalSeconds = myTime.seconds
    hours, remainder = divmod(totalSeconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours != 0:
        return '%sh %sm %ss' % (hours, minutes, seconds)
    else:
        return '%sm %ss' % (minutes, seconds)

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def extractFilename(sFilename):
    """ Récupère le nom sans l'extension """
    sOut = '.'.join(sFilename.split('.')[:-1])
    return sOut

#
# MAIN
#

def main():
    """ Run the whole program """

    #----------------------------------------------------
    # On Parse les arguments
    #----------------------------------------------------

    parser = argparse.ArgumentParser(
                                        description = 'Programme qui permet de faire défiler des questions sur une table \
                                        particulière ou un ensemble de table. Un niveau permet de choisir la difficulté.',
                                        epilog = 'Utilisation : multiplication.py 6 (uniquement la table de 6)\n \
                                        multiplication.py 3,4,5,6 (uniquement un mélange des tables de 3,4,5 et 6) \
                                        multiplication.py 4,5 -lvl=5 (uniquement un mélange des tables de 4 et 5 mais en prenant le \
                                        deuxième facteur >= 5).'
                                    )

    parser.add_argument(
                            'table',
                            help = 'Numéro de la table de multiplication.'
                        )

    parser.add_argument(
                            '-lvl',
                            help = 'Niveau de difficulté (1-9).',
                            choices = ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
                            default = 1
                        )

    parser.add_argument(
                            '-o',
                            '--outfile',
                            help = 'Nom du fichier généré. \
                                    Si non spécifie, le fichier sera généré tout seul.',
                            default = 'resultat.txt'
                        )

    parser.add_argument(
                            '-l',
                            '--log',
                            dest    = 'sLogLevel',
                            choices = ['DEBUG', 'INFO'],
                            help    = 'Niveau du log (INFO par défaut). DEBUG pour plus de détails.',
                            default = 'INFO'
                        )

    args = parser.parse_args()

    iTmpTable = args.table
    sOutfile  = args.outfile
    iLvl      = int(args.lvl)
    sFilename = sys.argv[0]

    iTable = iTmpTable.split(",")

    #----------------------------------------------------
    # On initialise le logging
    #----------------------------------------------------

    logging.basicConfig(
                            filename=extractFilename(sFilename) + '.log',
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%d/%m/%Y-%H:%M',
                            filemode='w',
                            level=getattr(logging, args.sLogLevel)
                        )

    logging.getLogger(__name__)

    dateStart = datetime.now()
    logging.info('Démarrage du process : %s' % (dateStart.strftime('%x - %X')))

    logging.debug('Nom du programme = ' + sFilename)
    logging.debug('Table = ' , iTable)
    logging.debug('Outfile = ' + str(sOutfile))

#    sOutfile = "resultat.txt"

    #----------------------------------------------------
    # START !!!
    #----------------------------------------------------

    # On met les variables à 0
    iCptBon   = 0
    iCptFaux  = 0
    iCptTotal = 0
    iReponse  = 0

    # On efface l'écran
    cls()

    try:
        # On crée le fichier de suivi
        with open(sOutfile, 'w') as outfile:

            # On y inscrit le level
            outfile.write("Niveau: %d\n" % (iLvl))

            # Tant que l'utilisateur ne sort pas (-1), on pose les questions
            while iReponse != -1:

                # On prend le temps au moment où on pose la question
                tIn = datetime.now()

                # On initialise les facteurs et on calcule le produit pour comparer avec la réponse
                # iFacteur1 représente les tables passées en paramètre et on en prend une au hasard
                iFacteur1 = int(random.choice(iTable))
                # iFacteur2 représente un choix au hasard entre iLvl et 10 (Plus iLvl augmente moins on a les petites valeurs à multiplier)
                iFacteur2 = int(random.randint(iLvl, 10))
                iProduit = int(iFacteur1 * iFacteur2)

                # On boucle sur la saisie pour passer les "Entrée" sans saisies ou les saisies autres que numériques
                while True:
                    try:
                        # On attend un entier
                        print("\n(-1 pour sortir...)\n")
                        iReponse = int(input("Combien font %d X %d = " % (iFacteur1, iFacteur2)))
                        bResultat = iReponse == iProduit
                        # On sort du while si tout s'est bien passé
                        break
                    except ValueError:
                        # Si jamais il y a une erreur de saisie, on boucle sur la demande (en gardant les mêmes facteurs)
                        continue

                # Le contrat est rempli, on arrête le chrono
                tOut = datetime.now()

                # Si le résultat est bon
                if bResultat:
                    # On félicite le joueur
                    print("\nBRAVO !")
                    # On incrémente les Bons
                    iCptBon += 1
                    # On sauve le tout dans un fichier de stats
                    outfile.write("%-2d X %-2d = %-2d BON  en %-15s\n" % (iFacteur1, \
                                                                           iFacteur2, \
                                                                           iProduit, \
                                                                           deltaFormat(tOut-tIn)))
                    # On attend 1 seconde que l'utilisateur ai le temps de lire
                    time.sleep(1)
                    # Puis on efface l'écran pour qu'il ne soit pas tenté de regarder les résultats précédents
                    cls()
                else:
                    # Sinon, si le résultat est faux ET que l'on est pas en mode "sortie du jeu"
                    if iReponse != -1:
                        # On prévient l'utilisateur qu'il s'est trompé
                        print("\nNon. %d X %d = %d" % (iFacteur1, iFacteur2, iProduit))
                        # On augmente le compteur des Faux
                        iCptFaux = iCptFaux + 1
                        # On sauve le tout dans un fichier de stats
                        outfile.write("%-2d X %-2d = %-2d FAUX en %-15s -- (répondu: %-2d) \n" % (iFacteur1, \
                                                                                                   iFacteur2, \
                                                                                                   iProduit, \
                                                                                                   deltaFormat(tOut-tIn), \
                                                                                                   iReponse))
                        # On attend 4 secondes le temps qu'il lise la bonne réponse
                        time.sleep(4)
                        # Puis on efface l'écran pour qu'il ne soit pas tenté de regarder les résultats précédents
                        cls()

                # Comme on jour toujours, on affiche un mini score au joueur histoire qu'il sache où il en est
                if iReponse != -1:
                    iCptTotal = iCptTotal + 1
                    print("\nRéussi: %d (%2.2f%%)- Faux: %d (%2.2f%%)- Total: %d" % (iCptBon, iCptBon/iCptTotal*100, iCptFaux, iCptFaux/iCptTotal*100,iCptTotal))

                # Et on recommence au début (while) !

    except EnvironmentError as e:
        logging.exception(e)
        sys.exit(e)

    finally:
        # On note la date de fin pour calculer le temps du test
        dateStop = datetime.now()
        logging.info('Fin du process à %s' % (dateStop.strftime('%x - %X')))

        # On calcule le delta par rapport au temps de démarrage
        dDelta = dateStop - dateStart
        logging.info('Temps d\'exécution: %s' % (dDelta))

        # On affiche les scores
        print("Nombre de bons: %d - Nombre de faux: %d sur un total de %d" % (iCptBon, iCptFaux, iCptTotal))

        # On note les stats si on n'est pas sorti dès le départ
        if iCptTotal != 0:
            try:
                # On peaufine le fichier de sortie en rajoutant les infos finales
                with open(sOutfile, 'a') as outfile:
                    outfile.write("Nombre de bons: %-2d (%2.2f) - Nombre de faux: %-2d (%2.2f) - Total: %d - Durée de la session de %-15s" % (iCptBon, iCptBon/iCptTotal*100, iCptFaux, iCptFaux/iCptTotal*100, iCptTotal, deltaFormat(dDelta)))
            except EnvironmentError as e:
                logging.exception(e)
                sys.exit(e)

        print("Fichier généré avec succès: %s" % (sOutfile))

if __name__ == '__main__':
    main()
