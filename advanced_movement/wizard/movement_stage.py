from odoo import models, fields


class Stage(models.Model):
    _name = "movement.stage"
    _description = " Movement Stage "
    _order = "sequence"

    approval_role_id = fields.Many2one("approval.role", string="Stage Name", required=True)
    s_hr_employee_id = fields.Many2one("hr.employee")
    approvers = fields.Many2one('res.users', string="Approvers(Predefined)", required=True)
    sequence = fields.Char(string="Sequence")
    approval_flow_id = fields.Many2one("approval.flow", string="Approval Flow")
    is_approver = fields.Boolean(string="Is Approver")
    is_refuse = fields.Boolean(string="Is Refuse")