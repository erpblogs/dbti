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
    is_type_job_rotation_request = fields.Boolean(string="Is Type Job Rotation Request")
    is_type_regularization_request = fields.Boolean(string="Is Type Regularization Request")
    approve_hr_movement_ids = fields.One2many("hr.movement", "movement_type_id", string="Approve Movement Type")

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

    def write(self, vals):
        res = super(ApprovalFlow, self).write(vals)
        approve_hr_movement_ids = self.approve_hr_movement_ids
        stage_id = self.stage_id
        if approve_hr_movement_ids:
            for approve_hr_movement_id in approve_hr_movement_ids:
                for user_approve in stage_id.user_ids:
                    if user_approve not in approve_hr_movement_id.action_user_ids.user_id:
                        approve_hr_movement_id.action_user_ids = [(0, 0, {'user_id': user_approve.id})]
        return res
