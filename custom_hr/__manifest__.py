# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Custom HR',
    'version': '0.1',
    'summary': 'Custom hr',
    'sequence': 10,
    'category': 'Hidden',
    'description': """ 
    Custom HR
    """,
    'data': [
        # 'security/hr_security.xml',
        'security/ir.model.access.csv',
        # 'data/cron.xml',
        'views/hr_job_level_views.xml',
        'views/hr_employee_views.xml',
    ],
    'depends': [
        'hr',
    ],
    'auto_install': False,
    'license': '',
}
