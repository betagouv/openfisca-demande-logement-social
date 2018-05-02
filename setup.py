#! /usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


setup(
    name = 'OpenFisca-demande-logement-social',
    version = '0.1.0',
    author = 'Beta.gouv.fr',
    author_email = 'thomas.guillet@beta.gouv.fr',
    classifiers = [
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Information Analysis",
        ],
    description = u'Un module de génération de situation OpenFisca à partir d‘un XML de demande de logement social',
    license = 'https://www.fsf.org/licensing/licenses/agpl-3.0.html',
    url = 'https://github.com/betagouv/openfisca-demande-logement-social',
    include_package_data = True,  # Will read MANIFEST.in
    install_requires = [
        'OpenFisca-Core >= 22.0.0, < 23',
        ],
    )
