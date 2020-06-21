# -*- coding: utf-8 -*-


from odoo import models, api, fields, _


class StockMovementsReport(models.TransientModel):
    _name = "stock.movements.report.wiz"

    date_from = fields.Date('From')
    date_to = fields.Date('To')
    categ_id = fields.Many2many('product.category', string='Product Category')
    branch_id = fields.Many2many('res.branch',string='Branch')
    product_id = fields.Many2many('product.product',string='Product')
    product_tag_id = fields.Many2many('product.product.tags',string='Product Tag')
    product_mrp_type_id = fields.Selection([('spare_parts', 'Spare Parts'), ('equipment', 'Equipment'), ('materials', 'Materials')],string='Product MRP Type')
    # product_mrp_type = fields.Selection(
    #     selection=[('spare_parts', 'Spare Parts'), ('equipment', 'Equipment'), ('materials', 'Materials')],
    #     string='Product MRP Type', default='spare_parts')



    def print_report_xlsx(self):
        data = {'date_from': self.date_from,
                'date_to': self.date_to,
                'branch_id': self.branch_id,
                'categ_id': self.categ_id,
                'product_tag_id': self.product_tag_id,
                'product_mrp_type_id': self.product_mrp_type_id,
                'product_id': self.product_id,
                'wiz_id': self.id}
        return self.env.ref('odt_gte_printouts.stock_movements_reports').report_action(self, data=data)

    def print_report(self):
        data = {'date_from': self.date_from,
                'date_to': self.date_to,
                'branch_id': self.branch_id,
                'categ_id': self.categ_id,
                'product_tag_id': self.product_tag_id,
                'product_mrp_type_id': self.product_mrp_type_id,
                'product_id': self.product_id,
                'wiz_id': self.id}
        return self.env.ref('odt_gte_printouts.stock_movements_reports_pdf').report_action(self, data=data)
