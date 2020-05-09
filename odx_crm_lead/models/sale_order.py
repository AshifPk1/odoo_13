# -*- coding: utf-8 -*-

from odoo import fields, models, api
from datetime import datetime


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    business_insurance_type = fields.Selection(
        [('business_all_risk', 'Business All Risk'), ('contractors_all_risk', 'Contractors All Risk'),
         ('workmen_compensation', 'Workmen Compensation'), ('erection_all_risk', 'Erection All Risk'),
         ('group_health', 'Group Health'),
         ('group_life', 'Group Life'), ('liability_insurance', 'Liability Insurance'),
         ('marine_insurance', 'Marine Insurance'), ('medical_malpractice', 'Medical Malpractice'),
         ('motor_insurance', 'Motor Insurance'), ('personal_accident', 'Personal Accident'),
         ('property_insurance', 'Property Insurance'),
         ('professional_indemnity', 'Professional Indemnity')], String="Business Insurance Type")

    insurence_category = fields.Selection(
        [('motor_insurance', 'Motor Insurance'), ('family_medical', 'Individual / Family Medical Insurance'),
         ('group_medical', 'Group Medical Insurance'), ('business', 'Business Insurance'),
         ('travel', 'Travel Insurance'), ('bike_insurance', 'Bike Insurance'), ('yacht_insurance', 'Yacht Insurance'),
         ('home_insurance', 'Home Insurance')], string='Insurance Category')

    vehicle_type = fields.Selection(
        [('saloon', 'Saloon'), ('4_4', '4*4'), ('p_up', 'P/UP'), ('motor_cycle', 'Motor Cycle'),
         ('trailer_watertanker', 'Trailer & Water Tanker'), ('equipments', 'Equipments'), ('bus', 'Bus'),
         ('van', 'Van')],
        string="Vehicle Type")
    insurance_premium_table_ids = fields.One2many('insurance.premium.table', 'saleorde_id', "Insurance Premium Table")

    visible_insurance_company = fields.Boolean('Company visible')
    vehicle_id = fields.Many2one("uae.car.valuation", 'Vehicle')


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    premium = fields.Float('Premium')
    commission = fields.Float('Commission %')

    price_unit = fields.Float('Unit Price', required=True, digits='Product Price', compute="_compute_price_unit",
                              default=0.0)

    @api.depends('premium', 'commission')
    def _compute_price_unit(self):
        for record in self:
            record.price_unit = record.premium * record.commission / 100


class InsurancePremiumTable(models.Model):
    _name = 'insurance.premium.table'

    insurance_company_id = fields.Many2one('res.partner', 'Insurance Company',
                                           domain=[('is_insurance_comapny', '=', True)])
    insurance_premium_id = fields.Many2one('insurance.premium', 'Insurance Policy')
    amount = fields.Float("Premium")
    tax_id = fields.Many2one('account.tax', "Tax")
    saleorde_id = fields.Many2one('sale.order')
    brokarage = fields.Float('Brokarage %')

    tax_amount = fields.Float('Tax', compute="_compute_total")
    total_amount = fields.Float('Total', compute="_compute_total")

    @api.depends('amount', 'tax_id.amount')
    def _compute_total(self):
        for record in self:
            if record.tax_id:
                record.tax_amount = record.amount * (record.tax_id.amount / 100)
            else:
                record.tax_amount = 0
            record.total_amount = record.amount + record.tax_amount

    @api.onchange('insurance_premium_id')
    def onchange_insurance_premium_id(self):
        if self.insurance_premium_id:
            self.amount = self.insurance_premium_id.premium
            self.brokarage = self.insurance_premium_id.brokarage
            if self.insurance_premium_id.tax_id:
                self.tax_id = self.insurance_premium_id.tax_id.id

    def confirm_premium(self):
        if self.insurance_premium_id:
            lines = {
                'product_id': self.insurance_premium_id.premium_product.id,
                'premium': self.amount,
                'commission': self.brokarage
            }
            if self.saleorde_id:
                self.saleorde_id.update({
                    'visible_insurance_company': True,
                    'partner_invoice_id': self.insurance_company_id.id,
                    'order_line': [(0, 0, lines)],
                })
