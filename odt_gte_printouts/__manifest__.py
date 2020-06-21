# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'GTE Printouts',
    'category': 'Localization',
    'description': """

    """,
    'depends': ['base','account','stock','purchase','sale','report_xlsx','product_customs','branch','sale_stock','purchase_stock'],
    'data': [
        'views/res_partner.xml',
        'views/res_company.xml',
        'views/res_bank.xml',
        'views/stock_picking.xml',
        'report/reports.xml',
        'report/account_cash_invoice_template.xml',
        'report/gte_account_move_layout.xml',
        'report/stock_picking_template.xml',
        'report/stock_picking_layout.xml',
        'report/gte_invoice_report.xml',
        'report/account_credit_invoice_template.xml',
        'report/account_credit_note_template.xml',
        'report/account_debit_note_template.xml',
        'report/account_receipt_vouchar_template.xml',
        'report/account_receipt_voucher_layout.xml',
        'report/gte_cash_and_credit_invoice.xml',
        'report/terms_and_condition_template.xml',
        'views/account_move.xml',
        'views/account_payment_term.xml',
        'views/account_payment.xml',
        'wizard/stock_movements_report_wiz_view.xml',
        'report/stock_movements_reports_template.xml'


    ],
}