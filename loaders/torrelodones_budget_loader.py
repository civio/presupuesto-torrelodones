# -*- coding: UTF-8 -*-
from budget_app.models import *
from budget_app.loaders import SimpleBudgetLoader
from decimal import *
import csv
import os
import re

class TorrelodonesBudgetLoader(SimpleBudgetLoader):

    def parse_item(self, filename, line):
        # Income data has one less column (missing functional category), so align them
        is_expense = (line[1].strip() == 'G')
        if not is_expense:
            line.insert(3, '')

        return {
            'is_expense': is_expense,
            'is_actual': (line[2].strip() != 'P'),  # Projected (budget) or actual amount (execution)
            'fc_code': line[3].strip(),
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
