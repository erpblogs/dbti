# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Custom Base Image',
    'version': '0.1',
    'summary': 'Custom image, remove the file image extension ,only use png,jpeg',
    'sequence': 10,
    'category': 'Hidden',
    'description': """ 
    Custom image, remove the file image extension, only use png,jpeg'
    """,
    
    'depends': [
        'base',
    ],
    'data': [
        'views/res_company_views.xml',
        ],

    'auto_install': True,
    'license': '',
}