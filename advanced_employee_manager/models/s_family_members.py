from odoo import models, fields, api
import re
from datetime import datetime
from odoo.exceptions import ValidationError


class SFamilyMember(models.Model):
    _name = 's.family.member'

    s_family_member = fields.Char(string='Family Members', required=True, size=100)
    s_hr_family_member = fields.Many2one('hr.employee')