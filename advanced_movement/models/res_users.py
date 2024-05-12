from odoo import models, fields


class ResUsers(models.Model):
    _inherit = "res.users"

    s_state_movement = fields.Selection([('approve', 'Approve'), ('refuse', 'Refuse')])
