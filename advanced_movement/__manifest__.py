# -*- coding: utf-8 -*-
{
    'name': "Advanced Movement",
    'summary': "Advanced Movement",
    'description': """Advanced Movement""",
    'author': "Tu_Dai",
    'website': "savvycom",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'survey', 'mail', 'hr', 'custom_hr', 'advanced_employee_manager'],
    # always loaded
    'data': [
        'security/hr_movement.xml',
        'security/ir.model.access.csv',
        'views/hr_movement_views.xml',
        'views/s_exit_interview_record.xml',
        'data/approval_role_data.xml',
        'data/approval_flow_data.xml',
        'wizard/movement_stage_views.xml',
        'views/approval_flow_views.xml',
        'views/approval_role_views.xml',

        'views/s_job_rotation_request.xml',
        'views/movement_menu_viewx.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'advanced_movement/static/src/css/my_one2many_field_class.css',
        ]
    },
    'installed': True,
    'auto_install': False,
}
