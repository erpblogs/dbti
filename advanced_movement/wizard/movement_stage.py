from odoo import models, fields


class Stage(models.Model):
    _name = "movement.stage"
    _description = " Movement Stage "
    _order = "sequence"
    
    name = fields.Char(string="Stage Name", size=100, required=True)
    approval_role_id = fields.Many2one("approval.role", string="Approval Type", required=True)
    approvers = fields.Many2one('hr.employee', string="Approvers(Predefined)", required=True)
    sequence = fields.Integer(string="Sequence")
    approval_flow_id = fields.Many2one("approval.flow", string="Approval Flow")

    def unlink(self):
        for i in self:
            i.unlink()
