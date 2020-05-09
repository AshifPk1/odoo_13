{
    'name': 'Bank Details With Pricelist',
    'version': '1.0',
    'category': 'Account',
    'description': """
        Add Bank Details in Invoice With Pricelist
     """,
    'depends': ['base','account'],
    'data': [
             'views/product_pricelist_view.xml',
             'views/account_invoice.xml',
             'report/invoice_report_inherit.xml'
    ],
}