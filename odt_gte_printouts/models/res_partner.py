from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    street_1 = fields.Char()
    street_2 = fields.Char()
    city_arabic = fields.Char()
    state_arabic = fields.Char()
    country_arabic = fields.Char()
    phone_arabic=fields.Char()
    mobile_arabic=fields.Char()
    # com_register=fields.Char()
    # salesman_id=fields.Char()
    # customer_sequence=fields.Char()
    acc_number_arabic=fields.Char("Account Number Arabic")

class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    acc_number_arabic = fields.Char("Account Number Arabic")
    iban_english = fields.Char("IBAN")
    iban_arabic = fields.Char("IBAN Arabic")
