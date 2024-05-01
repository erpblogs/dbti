from odoo import models, fields, api
import re
from datetime import datetime
from odoo.exceptions import ValidationError


class SLicense(models.Model):
    _name = 's.license'

    s_license = fields.Char(string='License', required=True, size=100)
    s_license_id = fields.Char(string='License ID', required=True, size=100)
    s_hr_license_id = fields.Many2one('hr.employee')