from odoo import models, fields


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    branch_id=fields.Char('Branch')