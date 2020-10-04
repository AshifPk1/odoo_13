# See LICENSE file for full copyright and licensing details.

from odoo import models, api, fields, sql_db, _
from odoo.tools.mimetypes import guess_mimetype
from datetime import datetime
from odoo.exceptions import UserError
import requests
import json
import base64
import threading
import time
import logging

_logger = logging.getLogger(__name__)


class WhatsappMessage(models.TransientModel):

    _name = 'whatsapp.message'
    _description = "Whatsapp Message"

    partner_ids = fields.Many2many('res.partner', string='Contacts')
    message = fields.Text()
    attachment = fields.Binary("Attachment")
    filename = fields.Char()
    title = fields.Char()
    link = fields.Char("Link URL")
    message_type = fields.Selection([
        ('text', 'Text'),
        ('media', 'Media'),
        ('url_link', 'Url Link')], default='text')

    @api.onchange('message_type')
    def onchange_message_type(self):
        if self.message_type == 'text':
            self.attachment = False
            self.title = False
            self.link = False
            self.filename = False
        elif self.message_type == 'media':
            self.title = False
            self.link = False
        elif self.message_type == 'url_link':
            self.attachment = False
            self.filename = False

    def send_whatsapp_message_new(self):
        try:
            new_cr = sql_db.db_connect(self.env.cr.dbname).cursor()
            uid, context = self.env.uid, self.env.context
            attachment_new = False
            message = False
            with api.Environment.manage():
                self.env = api.Environment(new_cr, uid, context)
                company_id = self.env.user and\
                    self.env.user.company_id or False
                path = company_id and company_id.api_url + \
                    str(company_id.instance_no)
                whatsapp_log_obj = self.env['whatsapp.message.log']
                for rec in self:
                    if rec.message_type == 'text':
                        url_path = path + '/sendMessage'
                    elif rec.message_type == 'media':
                        url_path = path + '/sendFile'
                    elif rec.message_type == 'url_link':
                        url_path = path + '/sendLink'
                    token_value = {'token': company_id.api_token}
                    if rec.attachment:
                        mimetype = guess_mimetype(
                            base64.b64decode(rec.attachment))
                        if mimetype == 'application/octet-stream' and\
                                rec.message_type == 'media':
                            mimetype = 'video/mp4'
                        str_mimetype = 'data:' + mimetype + ';base64,'
                        attachment_new = str_mimetype + \
                            str(rec.attachment.decode("utf-8"))
                    if rec.filename:
                        message = "Message: " + rec.message +\
                            " Attachment: " + rec.filename
                    elif rec.message:
                        message = rec.message
                    for partner_rec in rec.partner_ids:
                        if partner_rec.is_whatsapp_number and\
                                partner_rec.mobile:
                            mobile = partner_rec._formatting_mobile_number()
                            if rec.message_type == 'text':
                                message_data = {'phone': mobile,
                                                'body': rec.message}
                            elif rec.message_type == 'media':
                                message_data = {'phone': mobile,
                                                'body': attachment_new,
                                                'filename': rec.filename,
                                                'caption': rec.message}
                            elif rec.message_type == 'url_link':
                                message_data = {
                                    'phone': mobile,
                                    'body': rec.link,
                                    'title': rec.title,
                                    'description': rec.message,
                                    'previewBase64': attachment_new,
                                }
                            data = json.dumps(message_data)
                            request_meeting = requests.post(
                                url_path, data=data, params=token_value,
                                headers={'Content-Type': 'application/json'})
                            if request_meeting.status_code == 200:
                                data = json.loads(request_meeting.text)
                                chat_id = data.get('id') and\
                                    data.get('id').split('_')
                                whatsapp_log_obj.create(
                                    {'name': partner_rec.name,
                                     'msg_date': datetime.now(),
                                     'link': url_path,
                                     'data': data,
                                     'chat_id': chat_id[1],
                                     'message': request_meeting.text,
                                     'message_body': message,
                                     'status': 'send'})
                                partner_rec.chat_id = chat_id[1]
                            else:
                                whatsapp_log_obj.create(
                                    {'name': partner_rec.name,
                                     'msg_date': datetime.now(),
                                     'link': url_path,
                                     'data': data,
                                     'message': request_meeting.text,
                                     'message_body': message,
                                     'status': 'error'})
                            new_cr.commit()
                            time.sleep(3)
        finally:
            self.env.cr.close()

    def send_whatsapp_message(self):
        """Send whatsapp message via threding."""
        company_id = self.env.user and\
            self.env.user.company_id or False
        if company_id and not company_id.authenticate:
            raise UserError(_('Whatsapp Authentication Failed.'
                              ' Configure Whatsapp Configuration'
                              ' in company setting.'))
        company_id.check_auth()
        thread_start = threading.Thread(
            target=self.send_whatsapp_message_new)
        thread_start.start()
        return True
