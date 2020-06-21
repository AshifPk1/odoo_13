from odoo import fields, models, _
import base64
from odoo.exceptions import UserError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    sdr_ids = fields.One2many('sdr.generate', 'task_id', string='SDRs')

    def generate_attachment(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Create SDR'),
            'res_model': 'sdr.generate.wiz',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_name': self.name,
                'default_type': 'task',
                'default_task_id': self.id,
                'default_user_id': self.project_id.main_imp.id,
                'default_number': 'M' + '/' + self.name,
            }
        }


class SDRGenerate(models.Model):
    _inherit = 'sdr.generate'

    task_id = fields.Many2one('project.task', string='Task')

