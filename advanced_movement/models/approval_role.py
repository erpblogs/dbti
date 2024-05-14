from odoo import models, fields , api
from odoo.exceptions import ValidationError


class ApprovalRole(models.Model):
    _name = "approval.role"
    _description = "Approval Role"
    _inherit = "mail.thread"
    _rec_name = "position_role_id"

    position_role_id = fields.Many2one('hr.job', string='Position/Role', domain="[('company_id', '=', company_id)]", required=True)
    user_ids = fields.Many2many("res.users", "approval_role_res_users_rel", string="Users(s)", domain="[('company_id', '=', company_id)]", required=True)
    company_id = fields.Many2one("res.company", string="Company", default=lambda self: self.env.company, required=True)

    @api.constrains('position_role_id')
    def check_unique_position_role_id(self):
        for record in self:
            if record.position_role_id:
                duplicate_records = self.env["approval.role"].search([('id', '!=', record.id), ('position_role_id.name', '=', record.position_role_id.name)])
                if duplicate_records:
                    raise ValidationError("The operation cannot be completed: The name of position/role must be unique per company!")