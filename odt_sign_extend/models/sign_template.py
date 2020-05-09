from odoo import fields, models, api
from odoo.osv import expression


class SignTemplate(models.Model):
    _inherit = 'sign.template'

    is_document_added = fields.Boolean("Documnet Added")


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('name', operator, name), ('project_id', operator, name)]
        ids = self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
        return self.browse(ids).name_get()


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('name', operator, name), ('email_cc', operator, name)]
        ids = self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
        return self.browse(ids).name_get()


