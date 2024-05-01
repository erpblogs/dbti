# -*- coding: utf-8 -*-
{
    'name': "Advanced Employee Manager",
    'summary': "Advanced Employee Manager",
    'description': """Advanced Employee Manager""",
    'author': "Dai",
    'website': "savvycom",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'hr', 'custom_hr', 'project', 'hr_skills'],
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/s_hr_employee_views.xml',
        'views/s_res_config_settings.xml',
        # 'views/s_res_config_fullname_employee.xml',
        'views/employee_template.xml',
        'views/s_project_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'advanced_employee_manager/static/fields/**/*',
        ],
    },
}
