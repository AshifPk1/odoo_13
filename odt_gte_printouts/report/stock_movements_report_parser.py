# -*- coding: utf-8 -*-

from odoo import api,fields, models


class StockMovementsreports(models.AbstractModel):
    _name = 'report.odt_gte_printouts.stock_movements_reports_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        wiz = self.env['stock.movements.report.wiz'].browse(data.get('wiz_id'))
        date_to = str(wiz.date_to) + ' ' + '23:59:59'
        date_from = str(wiz.date_from) + ' ' + '00:00:00'
        date_today = str(fields.Date.today())

        products_name = ''
        prodcts_catg = ''
        branch_name = ''
        mrp_type = ''
        mrp_type_dict = {'spare_parts':'Spare Parts','equipment':'Equipment','materials':'Materials'}
        product_tag = ''
        domain = [('picking_id.date_done', '<=', date_to), ('picking_id.date_done', '>=', date_from)]
        if wiz.product_id:
            domain.append(('product_id', 'in', wiz.product_id.ids))
            for product in wiz.product_id:
                products_name = products_name + product.name + ","
        if wiz.categ_id:
            domain.append(('product_id.categ_id', 'in', wiz.categ_id.ids))
            for product in wiz.categ_id:
                prodcts_catg = prodcts_catg + product.name + ","
        if wiz.branch_id:
            domain.append(('picking_id.branch_id', 'in', wiz.branch_id.ids))
            for product in wiz.branch_id:
                branch_name = branch_name + product.name + ","
        if wiz.product_mrp_type_id:
            domain.append(('product_id.product_mrp_type', '=', wiz.product_mrp_type_id))
            mrp_type = mrp_type_dict[wiz.product_mrp_type_id]
        if wiz.product_tag_id:
            domain.append(('product_id.division_ids', 'in', wiz.product_tag_id.ids))
            for product in wiz.product_tag_id:
                product_tag = product_tag + product.name + ","

        stock_moves = self.env['stock.move'].search(domain).sorted(key=lambda r: r.picking_id.name)
        sale_order_lines = self.env['sale.order.line'].search(
            [('order_id.date_order', '<=', date_to), ('order_id.date_order', '>=', date_from)]).sorted(
            key=lambda r: r.order_id.name)
        purchase_order_line = self.env['purchase.order.line'].search(
            [('order_id.date_order', '<=', date_to), ('order_id.date_order', '>=', date_from)]).sorted(
            key=lambda r: r.order_id.name)
        products = []
        results = []
        serial_no = 0
        for line in stock_moves:
            if line.product_id not in products:
                products.append(line.product_id)
        for product in products:
            serial_no += 1
            purchase_lines = purchase_order_line.filtered(lambda l: l.product_id == product)
            sale_lines = sale_order_lines.filtered(lambda l: l.product_id == product)

            purchase_qty = sum(purchase_lines.mapped('qty_received'))
            purchase_price = sum(purchase_lines.mapped('price_unit'))
            if len(purchase_lines) != 0:
                average_purchase_price = purchase_price / len(purchase_lines)
            else:
                average_purchase_price = 0
            sale_qty = sum(sale_lines.mapped('qty_delivered'))
            sale_price = sum(sale_lines.mapped('price_unit'))
            if len(sale_lines) != 0:
                avrg_sale_price = round(sale_price / len(sale_lines),2)
            else:
                avrg_sale_price = 0
            qty_spfied_date = product.with_context({'to_date': wiz.date_from}).qty_available
            qty_to_date = product.with_context({'to_date': wiz.date_to}).qty_available
            res = dict(
                (fn, 0.0) for fn in
                ['serial_no', 'default_code', 'name', 'qty_spfied_date', 'purchase_qty', 'sale_qty', 'qty_available',
                 'standard_price', 'avrg_sale_price'])
            res['serial_no'] = serial_no
            res['default_code'] = product.default_code
            res['name'] = product.name
            res['qty_spfied_date'] = qty_spfied_date
            res['purchase_qty'] = purchase_qty
            res['sale_qty'] = sale_qty
            res['qty_available'] = qty_to_date
            res['standard_price'] = round(product.standard_price,2)
            res['avrg_sale_price'] = avrg_sale_price
            results.append(res)

        data = {
            'date_to': wiz.date_to,
            'date_from': wiz.date_from,
            'results': results,
            'doc_ids': self.ids,
            'products_name':products_name,
            'prodcts_catg':prodcts_catg,
            'branch_name': branch_name,
            'mrp_type': mrp_type,
            'product_tag': product_tag,
            'date_today':date_today

        }
        return data
