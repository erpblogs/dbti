import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'


    @api.constrains('email')
    def _check_email_format(self):
        for record in self:
            if record.email:
                email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'  # Regex pattern for email
                if not re.match(email_pattern, record.email):
                    raise ValidationError("Invalid email format! Please enter a valid email.")

    @api.constrains('mobile')
    def _check_phone_format(self):
        for record in self:
            if record.mobile:
                mobile_pattern = r'^\d+$'  # Regex pattern for phone number (only digits)
                if not re.match(mobile_pattern, record.mobile):
                    raise ValidationError("Invalid mobile number format! Please enter a valid phone number.")
                
    @api.constrains('phone')
    def _check_mobile_format(self):
        for record in self:
            if record.phone:
                phone_pattern = r'^\+?\d{8,15}$'  # Regex pattern for mobile number
                if not re.match(phone_pattern, record.phone):
                    raise ValidationError("Invalid phone number format! Please enter a valid mobile number.")        