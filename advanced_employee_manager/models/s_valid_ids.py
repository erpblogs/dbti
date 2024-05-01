from odoo import models, fields, api
import re
from datetime import datetime
from odoo.exceptions import ValidationError


class SValidIds(models.Model):
    _name = 's.valid.ids'

    s_valid_id = fields.Char(string='Valid ID', required=True, size=100)
    s_hr_valid_id = fields.Many2one('hr.employee')