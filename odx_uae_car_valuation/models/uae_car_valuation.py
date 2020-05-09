# -*- coding: utf-8 -*-

from odoo import fields, models, api
from datetime import datetime


class UaeCarValuation(models.Model):
    _name = 'uae.car.valuation'

    name = fields.Char(compute="_compute_vehicle_name", store=True)
    make_id = fields.Many2one('vehicle.brand', string="Make", related='version_id.make_id',store=True)
    model_id = fields.Many2one('vehicle.model', string="Model",related='version_id.model_id',store=True)
    version_id = fields.Many2one('vehicle.version',"Version" , required=True)
    estimated_price_new_min = fields.Float("Minimum Price")
    estimated_price_new_max = fields.Float("Maximum Price")
    estimated_price_old_min = fields.Float("Current Value Minimum")
    estimated_price_old_max = fields.Float("Current Value Maximum")
    year = fields.Selection([(str(num), num) for num in range(1900, (datetime.now().year) + 100)], 'Year')
    version_type_id = fields.Many2one('vehicle.version.type')
    no_of_cylinder = fields.Char("No Of Cylinder")
    no_of_doors = fields.Char("No Of Doors")
    no_of_seats = fields.Char("No Of Seats")
    version_category = fields.Many2one('vehicle.version.category', "Category")
    vehicle_type = fields.Selection(
        [('saloon', 'Saloon'), ('4_4', '4*4'), ('p_up', 'P/UP'), ('motor_cycle', 'Motor Cycle'),
         ('trailer_watertanker', 'Trailer & Water Tanker'), ('equipments', 'Equipments'), ('bus', 'Bus'),
         ('van', 'Van')],
        string="Vehicle Type",required=True)

    @api.depends('make_id.name', 'model_id.name', 'version_id.name')
    def _compute_vehicle_name(self):
        for record in self:
            record.name = (record.make_id.name or '') + '/' + (
                                  record.version_id.name if record.version_id else '' or '')


class VehicleBrand(models.Model):
    _name = 'vehicle.brand'

    name = fields.Char("Make", required=True)


class VehicleModel(models.Model):
    _name = 'vehicle.model'

    name = fields.Char("Model", required=True)
    make_id = fields.Many2one('vehicle.brand', string="Make")

class VehicleVersion(models.Model):
    _name = 'vehicle.version'

    name = fields.Char('Name', compute="_compute_vehicle_name", store=True)
    version = fields.Char('Version' , required=True)
    make_id = fields.Many2one('vehicle.brand', string="Make", related='model_id.make_id',store=True)
    model_id = fields.Many2one('vehicle.model', string="Model")
    version_type_id = fields.Many2one('vehicle.version.type')
    no_of_cylinder = fields.Char("No Of Cylinder")
    no_of_doors = fields.Char("No Of Doors")
    no_of_seats = fields.Char("No Of Seats")
    version_category = fields.Many2one('vehicle.version.category',"Category")


    @api.depends('version', 'model_id.name')
    def _compute_vehicle_name(self):
        for record in self:
            record.name = (record.model_id.name or '') + '/' + (record.version or '')

class VehicleVersionType(models.Model):
    _name = 'vehicle.version.type'

    name = fields.Char("Name")

class VehicleVersionCategory(models.Model):
    _name = 'vehicle.version.category'

    name = fields.Char("Name")




