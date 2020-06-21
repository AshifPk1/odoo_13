from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    street_1 = fields.Char()
    street_2 = fields.Char()
    city_arabic = fields.Char()
    state_arabic = fields.Char()
    country_arabic = fields.Char()
    phone_arabic=fields.Char()
