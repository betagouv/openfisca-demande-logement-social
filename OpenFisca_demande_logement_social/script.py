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


def getRFR(sourceRFR):
    rfr = {}
    if sourceRFR is not None:
        am1 = sourceRFR.find('ns1:anneeMoins1', namespaces=namespaces)
        if am1 is not None:
            rfr[am1.text] = float(sourceRFR.find('ns1:montantMoins1', namespaces=namespaces).text)
        
        am2 = sourceRFR.find('ns1:anneeMoins2', namespaces=namespaces)
        if am2 is not None:
            rfr[am2.text] = float(sourceRFR.find('ns1:montantMoins2', namespaces=namespaces).text)
    return rfr


def processIndividu(sourceIndividu, famille):
    listeRessourceRecueDemandeur = sourceIndividu.find('ns1:listeRessourceRecue', namespaces=namespaces)
    detailRessources = listeRessourceRecueDemandeur.findall('ns1:detailRessource', namespaces=namespaces)
    demandeurRessources = [getRessource(ressource) for ressource in detailRessources]

    for r in demandeurRessources:
        if r is not None and ('entity' not in r['field'] or r['field']['entity'] == 'famille'):
            name = r['field']['name']
            if name in famille:
                famille[name] += r['value']
            else:
                famille[name] = r['value']

    return {
        #'date_naissance': sourceIndividu.find('ns1:dateNaissance', namespaces=namespaces).text,
        r['field']['name']: r['value'] for r in demandeurRessources if r is not None and 'entity' in r['field'] and r['field']['entity'] == 'individu'
    }


def generateSituation(file):
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(file, parser)

    dateDemande = periods.instant(tree.find('//ns1:dateCreationDemande', namespaces=namespaces).text)
    moisDemande = dateDemande.period('month')
    moisDemandeKey = str(moisDemande)

    last4Years = [moisDemande.offset(offset, 'month')  for offset in range(-12 * 4 + 1, 1)]
    def duplicateMonthly(value):
        return { str(m): value for m in last4Years }

    def expand(entity, additions = {}):
        result = { field: duplicateMonthly(entity[field]) for field in entity }

        for k in additions:
            result[k] = additions[k]

        return result

    details = tree.find('//ns1:personnePhysique', namespaces=namespaces)
    famille = {
        'aide_logement': 0, # Met à zéro l'aide au logement perçu par défaut
    }
    sourceDemandeur = details.find('ns1:demandeur', namespaces=namespaces)
    demandeur = processIndividu(sourceDemandeur, famille)

    rfr = getRFR(sourceDemandeur.find('ns1:revenuFiscal', namespaces=namespaces))

    situation = {
        'individus': {
            'demandeur': expand(demandeur)
        },
        'familles': {
            '_': expand(famille, { 'parents': ['demandeur'] })
        },
        'foyers_fiscaux': {
            '_': {
                'declarants': ['demandeur'],
                'rfr': rfr,
            }
        },
        'menages': {
            '_': {
                'personne_de_reference': ['demandeur'],
                'depcom': duplicateMonthly('75113'),
                'loyer': duplicateMonthly(800),
                'statut_occupation_logement': duplicateMonthly('locataire_hlm'),
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
