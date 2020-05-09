{
    'name': 'Odx Crm Lead',
    'version': '1.0',
    'category': 'crm',
    'description': """
        Add fields in crm_lead
     """,
    'author': "Odox Softhub",
    'website': "http://odoxsofthub.com",
    'depends': ['base', 'crm', 'odx_uae_car_valuation', 'sale','sale_crm','product','account'],
    'data': [
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'data/email_template.xml',
        'views/crm_lead_view.xml',
        'views/insurance_master.xml',
        'views/sale_order_view.xml',
        'views/res_partner_view.xml',
        'views/product_view.xml',
        # 'views/insurance_policy.xml',
        'report/premium_table_template.xml',
        'report/report.xml',
        # 'views/premium_type.xml',
        'views/insurance_premium_view.xml'

    ],
}
