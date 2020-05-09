from odoo import api, fields, models,_
from odoo.exceptions import UserError, ValidationError



class TaskTicketWizard(models.TransientModel):
    _name = 'task.ticket.wizard'

    ticket_task = fields.Selection([('ticket', 'Ticket'), ('task', 'Task')], 'Ticket /Task')

    attachment_id = fields.Many2one('ir.attachment', related='sign_template_id.attachment_id', string="Attachment",
                                    required=True, ondelete='cascade')

    task_id = fields.Many2one('project.task', String='Task')
    sign_template_id = fields.Many2one("sign.template")
    ticket_id = fields.Many2one('helpdesk.ticket', string="Ticket")

    def confirm(self):
        if self.attachment_id:
            if self.ticket_task == 'task':
                self.attachment_id.res_model = 'project.task'
                self.attachment_id.res_id = self.task_id.id
            if self.ticket_task == 'ticket':
                self.attachment_id.res_model = 'helpdesk.ticket'
                self.attachment_id.res_id = self.ticket_id.id
            if self.sign_template_id:
                self.sign_template_id.is_document_added = True
        else:
            raise UserError(_('There is no attachment in the file'))


