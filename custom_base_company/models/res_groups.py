from odoo import models, fields, api


class Groups(models.Model):
    _inherit = 'res.groups'

    group_code = fields.Char(string=" Group ID", required=True, help="Create Id of this group")
    
    _sql_constraints = [
        ('group_code_unique', 'unique (group_code)', 'The group id must be unique within an application!')
    ]