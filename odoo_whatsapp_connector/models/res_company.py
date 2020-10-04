# See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _
from odoo.exceptions import Warning
import requests
import json


class ResCompany(models.Model):
    _inherit = 'res.company'
    _description = 'Res Company'

    api_url = fields.Char("API URL",
                          default='https://api.chat-api.com/instance')
    instance_no = fields.Integer("Instance Number")
    api_token = fields.Char("API Token")
    whatsapp_qr_code = fields.Binary("QR Code")
    authenticate = fields.Boolean("Authenticate")
    partner_ids = fields.Many2many('res.partner', string='Contacts')
    label = fields.Char(
        string='Label', readonly=True,
        default="Configure API Token and Instance Number."
    )

    def check_auth(self):
        for rec in self:
            url_path = ''
            if rec.api_url and rec.instance_no and rec.api_token:
                url_path = rec.api_url + \
                    str(rec.instance_no) + '/status' + '?token=' \
                    + rec.api_token
            try:
                requests.get(
                    url_path, headers={
                        'Content-Type': 'application/json'})
            except (requests.exceptions.HTTPError,
                    requests.exceptions.RequestException,
                    requests.exceptions.ConnectionError) as err:
                raise Warning(
                    _('Error! \n Could not connect to Whatsapp account. %s')
                    % (err))

    def get_qr_code(self):
        for rec in self:
            qr_data = {}
            rec.check_auth()
            if rec.instance_no and rec.api_token:
                url_path = rec.api_url + \
                    str(rec.instance_no) + '/status' + '?token=' \
                    + rec.api_token
                request_qr = requests.get(
                    url_path, headers={
                        'Content-Type': 'application/json'})
                qr_data = json.loads(request_qr.text)
                if qr_data.get('accountStatus') == 'authenticated':
                    rec.write({'authenticate': True,
                               'label': 'Successfully login'})
                elif qr_data.get('qrCode'):
                    image = qr_data.get('qrCode').split(',')
                    rec.write(
                        {'whatsapp_qr_code': image[1],
                         'label': 'Please scan QR code to Log In from Mobile'})
                else:
                    rec.write(
                        {'whatsapp_qr_code': False,
                         'label': qr_data.get('error')})

    def logout(self):
        for rec in self:
            rec.check_auth()
            if rec.instance_no and rec.api_token:
                url_path = rec.api_url + \
                    str(rec.instance_no) + '/logout' + '?token=' \
                    + rec.api_token
                requests.post(url_path, headers={
                    'Content-Type': 'application/json'})
                rec.write({'whatsapp_qr_code': False,
                           'authenticate': False,
                           'label': 'Successfully Logout...'})
