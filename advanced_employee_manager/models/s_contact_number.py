from odoo import models, fields, api
import re
from datetime import datetime
from odoo.exceptions import ValidationError


class SContactNumber(models.Model):
    _name = 's.contact.number'

    s_contact_number = fields.Char(string='Contact number', required=True, size=100)
    s_hr_contact_number_id = fields.Many2one('hr.employee', string='Contact number')