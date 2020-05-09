from odoo import fields, models


class PriceListCreate(models.Model):
    _inherit = 'product.pricelist'

    bank_details = fields.Text(string="Bank Details")
