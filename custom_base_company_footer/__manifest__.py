# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
# If setup module invoice , it will display footer in "Company create" screen
{
    'name': 'Custom Base Company Footer',
    'version': '0.1',
    'summary': 'Custom display shortage Footer in "Company create" screen',
    'sequence': 10,
    'category': 'Hidden',
    'description': """ 
    Custom display shortage Footer in "Company create" screen
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
