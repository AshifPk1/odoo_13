
from odoo import api, fields, models, _

class PoductTemplate(models.Model):
    _inherit = 'product.template'

    status = fields.Char('Status')
    arabic_name = fields.Char('Arabic Name')
    brand_id = fields.Many2one('product.brand','Brand')
    can_be_sold_online_b2c = fields.Boolean('Can be Sold Online B2C (MAGENTO)')
    can_be_sold_online_b2b = fields.Boolean('Can be Sold Online B2B (MAGENTO)')




class ProductBrand(models.Model):
    _name = 'product.brand'

    name = fields.Char('Brand', required=True)