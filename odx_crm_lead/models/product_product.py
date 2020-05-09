# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'product.product'

    is_premium = fields.Boolean("premium Product")
    premium_type = fields.Many2one('premium.type','Premium Type')

class PremiumType(models.Model):
    _name = 'premium.type'

    name = fields.Char('Name')