from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    print = fields.Selection([
        ('cash_invoice', 'Cash Invoice'),
        ('credit_invoice', 'Credit Invoice'),],string='Print Type',
         required=True, readonly=0,default='cash_invoice')
    po=fields.Char(string='P.O.')
    # branch_id=fields.Char(string="Branch")

