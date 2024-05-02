from odoo import models, fields, api
import re
from datetime import datetime
from odoo.exceptions import ValidationError


class SProjectProject(models.Model):
    _inherit = 'project.project'

    s_hr_employee_id = fields.Many2one('hr.employee', string='Employee')
    line_type_id = fields.Many2one('hr.resume.line.type', string="Type")