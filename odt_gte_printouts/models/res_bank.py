from odoo import models, fields


class ResBank(models.Model):
    _inherit = 'res.bank'

    name_ar=fields.Char("Arabic Name")
    check_name_en=fields.Char("Check Name English")
    check_name_ar = fields.Char("Check Name Arabic")

