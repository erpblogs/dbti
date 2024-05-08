from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = "hr.employee"
    
    approval_role_ids = fields.Many2one("approval.role", string="Approval Role ID")