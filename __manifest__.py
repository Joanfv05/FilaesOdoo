# -*- coding: utf-8 -*-
{
    'name': "Filaes Sant Jordi",
    'summary': "Gestión de filaes y montepios para la Asociación de Sant Jordi",
    'description': """
Este módulo permite gestionar las filaes de la Asociación de Sant Jordi, incluyendo:
- Gestión de socios
- Gestión de filaes
- Registro histórico de altas y bajas
- Control de montepios (aportaciones)
    """,
    'author': "Joan",
    'website': "https://es.restaurantguru.com/Telexurro-Spain/reviews?bylang=1",
    'category': 'Asociaciones',
    'version': '1.0',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/socies_views.xml',
        'views/filaes_views.xml',
        'views/historic_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'installable': True,
}
