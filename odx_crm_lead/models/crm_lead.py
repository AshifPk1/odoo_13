# -*- coding: utf-8 -*-

from odoo import fields, models, api
from datetime import datetime


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    insured_name = fields.Char('Insured Name')
    Date_of_birth = fields.Date('Date Of Birth')
    insurance_type = fields.Selection([('third_party', 'Third Party'), ('comprehensive', 'Comprehensive')],
                                      string="Insurance Type")
    insurence_category = fields.Selection(
        [('motor_insurance', 'Motor Insurance'), ('family_medical', 'Individual / Family Medical Insurance'),
         ('group_medical', 'Group Medical Insurance'), ('business', 'Business Insurance'),
         ('travel', 'Travel Insurance'), ('bike_insurance', 'Bike Insurance'), ('yacht_insurance', 'Yacht Insurance'),
         ('home_insurance', 'Home Insurance')], string='Insurance Category', required=True)
    premium = fields.Char("Premium")
    date = fields.Date('Lead Date')

    country_id = fields.Many2one('res.country', string='Nationality')
    gender = fields.Selection([('male', 'Male'), ('femal', 'female')], string='Gender')
    currently_insured = fields.Boolean("Currently Insured")
    insurance_expiry_date = fields.Date('Insurance Expiry Date')
    first_name = fields.Char("FIrst Name")
    last_name = fields.Char("Last Name")

    # Motor Insurance
    vehicle_id = fields.Many2one("uae.car.valuation",'Vehicle')
    make_id = fields.Many2one('vehicle.brand', string="Make",related='vehicle_id.make_id',store=True)
    model_id = fields.Many2one('vehicle.model', string="Model", related='vehicle_id.model_id',store=True)
    version_id = fields.Many2one('vehicle.version', "Version", related='vehicle_id.version_id',store=True)
    year = fields.Selection([(str(num), num) for num in range(1900, (datetime.now().year) + 100)], 'Year', related='vehicle_id.year',store=True)
    vehicle_value = fields.Float("Vehicle Value")


    brand_new = fields.Boolean("Brand New", help='Is the car is brand new ')
    registered_location = fields.Selection(
        [('dubai', 'Dubai'), ('sharjah', 'Sharjah'), ('abudhabi', 'Abudhabi'), ('rasalkhaimah', 'Rasalkhaimah'),
         ('ajman', 'Ajman'), ('ummalquwain', 'Ummalquwain'), ('fujairah', 'Fujairah')], string='Registerd Location',
        help='Where it will be registered')
    driving_experience = fields.Selection(
        [('0-6 months', '0-6 Months'), ('6-12months', '6-12 Months'), ('1-2 years', '1-2 Years'),
         ('2-3 years', '2-3 Years'), ('3-4 years', '3-4 Years'), ('4-5 years', '4-5 Years'),
         ('5 years and above', '5 Years And Above')], string='Driving Experience ')
    claim_status = fields.Boolean(string="Claim Status", help='Last 12 Months Claim Status')
    years_of_no_claim_certificate = fields.Selection(
        [('no_certificate', 'No Certificate'), ('1_year', '1 Year Proof'), ('2_year', '2 Year Proof'),
         ('3_year_more', '3 Or More Years Proof')], string='Years Of No Claim Certificate ')
    current_repair_type = fields.Selection(
        [('agency_repair', 'Agency Repair'), ('non_agency_repair', 'Non Agency Repair')], string='Current Repair Type')
    specification = fields.Selection([('gcc', 'GCC'), ('non_gcc', 'NON GCC')], string='Specification')
    suage_of_the_vehicle = fields.Selection([('private', 'Private'), ('Public', 'Public')],
                                            string='Usage Of the Vehicle')

    # Individual / Family Medical Insurance

    visa_emirates_id = fields.Many2one('visa.emirates', "Visa Emirates")


    salary = fields.Selection([('above_4000', 'Above 4000'), ('below_4000', 'Below 4000')], string='Salary')
    additional_members_ids = fields.One2many('additional.members', 'insurance_id', string='Additional Members')
    details_of_existing_policy = fields.Char("Details of existing Policy")

    # Group Medical Insurance

    number_of_employees = fields.Integer('Number of employees')

    business_name = fields.Char("Business Name")
    insurance_company_id = fields.Many2one('insurance.company')

    # Business Insurance

    business_insurance_type = fields.Selection(
        [('business_all_risk', 'Business All Risk'), ('contractors_all_risk', 'Contractors All Risk'),
         ('workmen_compensation', 'Workmen Compensation'), ('erection_all_risk', 'Erection All Risk'),
         ('group_health', 'Group Health'),
         ('group_life', 'Group Life'), ('liability_insurance', 'Liability Insurance'),
         ('marine_insurance', 'Marine Insurance'), ('medical_malpractice', 'Medical Malpractice'),
         ('motor_insurance', 'Motor Insurance'), ('personal_accident', 'Personal Accident'),
         ('property_insurance', 'Property Insurance'),
         ('professional_indemnity', 'Professional Indemnity')], String="Business Insurance Type")

    # Travel Insurance

    travelling_date_from = fields.Date('Travelling Date From')
    travelling_date = fields.Date("Travelling Date To")

    travel_type = fields.Selection([('single', 'Single Trip'), ('annual', 'Annual Trip')], String="Travel Type")
    Travelling_to = fields.Selection([('worldwide', 'Worldwide'), ('schengen', 'Schengen'), ('regional', 'Regional'),
                                      ('worldwide_eclude_usa', 'Worldwode Exluding USA & Canada')],
                                     string='Travelling To')
    travelling_with = fields.Selection([('individual', 'Individual'), ('family', 'Family')], string="Travelling With")

    # Bike Insurance

    details_of_bike = fields.Char('Details of the bike')

    # Yacht Insurance

    boat_details = fields.Char('Boat Details')
    engine_details = fields.Char("Engine Details")

    # Home Insurance

    home_status = fields.Selection([('own', 'Own'), ('rental', 'Rental')], string='Home status')
    value_of_buildings = fields.Char("Value Of Buildings")
    value_of_home_contents = fields.Char("Value Of Home Contents")
    value_of_personal_belongings = fields.Char("Value Of Personal Belongings")

    # attachments

    mulika_front = fields.Binary("Mulika Front")
    mulika_back = fields.Binary("Mulika Back")
    driving_license_front = fields.Binary("Driving License Front")
    driving_license_back = fields.Binary("Driving License Back")
    emirates_id_front = fields.Binary("Emirates ID Front")
    emirates_id_back = fields.Binary("Emirates ID Back")
    pass_certificate = fields.Binary("Pass Certificate")
    trade_license = fields.Binary("Trade License")

    passport_copy_front = fields.Binary("Passport Front")
    passport_copy_back = fields.Binary("Passport Back")
    visa_copies = fields.Binary("Visa")
    emirates_id_family_front = fields.Binary("Emirates ID Family Front ")
    emirates_id_family_back = fields.Binary("Emirates ID Family Back ")

    census_list = fields.Binary("Census List")
    trade_license_medical = fields.Binary("Trade License Medical")
    existing_tob = fields.Binary("Existing TOB")

    def action_new_quotation(self):
        res = super(CrmLead, self).action_new_quotation()
        res['context']['default_business_insurance_type'] = self.business_insurance_type
        res['context']['default_insurence_category'] = self.insurence_category
        res['context']['default_vehicle_id'] = self.vehicle_id.id
        return res


class VisaEmirates(models.Model):
    _name = 'visa.emirates'

    name = fields.Char("Name", required=True)


class AdditionalMembers(models.Model):
    _name = 'additional.members'

    name = fields.Char("Name", required=True)
    insurance_id = fields.Many2one('crm.lead', string="Insurance")
    relationship = fields.Selection([('child', 'Child'), ('spouse', 'Spouse'), ('parent', 'Parent')],
                                    string='Relationship')
    gender = fields.Selection([('male', 'Male'), ('femal', 'female')], string='Gender')
    marriage_status = fields.Selection([('married', 'Married'), ('single', 'Single')],
                                       attrs="{'invisible': [('gender', '!=', femal)]}", string='Marriage Status')
    Date_of_birth = fields.Date('Date Of Birth')
    insurance_premium_id = fields.Many2one('insurance.premium',string='Insurance Premium')
    salary = fields.Selection([('above_4000', 'Above 4000'), ('below_4000', 'Below 4000')], string='Salary')


class InsurancePolicy(models.Model):
    _name = 'insurance.policy'

    insurance_company_id = fields.Many2one('res.partner', 'Insurance Company',
                                           domain=[('is_insurance_comapny', '=', True)])
    commission_from = fields.Selection([('broker', 'Broker'), ('company', 'Company')], string='Commisiion From',required=True)
    broker_id = fields.Many2one('res.partner', 'Insurance Broker', domain=[('is_insurance_broker', '=', True)])
    premium_details_ids = fields.One2many('premium.details', 'insurance_policy_id', 'Premium Details')
    commission = fields.Float('Commission %')


class Premiumdetails(models.Model):
    _name = 'premium.details'

    premium_type = fields.Many2one('premium.type', 'Premium Type')
    insurance_policy_id = fields.Many2one('insurance.policy')
    premium = fields.Char('Premium')
    insurance_company_id = fields.Many2one('res.partner', 'Insurance Company',
                                           domain=[('is_insurance_comapny', '=', True)])
    amount = fields.Float('Amount')
