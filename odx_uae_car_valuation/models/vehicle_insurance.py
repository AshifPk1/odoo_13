from odoo import fields, models, api

class VehicleInsurance(models.Model):
    _name = 'vehicle.insurance'

    name = fields.Char(string="Name", required=True)

class InsurancePayment(models.Model):
    _name = 'insurance.payment'

    insurance_company_id = fields.Many2one('vehicle.insurance', string="Insurance Company" , required=True)
    tariff_ids = fields.One2many('vehicle.tariff','insurance_payment_id',String='Tariff')
    date = fields.Date('Date')
    state = fields.Selection([('draft', 'Draft'),('confirmed', 'Confirmed')],string="State",  default='draft',)
    insurance_type = fields.Selection([('third_party', 'Third Party'), ('full_cover', 'Full Cover')], string="Insurance Type")

    @api.depends('insurance_company_id')
    def name_get(self):
        res = []
        for record in self:
            if record.insurance_company_id:
                name = record.insurance_company_id.name
            res.append((record.id, name))
        return res

    def confirm(self):
        self.write({'state': 'confirmed'})


class VehicleType(models.Model):
    _name = 'vehicle.type'

    name = fields.Char(string="Type of Vehicle")
    attribute_value_id = fields.Many2one('tariff.attribute', string='Attribute Name')


class VehicleTariff(models.Model):
    _name = 'vehicle.tariff'

    type_of_vehicle_id = fields.Many2one('vehicle.type',string="Type of Vehicle")
    attribute_value_id = fields.Many2one('tariff.attribute', string='Attribute Name' , related='type_of_vehicle_id.attribute_value_id' , store=True)
    value = fields.Char(string='Value')
    premium = fields.Float(string="Premium Amount")
    agency_repair = fields.Float(string="Agency Repair(Min Rate %)")
    non_agency_repair = fields.Float(string="Non-Agency Repair(Min Rate %)")
    insurance_payment_id = fields.Many2one('insurance.payment', 'Insurance Payment')
    ownership = fields.Selection([('private', 'Private'), ('commercial', 'Commercial')], string="Private/Commercial")


class TariffAttribute(models.Model):
    _name = 'tariff.attribute'

    name = fields.Char('Attributes', required=True)

