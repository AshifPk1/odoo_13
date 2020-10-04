# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, sql_db, _
from odoo.exceptions import UserError
from datetime import datetime
import threading
import requests


class WhatsappMessageLog(models.Model):
    _name = 'whatsapp.message.log'
    _description = 'Whatsapp Message Log'

    name = fields.Char('Contact')
    link = fields.Char("Link URL")
    message = fields.Text("Message")
    message_body = fields.Text(
        string='Message',
    )
    data = fields.Text()
    msg_date = fields.Datetime("Message Date")
    chat_id = fields.Char(
        string='Chat Id',
    )
    user_id = fields.Many2one(
        'res.users',
        string='Send By',
        default=lambda self: self.env.user,
    )
    status = fields.Selection([
        ('error', 'Error'), ('send', 'Sent')], string='Status',)

    @api.model
    def whatsapp_message_resend(self, company_id):
        try:
            new_cr = sql_db.db_connect(self.env.cr.dbname).cursor()
            uid, context = self.env.uid, self.env.context
            with api.Environment.manage():
                self.env = api.Environment(new_cr, uid, context)
                message_log_rec = self.env['whatsapp.message.log'].search(
                    [('status', '=', 'error')])
                token_value = {'token': company_id.api_token}
                for log_rec in message_log_rec:
                    request_meeting = requests.post(
                        log_rec.link, data=log_rec.data,
                        params=token_value,
                        headers={'Content-Type': 'application/json'})
                    if request_meeting.status_code == 200:
                        log_rec.write({
                            'msg_date': datetime.now(),
                            'message': request_meeting.text,
                            'status': 'send'})
                    else:
                        log_rec.write({
                            'msg_date': datetime.now(),
                            'message': request_meeting.text,
                            'status': 'error'})
                    new_cr.commit()
        finally:
            self.env.cr.close()

    @api.model
    def resend_whatsapp_message(self):
        """Resend whatsapp message via threding."""
        company_id = self.env.user.company_id
        if company_id and not company_id.authenticate:
            raise UserError(_('Whatsapp Authentication Failed.'
                              ' Configure Whatsapp Configuration'
                              ' in company setting.'))
        company_id.check_auth()
        thread_start = threading.Thread(
            target=self.whatsapp_message_resend(company_id))
        thread_start.start()
        return True
