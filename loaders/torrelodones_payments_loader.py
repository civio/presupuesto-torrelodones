# -*- coding: UTF-8 -*-
from budget_app.loaders import PaymentsLoader

class TorrelodonesPaymentsLoader(PaymentsLoader):

    def parse_item(self, budget, line):
        # We reuse the parent implementation...
        fields = PaymentsLoader.parse_item(self, budget, line)

        # ...but we modify the programme field.
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

        if budget.year < 2015:
            new_programme = programme_mapping.get(fields['fc_code'])
            if new_programme:
                fields['fc_code'] = new_programme

        return fields