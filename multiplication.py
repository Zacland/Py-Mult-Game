#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Ligne à activer pour la compatibilité en version 2 de Python
# from __future__ import (unicode_literals, absolute_import, print_function, division)

"""
    Interro sur les tables de multiplcation
    On passe la (les) table(s) en paramètre (séparées par une virgule : 6,7,8)
    On note les scores (vrai/faux/total)
    On note les temps (début, fin, temps de réponse)
"""

__author__ = "Zacland"
__version__ = "1.0"
__license__ = "Zacland.net"

#
# IMPORTS
#
import os
import sys
import logging
import time
import argparse
import random
from datetime import datetime


#
# FONCTIONS
#
def delta_format(my_time):
    total_seconds = my_time.seconds
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours != 0:
        return '%sh %sm %ss' % (hours, minutes, seconds)
    else:
        return '%sm %ss' % (minutes, seconds)


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def extract_filename(s_filename):
    """ Récupère le nom sans l'extension """
    s_out = '.'.join(s_filename.split('.')[:-1])
    return s_out


#
# MAIN
#
def main():
    """ Run the whole program """

    # ----------------------------------------------------
    # On Parse les arguments
    # ----------------------------------------------------

    parser = argparse.ArgumentParser(
        description='Programme qui permet de faire défiler des questions sur une \
                                        table particulière ou un ensemble de table. Un niveau permet de choisir \
                                        la difficulté.',
        epilog='Utilisation : multiplication.py 6 (uniquement la table de 6)\n \
                                        multiplication.py 3,4,5,6 (uniquement un mélange des tables de 3,4,5 et 6) \
                                        multiplication.py 4,5 -lvl=5 (uniquement un mélange des tables de 4 et 5 \
                                        mais en prenant le deuxième facteur >= 5).'
    )

    parser.add_argument(
        'table',
        help='Numéro de la table de multiplication.',
        default='1, 2, 3, 4, 5, 6, 7, 8, 9'
    )

    parser.add_argument(
        '-lvl',
        help='Niveau de difficulté (1-9).',
        choices=['1', '2', '3', '4', '5', '6', '7', '8', '9'],
        default=1
    )

    parser.add_argument(
        '-o',
        '--outfile',
        help='Nom du fichier généré. \
                                    Si non spécifie, le fichier sera généré tout seul.',
        default='resultat.txt'
    )

    parser.add_argument(
        '-l',
        '--log',
        dest='sLogLevel',
        choices=['DEBUG', 'INFO'],
        help='Niveau du log (INFO par défaut). DEBUG pour plus de détails.',
        default='INFO'
    )

    args = parser.parse_args()

    i_tmp_table = args.table
    s_outfile = args.outfile
    i_lvl = int(args.lvl)
    s_filename = sys.argv[0]

    i_table = i_tmp_table.split(",")

    # ----------------------------------------------------
    # On initialise le logging
    # ----------------------------------------------------

    logging.basicConfig(
        filename=extract_filename(s_filename) + '.log',
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        datefmt='%d/%m/%Y-%H:%M',
        filemode='w',
        level=getattr(logging, args.sLogLevel)
    )

    logging.getLogger(__name__)

    date_start = datetime.now()
    logging.info('Démarrage du process : %s' % (date_start.strftime('%x - %X')))

    logging.debug('Nom du programme = ' + s_filename)
    logging.debug('Table = ', i_table)
    logging.debug('Outfile = ' + str(s_outfile))

    # ----------------------------------------------------
    # START !!!
    # ----------------------------------------------------

    # On met les variables à 0
    i_cpt_bon = 0
    i_cpt_faux = 0
    i_cpt_total = 0
    i_reponse = 0

    # On efface l'écran
    cls()

    try:
        # On crée le fichier de suivi
        with open(s_outfile, 'w') as outfile:

            # On y inscrit le level
            outfile.write("Niveau: %d\n" % i_lvl)

            # Tant que l'utilisateur ne sort pas (-1), on pose les questions
            while i_reponse != -1:

                # On prend le temps au moment où on pose la question
                t_in = datetime.now()

                # On initialise les facteurs et on calcule le produit pour comparer avec la réponse
                # i_facteur1 représente les tables passées en paramètre et on en prend une au hasard
                i_facteur1 = int(random.choice(i_table))
                # i_facteur2 représente un choix au hasard entre i_lvl et 10
                # (Plus i_lvl augmente moins on a les petites valeurs à multiplier)
                i_facteur2 = int(random.randint(i_lvl, 10))
                i_produit = int(i_facteur1 * i_facteur2)

                # On boucle sur la saisie pour passer les "Entrée" sans saisies ou les saisies autres que numériques
                while True:
                    try:
                        # On attend un entier
                        print("\n(-1 pour sortir...)\n")
                        i_reponse = int(input("Combien font %d X %d = " % (i_facteur1, i_facteur2)))
                        b_resultat = i_reponse == i_produit
                        # On sort du while si tout s'est bien passé
                        break
                    except ValueError:
                        # Si jamais il y a une erreur de saisie,
                        # on boucle sur la demande (en gardant les mêmes facteurs)
                        continue

                # Le contrat est rempli, on arrête le chrono
                t_out = datetime.now()

                # Si le résultat est bon
                if b_resultat:
                    # On félicite le joueur
                    print("\nBRAVO !")
                    # On incrémente les Bons
                    i_cpt_bon += 1
                    # On sauve le tout dans un fichier de stats
                    outfile.write("%-2d X %-2d = %-2d BON  en %-15s\n" % (i_facteur1,
                                                                          i_facteur2,
                                                                          i_produit,
                                                                          delta_format(t_out - t_in)))
                    # On attend 1 seconde que l'utilisateur ai le temps de lire
                    time.sleep(1)
                    # Puis on efface l'écran pour qu'il ne soit pas tenté de regarder les résultats précédents
                    cls()
                else:
                    # Sinon, si le résultat est faux ET que l'on est pas en mode "sortie du jeu"
                    if i_reponse != -1:
                        # On prévient l'utilisateur qu'il s'est trompé
                        print("\nNon. %d X %d = %d" % (i_facteur1, i_facteur2, i_produit))
                        # On augmente le compteur des Faux
                        i_cpt_faux = i_cpt_faux + 1
                        # On sauve le tout dans un fichier de stats
                        outfile.write("%-2d X %-2d = %-2d FAUX en %-15s -- (répondu: %-2d) \n" %
                                      (i_facteur1,
                                       i_facteur2,
                                       i_produit,
                                       delta_format(t_out - t_in),
                                       i_reponse))
                        # On attend 4 secondes le temps qu'il lise la bonne réponse
                        time.sleep(4)
                        # Puis on efface l'écran pour qu'il ne soit pas tenté de regarder les résultats précédents
                        cls()

                # Comme on jour toujours, on affiche un mini score au joueur histoire qu'il sache où il en est
                if i_reponse != -1:
                    i_cpt_total = i_cpt_total + 1
                    print("\nRéussi: %d (%2.2f%%)- Faux: %d (%2.2f%%)- Total: %d" %
                          (i_cpt_bon,
                           i_cpt_bon / i_cpt_total * 100,
                           i_cpt_faux,
                           i_cpt_faux / i_cpt_total * 100,
                           i_cpt_total)
                          )
                # Et on recommence au début (while) !

    except EnvironmentError as e:
        logging.exception(e)
        sys.exit(e)

    finally:
        # On note la date de fin pour calculer le temps du test
        date_stop = datetime.now()
        logging.info('Fin du process à %s' % (date_stop.strftime('%x - %X')))

        # On calcule le delta par rapport au temps de démarrage
        d_delta = date_stop - date_start
        logging.info('Temps d\'exécution: %s' % d_delta)

        # On affiche les scores
        print("Nombre de bons: %d - Nombre de faux: %d sur un total de %d" % (i_cpt_bon, i_cpt_faux, i_cpt_total))

        # On note les stats si on n'est pas sorti dès le départ
        if i_cpt_total != 0:
            try:
                # On peaufine le fichier de sortie en rajoutant les infos finales
                with open(s_outfile, 'a') as outfile:
                    outfile.write(
                        "Nombre de bons: %-2d (%2.2f) - Nombre de faux: %-2d (%2.2f) \
                        - Total: %d - Durée de la session de %-15s" %
                        (i_cpt_bon,
                         i_cpt_bon / i_cpt_total * 100,
                         i_cpt_faux,
                         i_cpt_faux / i_cpt_total * 100,
                         i_cpt_total,
                         delta_format(d_delta)
                         )
                    )
            except EnvironmentError as e:
                logging.exception(e)
                sys.exit(e)

        print("Fichier généré avec succès: %s" % s_outfile)


if __name__ == '__main__':
    main()
