from odoo import fields, models, _


class SDRGenerateWiz(models.TransientModel):
    _name = 'sdr.generate.wiz'
    _description = 'Generate SDR Wizard'

    name = fields.Char('Name', required=True)
    ticket_id = fields.Many2one('helpdesk.ticket', string='Ticket')
    task_id = fields.Many2one('project.task', string='Task')
    partner_ids = fields.Many2many('res.partner', string='Customer', required=True)
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
    number = fields.Char('Ticket/Task No')
    in_time = fields.Float('In Time')
    out_time = fields.Float('Out Time')

    def generate_attachment(self):
        for partner in self.partner_ids:
            sdr = self.env['sdr.generate'].create({
                'name': self.name,
                'ticket_id': self.ticket_id.id,
                'task_id': self.task_id.id,
                'partner_id': partner.id,
                'user_id': self.user_id.id,
                'is_project_plan': self.is_project_plan,
                'is_portal_access_training': self.is_portal_access_training,
                'is_data_template': self.is_data_template,
                'is_kick_of_meeting': self.is_kick_of_meeting,
                'is_installation': self.is_installation,
                'is_key_user_interview': self.is_key_user_interview,
                'is_pdd_approval': self.is_pdd_approval,
                'is_end_user_training': self.is_end_user_training,
                'is_meeting': self.is_meeting,
                'is_test': self.is_test,
                'is_opening_balance_method': self.is_opening_balance_method,
                'is_indoor_skydiving': self.is_indoor_skydiving,
                'is_cut_of_plan': self.is_cut_of_plan,
                'is_support': self.is_support,
                'is_meeting_visit': self.is_meeting_visit,
                'details_of_work': self.details_of_work,
                'number': self.number,
                'in_time': self.in_time,
                'out_time': self.out_time,
            })
            sdr.generate_attachment()
