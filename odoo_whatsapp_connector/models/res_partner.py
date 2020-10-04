# See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _, api
from odoo.exceptions import UserError, ValidationError
import requests
import json
import re


class Partner(models.Model):
    """Inherit Partner."""

    _inherit = "res.partner"

    is_whatsapp_number = fields.Boolean(string="Is Whatsapp Number",
                                        default=False)
    chat_id = fields.Char(
        string='Chat Id',
    )

    def _formatting_mobile_number(self):
        for rec in self:
            module_rec = self.env['ir.module.module'].search_count([
                ('name', '=', 'phone_validation'),
                ('state', '=', 'installed')])
            return module_rec and re.sub("[^0-9]", '', rec.mobile) or \
                str(rec.country_id.phone_code
                    ) + rec.mobile

    def check_whatsapp_number_response(self, company):
        """Method to check mobile is on whatsapp."""
        number_dict = {}
        if self.mobile:
            mobile = self._formatting_mobile_number()
            url_path = company.api_url + \
                str(company.instance_no) + '/checkPhone' + '?token=' \
                + company.api_token + '&phone=' \
                + mobile
            request_meeting = requests.get(
                url_path, headers={
                    'Content-Type': 'application/json'})
            number_dict = json.loads(request_meeting.text)
        return number_dict

    def check_number_whatsapp(self):
        """Check Partner Mobile."""
        for rec in self:
            company_id = self.env.user.company_id
            if company_id and not company_id.authenticate:
                raise UserError(_('Whatsapp Authentication Failed.'
                                  ' Configure Whatsapp Configuration'
                                  ' in company setting.'))
            company_id.check_auth()
            number_dict = rec.check_whatsapp_number_response(
                company_id)
            if number_dict.get('result') == 'not exists':
                rec.is_whatsapp_number = False
            elif number_dict.get('result') == 'exists':
                rec.is_whatsapp_number = True

    @api.constrains('mobile')
    def _validate_mobile(self):
        for rec in self:
            mobile = rec._formatting_mobile_number()
            if not mobile.isdigit():
                raise ValidationError(_("Invalid mobile number."))
