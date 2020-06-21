from odoo import models, fields

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    customer_order_number = fields.Char("Customer Order Number")