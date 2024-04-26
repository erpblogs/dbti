import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'mail.alias.domain'


    @api.constrains('name')
    def _constrains_name_alias_domain_id(self):
        for record in self:
            if record.name:
                email_domain = r'^[a-zA-Z0-9]+([-.][a-zA-Z0-9]+)*\.[a-zA-Z]{2,}$'  # Regex pattern for email domain
                if not re.match(email_domain, record.name):
                    raise ValidationError("Invalid email domain format! Please enter a valid email domain.")
