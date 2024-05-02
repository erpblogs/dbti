from odoo import models, fields, api
from odoo.exceptions import ValidationError

         
class ChangePasswordUser(models.TransientModel):
    _inherit = 'change.password.user'

    @api.constrains('new_passwd')
    def _check_password_strength(self):
        for record in self:
            if record.new_passwd.isdigit():
                raise ValidationError("Password must be numbers, letters, or other characters.")
            elif len(record.new_passwd) < 8:
                raise ValidationError("Password must be more than 8 characters.")
            elif record.new_passwd.islower():
                raise ValidationError("Password must include at least an upper-case character.")

    def change_password_button(self):
        for line in self:
            if line.new_passwd:
                line.user_id._change_password(line.new_passwd)
        # don't keep temporary passwords in the database longer than necessary
        self.write({'new_passwd': line.new_passwd})
