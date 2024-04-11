# -*- coding: utf-8 -*-
{
    'name': "Custom Website",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "Quangtv",
    'website': "savvycom",

    'category': 'web',
    'version': '0.1',
    'depends': ['base', 'portal', 'auth_signup'],

    # always loaded
    'data': [
        # 'security/base_group.xml',
        # 'security/base_security.xml',
        # 'security/ir.model.access.csv',
        
        # datas
        # 'data/company.xml', 
        # 'data/website_data.xml',
        
        # view
        
        # layout
        'views/web_layout.xml',
        # 'views/contactus_layout.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            # 'custom_web/static/src/scss/lib/custom_bootstrap.scss',
            # 'custom_web/static/src/scss/style.scss',
            'custom_web/static/src/scss/login_layout.scss',
        ],
        'web._assets_primary_variables': [
            ('before', 'web/static/src/scss/primary_variables.scss',  'custom_web/static/src/scss/primary_variables.scss',),
        ],
        # 'web._assets_secondary_variables': [
        #     ('before', 'web/static/src/scss/secondary_variables.scss', 'custom_web/static/src/scss/secondary_variables.scss'),
        # ],
        'web._assets_common_styles': [
            'custom_web/static/src/scss/fonts.scss',
        ],
    }
}

