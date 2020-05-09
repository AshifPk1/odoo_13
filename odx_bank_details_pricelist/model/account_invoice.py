from odoo import fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    pricelist_id = fields.Many2one('product.pricelist', string="Price List")
