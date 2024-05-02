from odoo import models, fields, api, _
from odoo.exceptions import UserError

class HrDepartmentInherit(models.Model):
    _inherit = 'hr.department'
    
    department_id = fields.Char("Department ID", required=True)
    
    @api.depends('parent_path')
    def _compute_master_department_id(self):
        for department in self:
            if department.parent_path:
                try:
                    master_department_id = int(department.parent_path.split('/')[0])
                except: 
                    master_department_id = department.id
            department.master_department_id = master_department_id or department.id
            
    @api.constrains('department_id')
    def _check_department_id(self):
        for d in self:
            # if not department_id:
            #     raise UserError(_("Department is required!"))
            if d.department_id and self.search([
                ('id', '!=', d.id),
                ('department_id', '=', d.department_id),
            ], limit=1):
                raise UserError(_("Department ID must be unique!"))
