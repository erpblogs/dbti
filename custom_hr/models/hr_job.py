from odoo import models, fields, _

class HrJobInherit(models.Model):
    _name = 'hr.job'
    _inherit = ['hr.job', 'mail.thread']
    
    def copy(self, default=None):
        default = dict(default or {})
        default['name'] = self.name + ' (copy)'
        return super().copy(default)
