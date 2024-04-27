# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Custom Base Company Footer',
    'version': '0.1',
    'summary': 'Custom format for email and phone',
    'sequence': 10,
    'category': 'Hidden',
    'description': """ 
    Custom format for email and phone
    """,
    
    'depends': [
        'base_setup','mail',
    ],
    'data': [
        'views/res_company_views.xml',
    ],

    'auto_install': False,
    'license': '',
}