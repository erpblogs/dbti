from odoo import models, fields, api
import re
from datetime import datetime
from odoo.exceptions import ValidationError


class SEducation(models.Model):
    _name = 's.education'

    s_school_name = fields.Char(string='School Name', required=True, size=100)
    s_level_of_education = fields.Selection(
        [('primary_education', 'Primary Education'), ('Secondary_education', 'Secondary Education'),
         ('vocational_education', 'Vocational Education'), ('tertiary_education', 'Tertiary Education'),
         ('undergraduate_education', 'Undergraduate Education'), ('graduate_education', 'Graduate Education'),
         ('postgraduate_education', 'Postgraduate Education')], string='Level of Education', required=True)
    s_duration_from = fields.Datetime(string='Duration From', required=True)
    s_duration_to = fields.Datetime(string='Duration To', required=True)
    s_major = fields.Char(string='Major', size=100)
    s_hr_education_id = fields.Many2one('hr.employee')
