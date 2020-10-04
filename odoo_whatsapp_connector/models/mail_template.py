# See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class MailTemplate(models.Model):
    """Inherit Mail Template."""

    _inherit = 'mail.template'

    is_whatsapp = fields.Boolean(
        string='Is Whatsapp Template',
        default=False
    )
