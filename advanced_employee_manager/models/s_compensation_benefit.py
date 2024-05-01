from odoo import models, fields, api
import re
from datetime import datetime
from odoo.exceptions import ValidationError


class SCompensationBenefit(models.Model):
    _name = 's.compensation.benefit'

    s_amount = fields.Float(string='Amount', required=True, size=15)
    s_transaction_type = fields.Char(string='Transaction Type', required=True, size=100)
    s_hr_compensation_benefit_id = fields.Many2one('hr.employee', string='Compensation Benefit')