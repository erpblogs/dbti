from odoo import models, api, _

class HrDepartmentInherit(models.Model):
    _inherit = 'hr.department'
    
    @api.depends('parent_path')
    def _compute_master_department_id(self):
        for department in self:
            if department.parent_path:
                try:
                    master_department_id = int(department.parent_path.split('/')[0])
                except: 
                    master_department_id = department.id
            department.master_department_id = master_department_id or department.id