# -*- coding: utf-8 -*-

import sys
from lxml import etree
from pprint import pprint
import json

from openfisca_core import periods

def main(filename):
    parser = etree.XMLParser(remove_blank_text=True, )
    with open(filename, 'r') as f:
        tree = etree.parse(f, parser)

    namespaces = { 'ns1': 'http://nuu.application.i2/' }
    dateDemande = periods.instant(tree.find('//ns1:dateCreationDemande', namespaces=namespaces).text)
    moisDemande = dateDemande.period('month')
    moisDemandeKey = str(moisDemande)

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
                'zone_apl': {
                    moisDemandeKey: None
                }
            }
        }
    }

    situation['familles']['_']['aide_logement'][moisDemandeKey] = None
    print(json.dumps(situation, indent=2))
    return situation


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Vous devez fournir un fichier XML en paramètre.')
        print('Abandon…')
        sys.exit(1)
    main(sys.argv[1])
