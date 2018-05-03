# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
from lxml import etree
from pprint import pprint
import json

from openfisca_core import periods

import mapping

namespaces = { 'ns1': 'http://nuu.application.i2/' }

def getRessource(ressourceElement):
    code = ressourceElement.find('ns1:ressource', namespaces=namespaces).get('code')
    montant = ressourceElement.find('ns1:montant', namespaces=namespaces).text

    if not code in mapping.ressource:
        print('Avertissement : Ressource ' + code + ' non prise en compte (montant : ' + montant + ')', file=sys.stderr)
        return None

    return {
        'field': mapping.ressource[code],
        'value': float(montant)
    }

def generateSituation(file):
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(file, parser)

    dateDemande = periods.instant(tree.find('//ns1:dateCreationDemande', namespaces=namespaces).text)
    moisDemande = dateDemande.period('month')
    moisDemandeKey = str(moisDemande)

    details = tree.find('//ns1:personnePhysique', namespaces=namespaces)
    demandeur = details.find('ns1:demandeur', namespaces=namespaces)

    listeRessourceRecueDemandeur = demandeur.find('ns1:listeRessourceRecue', namespaces=namespaces)
    detailRessources = listeRessourceRecueDemandeur.findall('ns1:detailRessource', namespaces=namespaces)

    demandeurRessources = [getRessource(ressource) for ressource in detailRessources]
    demandeurRFR = demandeur.find('ns1:revenuFiscal', namespaces=namespaces)

    last4Years = [moisDemande.offset(offset, 'month')  for offset in range(-12*4+1,1)]
    def vectorData(value):
        return { str(m): value for m in last4Years }

    situation = {
        'individus': {
            'demandeur': {
                'date_naissance': vectorData('1989-02-12'),
            }
        },
        'familles': {
            '_': {
                'parents': ['demandeur'],
                'aide_logement': vectorData(0),
                'aide_logement_base_ressources': vectorData(0),
            }
        },
        'foyers_fiscaux': {
            '_': {
                'declarants': ['demandeur']
            }
        },
        'menages': {
            '_': {
                'personne_de_reference': ['demandeur'],
                'depcom': vectorData('75113'),
                'loyer': vectorData(1000),
                'statut_occupation_logement': vectorData('locataire_hlm'),
            }
        }
    }

    situation['familles']['_']['aide_logement'][moisDemandeKey] = None
    print(json.dumps(situation, indent=2))
    return situation


def extractAideLogement(source):
    result = json.load(source)
    aide_logement = result['familles']['_']['aide_logement']
    valeur = aide_logement[max(aide_logement.keys())]
    print(valeur)
    return valeur


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage\
generate chemin-vers-fichier.xml pour générer le payload utilisable par l‘API Web d‘OpenFisca\
extract chemin-vers-resultat.json pour extraire la valeur calculée pour les aides au logement\
\
En indiquant - à la place du chemin, stdin est utilisé.')
        print('Abandon…')
        sys.exit(1)

    file_path = sys.argv[2]
    if sys.argv[1] == 'extract':
        command = extractAideLogement
    else:
        command = generateSituation

    if file_path == '-':
        command(sys.stdin)
    else:
        with open(file_path, 'r') as f:
            command(f)
