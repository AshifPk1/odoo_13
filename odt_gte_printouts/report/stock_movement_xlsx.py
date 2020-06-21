from odoo import models, fields
import datetime
import io
import base64

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def excel_style(row, col):
    """ Convert given row and column number to an Excel-style cell name. """
    result = []
    while col:
        col, rem = divmod(col - 1, 26)
        result[:0] = LETTERS[rem]
    return ''.join(result) + str(row)


class StoreReport(models.AbstractModel):
    _name = 'report.stock.report.report.xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, wiz):

        date_to = str(wiz.date_to) + ' ' + '23:59:59'
        date_from = str(wiz.date_from) + ' ' + '00:00:00'
        products = ''
        prodcts_catg = ''
        branch_name = ''
        mrp_type = ''
        product_tag = ''
        mrp_type_dict = {'spare_parts': 'Spare Parts', 'equipment': 'Equipment', 'materials': 'Materials'}

        domain = [('picking_id.date_done', '<=', date_to), ('picking_id.date_done', '>=', date_from)]
        if wiz.product_id:
            domain.append(('product_id', 'in', wiz.product_id.ids))
            for product in wiz.product_id:
                products = products + product.name + ","
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

        heading_format = workbook.add_format({'align': 'center',
                                              'valign': 'vcenter',
                                              'bold': True, 'size': 15,
                                              # 'bg_color': '#0077b3',
                                              })
        sub_heading_format = workbook.add_format({'align': 'center',
                                                  'valign': 'vcenter',
                                                  'bold': True, 'size': 11,
                                                  # 'bg_color': '#0077b3',
                                                  # 'font_color': '#FFFFFF'
                                                  })
        sub_heading_format_company = workbook.add_format({'align': 'left',
                                                          'valign': 'left',
                                                          'bold': True, 'size': 11,
                                                          # 'bg_color': '#0077b3',
                                                          # 'font_color': '#FFFFFF'
                                                          })

        col_format = workbook.add_format({'valign': 'left',
                                          'align': 'left',
                                          'bold': True,
                                          'size': 10,
                                          'font_color': '#000000'
                                          })
        data_format = workbook.add_format({'valign': 'center',
                                           'align': 'center',
                                           'size': 10,
                                           'font_color': '#000000'
                                           })
        line_format = workbook.add_format({'align': 'center',
                                           'valign': 'vcenter',
                                           'size': 1,
                                           'bg_color': '#9A9A9A',
                                           })

        col_format.set_text_wrap()
        worksheet = workbook.add_worksheet('Stock Movements Report')
        worksheet.set_column('A:A', 10)
        worksheet.set_column('B:B', 10)
        worksheet.set_column('C:C', 20)
        worksheet.set_column('D:D', 30)
        worksheet.set_column('E:E', 40)
        worksheet.set_column('F:F', 35)
        worksheet.set_column('G:G', 30)
        worksheet.set_column('H:H', 35)
        worksheet.set_column('I:I', 30)
        row = 1
        worksheet.set_row(1, 20)
        starting_col = excel_style(row + 1, 1)
        ending_col = excel_style(row + 1, 7)
        from_date = datetime.datetime.strptime(str(wiz.date_from), '%Y-%m-%d').strftime('%d/%m/%Y')
        to_date = datetime.datetime.strptime(str(wiz.date_to), '%Y-%m-%d').strftime('%d/%m/%Y')
        date_today = str(fields.Date.today())
        worksheet.merge_range('%s:%s' % (starting_col, ending_col),
                              "STOCK MOVEMENT REPORT ", heading_format)

        worksheet.merge_range(row + 1, 0, row + 1, 2, "Print Date : " + " " + date_today, sub_heading_format_company)
        worksheet.merge_range(row + 2, 0, row + 2, 2, "Date From : " + " " + from_date, sub_heading_format_company)
        worksheet.merge_range(row + 3, 0, row + 3, 2, "Date To : " + " " + to_date, sub_heading_format_company)
        row += 4
        starting_col = excel_style(row + 1, 1)
        ending_col = excel_style(row + 1, 7)
        if wiz.branch_id or wiz.categ_id or wiz.product_id or wiz.product_tag_id or wiz.product_mrp_type_id:
            worksheet.merge_range('%s:%s' % (starting_col, ending_col),
                                  "Filter By ", heading_format)
        if wiz.branch_id:
            worksheet.merge_range(row + 1, 0, row + 1, 3, "Branch :  " + " " + branch_name, sub_heading_format_company)
            row += 1
        if wiz.categ_id:
            worksheet.merge_range(row + 1, 0, row + 1, 3, "Product Category : " + " " + prodcts_catg,
                                  sub_heading_format_company)
            row += 1
        if wiz.product_id:
            worksheet.merge_range(row + 1, 0, row + 1, 3, "Products : " + " " + products, sub_heading_format_company)
            row += 1
        if wiz.product_tag_id:
            worksheet.merge_range(row + 1, 0, row + 1, 3, "Product tag : " + " " + product_tag,
                                  sub_heading_format_company)
            row += 1
        if wiz.product_mrp_type_id:
            worksheet.merge_range(row + 1, 0, row + 1, 3, "Product MRP Type : " + " " + mrp_type,
                                  sub_heading_format_company)
            row += 1
        buf_image = io.BytesIO(base64.b64decode(self.env.user.company_id.logo))

        # worksheet.insert_image('G3', "any_name.png", {'image_data': buf_image, 'x_scale': 0.5, 'y_scale': 0.35})
        row += 1

        worksheet.merge_range(row, 3, row, 6,
                              "QTY ", heading_format)
        worksheet.merge_range(row, 7, row, 8,
                              "VALUE ", heading_format)
        row += 1
        worksheet.write(row, 0, "SL No", sub_heading_format)
        worksheet.write(row, 1, "ITEM CODE", sub_heading_format)
        worksheet.write(row, 2, "ITEM NAME", sub_heading_format)
        worksheet.write(row, 3, "OPENING STOCK" + " " + from_date, sub_heading_format)
        worksheet.write(row, 4, "PURCHSED QTY" + " " + from_date + " " + "To" + " " + to_date, sub_heading_format)
        worksheet.write(row, 5, "SOLD QTY" + " " + from_date + " " + "To" + " " + to_date, sub_heading_format)
        worksheet.write(row, 6, "CLOSING STOCK " + " " + to_date, sub_heading_format)
        worksheet.write(row, 7, "ITEM COST PRICE(LANDED COST)", sub_heading_format)
        worksheet.write(row, 8, "ITEM AVERAGE SELLING PRICE", sub_heading_format)
        row += 1
        sl_no = 0
        products = []
        for line in stock_moves:
            if line.product_id not in products:
                products.append(line.product_id)
        for product in products:
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
            qty_date_to = product.with_context({'to_date': wiz.date_to}).qty_available
            sl_no += 1
            worksheet.write(row, 0, sl_no, data_format)
            worksheet.write(row, 1, product.default_code, data_format)
            worksheet.write(row, 2, product.name, data_format)
            worksheet.write(row, 3, qty_spfied_date, data_format)
            worksheet.write(row, 4, purchase_qty, data_format)
            worksheet.write(row, 5, sale_qty, data_format)
            worksheet.write(row, 6, qty_date_to, data_format)
            worksheet.write(row, 7, round(product.standard_price,2), data_format)
            worksheet.write(row, 8, avrg_sale_price, data_format)
            row += 1
