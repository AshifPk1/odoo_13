# -*- coding: utf-8 -*-

from odoo import fields, models, api

class InsurancePremium(models.Model):
    _name = 'insurance.premium'

    name = fields.Char('Name')

    insurance_company_id = fields.Many2one('res.partner', 'Insurance Company',
                                           domain=[('is_insurance_comapny', '=', True)],required=True)

    insurence_category = fields.Selection(
        [('motor_insurance', 'Motor Insurance'), ('family_medical', 'Individual / Family Medical Insurance'),
         ('group_medical', 'Group Medical Insurance'), ('business', 'Business Insurance'),
         ('travel', 'Travel Insurance'), ('bike_insurance', 'Bike Insurance'), ('yacht_insurance', 'Yacht Insurance'),
         ('home_insurance', 'Home Insurance')], string='Insurance Category', required=True)
    insurance_premium = fields.Selection([('fullcover', 'Full Cover'), ('comprehensive', 'Comprehensive')],
                                         string="Insurance Premium")
    vehicle_type = fields.Selection([('saloon', 'Saloon'), ('4_4', '4*4'),('p_up', 'P/UP'), ('motor_cycle', 'Motor Cycle'),
                                     ('trailer_watertanker', 'Trailer & Water Tanker'), ('equipments', 'Equipments'),('bus', 'Bus'),
                                     ('van', 'Van')],
                                      string="Vehicle Type")
    brokarage = fields.Float('Brokarage %')


    premium_product = fields.Many2one('product.product',"Premium Product",required=True)


    premium = fields.Float('Premium')
    tax_id = fields.Many2one('account.tax',String='Tax')
    total = fields.Float("Total",compute="_compute_amount")
    tax_amount = fields.Float('Tax Amount ',compute="_compute_amount")
    car_value = fields.Float('Car value')
    excess = fields.Char('Excess / Deductible')
    repaire_rates = fields.Char('Repaire Rates')
    driver_age  = fields.Selection([('18to25', 'Between 18 years to 25 years'), ('25_above', 'Above 25 years')],
                                      string="Driver Age ")
    date_of_first_registration = fields.Selection([('1st', '1st Year'), ('2nd', '2nd Year'),('3rd', '3rd Year'), ('4th', '4th Year'),('5th', '5th Year'), ('6th', '6th Year and above')],
                                      string="Date of first registration and use")




    # benifits



    loss_dammage = fields.Boolean("Loss or Damage Cover")
    repaire_type = fields.Selection(
        [('agency', 'Agency Repair'),('non_agency', 'Non Agency Repair')],string="Repaire Type")
    third_party_liability = fields.Float("Third Party Liability")
    blood_money = fields.Boolean("Blood Money")
    fire_theft = fields.Boolean("Fire And Cheft Cover")
    storm_flood = fields.Boolean("Storm,Flood")
    natural_perils = fields.Boolean("Natural Perils")
    riot_strike = fields.Boolean("Riot & Strike")
    emergency_medical_expenses = fields.Boolean("Emergency Medical Expenses")
    personal_belongigs = fields.Boolean("Personal Belongings")
    oman_cover = fields.Selection(
        [('orange_card', 'Covered with orange card'),('yes', 'Yes'),('no', 'No')],string="Oman Cover")
    p_off_road = fields.Boolean("P Off-Road Cover")
    road_side_assistance = fields.Boolean("Road Side Assistance")
    ambulance_cover = fields.Boolean("Ambulance Cover")
    aed_500 = fields.Boolean("None Up to AED 5,000")
    aed_3500 = fields.Boolean("None Up to AED 3,500")
    optional_cover = fields.Boolean("Optional Covers")
    driver_cover = fields.Boolean("Driver Cover")
    passanger_cover = fields.Boolean("Passengers Cover")
    rent_a_car = fields.Char("Rent A Car")
    period_of_13_months = fields.Boolean("Perod Of 13 Months")
    geographical_area = fields.Char("Geographical Area")
    guranteed_repairs = fields.Boolean("Guaranteed Repairs")
    accident_break_down = fields.Boolean("Accident And Breakdown Recovery")
    excess_for_windscreen = fields.Char("Excess For Windscreen Damage")

    emergency_road_assistance = fields.Char('Emergency Road Assistance')
    geographical_area_extension = fields.Char("Geographical Area Extension")
    replacement_vehcle = fields.Char("Replacement Vehcle")
    assist_america_for_individual = fields.Char('Assist America For Individual')


    no_of_cylinder = fields.Selection(
        [('4cyl', '4Cyl'),('6cyl', '6Cyl'),('8cyl', '8Cyl'),('12cyl', '12Cyl')],string="No Of Cylinder")
    private_commercial = fields.Selection(
        [('private', 'Private'), ('commercial', 'Commercial')], string="Private/Commercial")

    weight = fields.Selection(
        [('1tonne', '1 Tonne'),('2tonne', '2 Tonne'),('3tonne', '3 Tonne'),('7tonne', '7 Tonne')],string="Weight")
    engin = fields.Selection(
        [('upto200', 'Up To 200 CC'), ('above200', 'Above 200 CC')],
        string="Engin")
    gallons = fields.Selection(
        [('upto200', 'Up To 2000 Gallons'), ('upto5000', 'Up To 5000 Gallons')],
        string="Gallons")
    water_tanker = fields.Boolean('Water Tanker')
    tariler = fields.Boolean("Trailer")
    water_tanker_trailer = fields.Boolean("Water Tanker Trailer")

    light_equipments = fields.Selection(
        [('dumber_agriculture', 'Dumber & Agriculture'), ('forklift', 'Forklift')],
        string="Light Equipments")
    heavy = fields.Boolean('Heavy')

    no_of_passengers = fields.Selection(
        [('upto14', 'Up To 14 Passengers'),('upto26', 'Up To 26 Passengers'),('upto56', 'Up To 56 Passengers')],string="No Of Passengers")


    # indivisual
    package_name = fields.Char("Package Name")
    network = fields.Char("Network")
    additional_members_ids = fields.One2many('additional.members', 'insurance_premium_id', string='Additional Members')



    @api.depends('premium', 'tax_id.amount')
    def _compute_amount(self):
        for record in self:
            if record.tax_id:
                record.tax_amount = record.premium * (record.tax_id.amount/100)
            else:
                record.tax_amount = 0

            record.total = record.premium + record.tax_amount





