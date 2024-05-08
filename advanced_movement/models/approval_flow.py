from odoo import models, fields, api


class ApprovalFlow(models.Model):
    _name = "approval.flow"
    _description = "Approval Flow"
    _inherit = "mail.thread"
    _rec_name = "movement_type"
    
    movement_type = fields.Char(string="Movement Type", readonly=True)
    company_id = fields.Many2one("res.company", string="Company")
    sequence = fields.Boolean(string="Sequence")
    parallel = fields.Boolean(string="Parallel")
    stage_id = fields.One2many("movement.stage", "approval_flow_id", string="Stage Name")

    @api.onchange('sequence')
    def _onchange_boolean_field_1(self):
        if self.sequence:
            self.parallel = False
        else:
            self.parallel = True

    @api.onchange('parallel')
    def _onchange_boolean_field_2(self):
        if self.parallel:
            self.sequence = False
        else:
            self.sequence = True
