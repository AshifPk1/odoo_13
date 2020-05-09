# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_insurance_comapny = fields.Boolean("Is Insurance Company")
    is_insurance_broker = fields.Boolean("Is Insurance Broker")