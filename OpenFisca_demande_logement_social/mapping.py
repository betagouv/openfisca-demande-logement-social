# -*- coding: utf-8 -*-

# The default entity is famille

ressource = {
    'AAH': { # Allocation d'adulte handicapé
        'name': 'aah',
        'entity': 'individu'
    },
    'AEEH': { # Allocation d'éducation d'enfant handicapé
        'name': 'aeeh',
    },
    'AF': { # Allocations familiales
        'name': 'af',
    },
#    'AJPP': { # Allocation journalière de présence parentale
#        'name': 'ajpp',
#    },
    'AMV': { # Allocation de minimum vieillesse
        'name': 'aspa',
    },
#    'AUT': { # Autre (hors APL ou AL)
#        'name': 'aut',
#    },
    'BE': { # Bourse étudiant
        'name': 'bourse_enseignement_sup',
        'entity': 'individu'
    },
    'CHO': { # Allocation chômage
        'name': 'chomage_brut',
        'entity': 'individu'
    },
    'PAJE': { # Allocation jeune enfant
        'name': 'paje_base',
    },
    'PAR': { # Pension alimentaire reçue
        'name': 'pensions_alimentaires_percues',
        'entity': 'individu'
    },
    'PAV': { # Pension alimentaire versée
        'name': 'pensions_alimentaires_versees_individu',
        'entity': 'individu'
    },
    'PINV': { # Pension invalidité
        'name': 'pensions_invalidite',
        'entity': 'individu'
    },
    'RET': { # Retraite
        'name': 'retraite_nette',
        'entity': 'individu'
    },
    'RSA': {
        'name': 'rsa'
    },
    'SAL': { # ou revenu d’activité
        'name': 'salaire_de_base',
        'entity': 'individu'
    },
}
