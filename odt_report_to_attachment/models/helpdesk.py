from odoo import fields, models,_
import base64
from odoo.exceptions import UserError


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    is_project_plan = fields.Boolean('Project Plan (Schedule / Team)')
    is_portal_acces_trainig = fields.Boolean("Portal Access Training")
    is_data_template = fields.Boolean("Data Template")
    is_kick_of_meeting = fields.Boolean("Kick off Meeting")
    is_installtion = fields.Boolean('Installation')
    is_key_user_interview = fields.Boolean('Key User Interview ')
    is_pdd_approval = fields.Boolean('PDD / CDD Review / Approval')
    is_meeting = fields.Boolean('Meeting')
    is_test = fields.Boolean('Test (Functional & Customization)')
    is_opppenig_balance_method = fields.Boolean('Opening Balance Method')
    is_end_user_trainig = fields.Boolean('End User Training')
    is_indoor_skydiving = fields.Boolean('Indoor Skydiving')
    is_cut_of_plan = fields.Boolean('Cut off Plan')
    is_support = fields.Boolean('Support')
    is_meeting_visit = fields.Boolean('Meeting / Visit')
    details_of_work = fields.Text('Details of Work ')

    def generate_attachment(self):
        if self.partner_id:
            if not self.partner_id.email:
                raise UserError(_(
                    'Please define a email to customer'))

        pdf = self.env.ref('odt_report_to_attachment.helpdesk_ticket_report').render_qweb_pdf(self.ids)
        b64_pdf = base64.b64encode(pdf[0])
        attachment = self.env['ir.attachment'].create({
            'name': self.name,
            'type': 'binary',
            'datas': b64_pdf,
            'display_name': self.name + '.pdf',
            'store_fname': self.name,
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/x-pdf'
        })
        sign_template = self.env['sign.template'].create({
            'name': self.name,
            'attachment_id': attachment.id,

        })
        responsible_id = self.env.ref('sign.sign_item_role_customer').id
        type_id = self.env.ref('sign.sign_item_type_signature').id
        sigh = {'0': {'type_id': type_id, 'required': True, 'name': 'Signature', 'option_ids': [],
                      'responsible_id': responsible_id, 'page': '1', 'posX': 0.797, 'posY': 0.731, 'width': 0.2,
                      'height': 0.05}}
        values = {
            'role_id': responsible_id,
            'partner_id': self.partner_id.id
        }
        sign_template.update_from_pdfviewer(template_id=sign_template.id, duplicate=None, sign_items=sigh, name=None)
        wizard = self.env['sign.send.request'].with_context({
            'active_id': sign_template.id
        }).create({'template_id': sign_template.id,
                   'signer_ids': [(0, 0, values)]})
        wizard.send_request()
