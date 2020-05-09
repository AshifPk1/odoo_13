# -*- coding: utf-8 -*-

from odoo import fields, models, api
import base64

class SaleOrder(models.Model):
    _inherit = 'sale.order'


    def send_premium_table(self):
        pdf = self.env.ref('odx_crm_lead.print_premium_table').render_qweb_pdf(self.ids)
        b64_pdf = base64.b64encode(pdf[0])

        ATTACHMENT_NAME = "Insurance Details"
        attachment_id = self.env['ir.attachment'].create({
            'name': ATTACHMENT_NAME,
            'type': 'binary',
            'datas': b64_pdf,
            'display_name': ATTACHMENT_NAME + '.pdf',
            'store_fname': ATTACHMENT_NAME,
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/x-pdf'
        })

        ir_model_data = self.env['ir.model.data']

        try:
            template_id = \
                ir_model_data.get_object_reference('odx_crm_lead', 'email_template_edi_insurance_new')[
                    1]
        except ValueError:
            template_id = False
        ctx = {
            'default_model': 'sale.order',
            'default_res_id': self.id,
            'default_use_template': True,
            'default_template_id': self.env.ref('odx_crm_lead.email_template_edi_insurance_new'),
            'default_composition_mode': 'comment',
            'web_base_url': self.env['ir.config_parameter'].get_param('web.base.url'),
            'mark_so_as_sent': True,
            'custom_layout': "sale.mail_notification_paynow",
            'proforma': self.env.context.get('proforma', False),
            'force_email': True
        }
        template = self.env['mail.template'].browse(template_id)
        html_body = template.body_html
        # text= template.with_context(ctx)._render_template(html_body, 'sale.order',
        #                                                   self.id)

        # for email_recipients in email_to:
        compose = self.env['mail.mail'].with_context(ctx).create({
            'subject': 'Insurance Details',
            'body_html': html_body,
            'email_to': self.partner_id.email,
            'attachment_ids': [(6, 0, [attachment_id.id])] or None,
        })
        compose.send()




