from odoo import models, fields


class ApprovalRole(models.Model):
    _name = "approval.role"
    _description = "Approval Role"
    _inherit = "mail.thread"
    _rec_name = "position_role"
    
    position_role = fields.Char(string="Position/Role")
    user_ids = fields.Many2many("hr.employee", "approval_role_id", string="Users(s)")
    company_id = fields.Many2one("res.company", string="Company")
