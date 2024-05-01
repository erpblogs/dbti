from odoo import models, fields, api
import re
from datetime import datetime
from odoo.exceptions import ValidationError


class SInternalWorkHistory(models.Model):
    _name = 's.internal.work.history'

    s_company_name = fields.Char(string='Company name', required=True, size=100)
    s_position = fields.Char(string='Position', required=True, size=100)
    s_duration_from = fields.Datetime(string='Duration From', required=True)
    s_duration_to = fields.Datetime(string='Duration To', required=True)
    s_major = fields.Char(string='Major', size=100)
    s_hr_internal_work_history_id = fields.Many2one('hr.employee')
