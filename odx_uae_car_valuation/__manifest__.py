{
    'name': 'UAE Car Valuation',
    'version': '1.0',
    'category': 'Fleet',
    'description': """
        UAE Car Valuation
     """,
    'author': "Odox Softhub",
    'website': "http://odoxsofthub.com",
    'depends': ['base','crm'],
    'data': [
              'security/ir.model.access.csv',
             'views/uae_car_valuation_view.xml',
            'views/vehicle_brand_view.xml',
             'views/model_view.xml',
              # 'views/vehicle_insurance_view.xml',
              # 'views/vehicle_type_view.xml',
              'views/vehicle_version.xml',
              # 'views/insurance_payment_view.xml',

    ],
}