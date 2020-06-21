from odoo import fields, models, api


class SignTemplate(models.Model):
    _inherit = 'sign.template'

    is_document_added = fields.Boolean("Document Added")


class SignRequest(models.Model):
    _inherit = 'sign.request'

    @api.onchange('state')
    def on_change_state(self):
        if self.state == 'signed':
            self.template_id.is_document_added = True
        else:
            self.template_id.is_document_added = False


class ResUsers(models.Model):
    _inherit = 'res.users'

    sign_signature = fields.Binary(string="Digital Signature", groups=False)
