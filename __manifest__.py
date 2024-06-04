# -*- coding: utf-8 -*-
{
    'name': "Email Parser",
    'summary': "Module to fetch and parse mail messages",
    'version': '1.0',
    'category': 'Email',
    'depends': ['base', 'website', 'mail', 'sale', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron_data.xml',
        'views/email_parser_fetch_views.xml',
        'views/email_parser_fetch_templates.xml',
        'views/parsed_email_views.xml',
        'views/parsed_email_templates.xml',
        'views/inventory_views.xml',
        'views/inventory_templates.xml',
        'views/inventory_update_views.xml',
        'views/inventory_update_templates.xml',
        # 'views/sale_order_templates.xml',
        # 'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': True,
}
