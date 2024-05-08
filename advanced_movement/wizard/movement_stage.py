from odoo import models, fields


class Stage(models.Model):
    _name = "movement.stage"
    _description = " Movement Stage "
    _order = "sequence"

    approval_role_id = fields.Many2one("approval.role", string="Stage Name", required=True)
    approval_type = fields.Char(string="Approval Type", size=100, required=True)
    approvers = fields.Many2one('hr.employee', string="Approvers(Predefined)", required=True)
    sequence = fields.Char(string="Sequence")
    approval_flow_id = fields.Many2one("approval.flow", string="Approval Flow")

    def unlink(self):
        for i in self:
            i.unlink()
