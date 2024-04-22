from odoo import models, fields, _



class HrEmployeeBase(models.AbstractModel):
    """
    Custom Hr Base
    """
    _inherit = 'hr.employee.base'
    
    job_level_id = fields.Many2one('hr.job.level', 'Level')
    
