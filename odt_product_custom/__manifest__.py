# -*- coding: utf-8 -*-
{
    'name': "Odt Product Custom",


    'description': """
        add new fields in product
    """,

    'author': "Odootec",
    'website': "http://odootec.com",
    'category': 'Product',
    'version': '0.5',
    'depends': ['base','stock'],
    'data': [
        'security/ir.model.access.csv',
        'view/product_view.xml',
        'view/product_brand.xml'
    ],
}