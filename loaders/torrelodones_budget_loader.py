# -*- coding: UTF-8 -*-
from budget_app.models import *
from budget_app.loaders import SimpleBudgetLoader
from decimal import *
import csv
import os
import re

class TorrelodonesBudgetLoader(SimpleBudgetLoader):

    def parse_item(self, filename, line):
        # Programme codes have changed in 2015, due to new laws. Since the application expects a code-programme
        # mapping to be constant over time, we are forced to amend budget data prior to 2015.
        # See https://github.com/civio/presupuestos/wiki/La-clasificaci%C3%B3n-funcional-en-las-Entidades-Locales
        programme_mapping = {
            '1340': '1350',     # Protección Civil
            '1550': '1532',     # Vías públicas
            '1620': '1621',     # Recogida, eliminación y tratamiento de residuos 
            '2310': '2210',     # Acción social: personal
            '2311': '2310',     # Acción social: servicios sociales
            '2320': '3371',     # Promoción social: juventud
            '2410': '4331',     # Desarrollo local
            '2411': '2410',     # Fomento del empleo: garantía social
            '3120': '3110',     # Sanidad
            '3130': '3110',     # Acciones públicas relativas a la salud
            '3210': '3230',     # Educación
            '3211': '3231',     # Escuela infantil
            '3300': '3330',     # Administración general de cultura
            '3301': '3340',     # Administración general de cultura: escuela de música
            '3302': '3261',     # Administración general de cultura: escuela de idiomas
            '3320': '3321',     # Bibliotecas
            '3400': '3420',     # Administración general de deportes
            '4400': '4410',     # Administración general del transporte
            '9240': '4910'      # Medios de comunicación social
        }

        # Income data has one less column (missing functional category), so align them
        is_expense = (line[1].strip() == 'G')
        if not is_expense:
            line.insert(3, '')

        # For years before 2015 we check whether we need to amend the programme code
        fc_code = line[3].strip()
        year = re.search('municipio/(\d+)/', filename).group(1)
        if year in ['2011', '2012', '2013', '2014']:
            new_programme = programme_mapping.get(fc_code)
            if new_programme:
                fc_code = new_programme

        return {
            'is_expense': is_expense,
            'is_actual': (line[2].strip() != 'P'),  # Projected (budget) or actual amount (execution)
            'fc_code': fc_code,
            'ec_code': line[4].strip(),
            'item_number': line[4][-2:],            # Last two digits
            'ic_code': '100',                       # We don't have this breakdown, so all goes to catch-all object
            'description': line[5].strip(),
            'amount': self._parse_amount(line[6])
        }


    # We don't have an institutional breakdown in Torrelodones, so we create just a catch-all organism.
    # (We then configure the theme so we don't show an institutional breakdown anywhere.)
    def load_institutional_classification(self, path, budget):
        InstitutionalCategory(  institution='1',
                                section='10',
                                department='100',
                                description='Ayuntamiento de Torrelodones',
                                budget=budget).save()
