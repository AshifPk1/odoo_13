from odoo import fields, models, _
import base64
from odoo.exceptions import UserError


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    sdr_ids = fields.One2many('sdr.generate', 'ticket_id', string='SDRs')

    def generate_attachment(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Create SDR'),
            'res_model': 'sdr.generate.wiz',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_name': self.name + '/' + self.ticket_number_val,
                'default_partner_ids': [(6, 0, [self.partner_id.id if self.partner_id else False])],
                'default_type': 'ticket',
                'default_ticket_id': self.id,
                'default_number': 'K' + '/' + self.ticket_number_val,
                'default_user_id': self.user_id.id,
            }
        }


class SDRGenerate(models.Model):
    _name = 'sdr.generate'
    _description = 'Generate SDR'

    name = fields.Char('Name', required=True)
    ticket_id = fields.Many2one('helpdesk.ticket', string='Ticket')
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    date = fields.Date('Date', required=True, index=True, default=fields.Date.context_today)
    user_id = fields.Many2one('res.users', string='User')
    is_project_plan = fields.Boolean('Project Plan (Schedule / Team)')
    is_portal_access_training = fields.Boolean("Portal Access Training")
    is_data_template = fields.Boolean("Data Template")
    is_kick_of_meeting = fields.Boolean("Kick off Meeting")
    is_installation = fields.Boolean('Installation')
    is_key_user_interview = fields.Boolean('Key User Interview ')
    is_pdd_approval = fields.Boolean('PDD / CDD Review / Approval')
    is_meeting = fields.Boolean('Meeting')
    is_test = fields.Boolean('Test (Functional & Customization)')
    is_opening_balance_method = fields.Boolean('Opening Balance Method')
    is_end_user_training = fields.Boolean('End User Training')
    is_indoor_skydiving = fields.Boolean('Indoor Skydiving')
    is_cut_of_plan = fields.Boolean('Cut off Plan')
    is_support = fields.Boolean('Support')
    is_meeting_visit = fields.Boolean('Meeting / Visit')
    details_of_work = fields.Text('Details of Work ')
    sign_request_id = fields.Many2one('sign.request', string='Sign Request')
    sign_state = fields.Selection(related='sign_request_id.state', store=True)
    attachment_id = fields.Many2one('ir.attachment', 'SDR')
    number = fields.Char('Ticket/Task No')
    in_time = fields.Float('In Time')
    out_time = fields.Float('Out Time')

    def generate_attachment(self):
        if self.partner_id:
            if not self.partner_id.email:
                raise UserError(_(
                    'Please define a email to customer "%s"') % self.partner_id.name)
        pdf = self.env.ref('odt_report_to_attachment.sdr_attachment_report').render_qweb_pdf(self.ids)
        b64_pdf = base64.b64encode(pdf[0])
        attachment = self.env['ir.attachment'].sudo().create({
            'name': self.name,
            'type': 'binary',
            'datas': b64_pdf,
            'display_name': self.name + '.pdf',
            'store_fname': self.name,
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/x-pdf'
        })
        sign_template = self.env['sign.template'].sudo().create({
            'name': self.name + '/' + self.number,
            'attachment_id': attachment.id,

        })
        responsible_id = self.sudo().env.ref('sign.sign_item_role_customer').id
        type_id = self.sudo().env.ref('sign.sign_item_type_signature').id
        sigh = {'0': {'type_id': type_id, 'required': True, 'name': 'Signature', 'option_ids': [],
                      'responsible_id': responsible_id, 'page': '1', 'posX': 0.797, 'posY': 0.870, 'width': 0.2,
                      'height': 0.05}}
        sign_template.sudo().update_from_pdfviewer(template_id=sign_template.id, duplicate=None, sign_items=sigh, name=None)
        wizard = self.env['sign.send.request'].with_context({
            'active_id': sign_template.id
        }).sudo().create({'template_id': sign_template.id,
                   'signer_ids': [(0, 0, {'role_id': responsible_id, 'partner_id': self.partner_id.id})]})
        wizard.sudo().send_request()
        sign_request = self.env['sign.request'].sudo().search([('template_id', '=', sign_template.id)])
        self.attachment_id = sign_template.sudo().attachment_id.id
        if sign_request:
            self.sign_request_id = sign_request.id

    def view_document(self):
        if self.sign_request_id:
            return self.sign_request_id.go_to_document()
        else:
            raise UserError(_("No SDR attached in Sign Request"))
