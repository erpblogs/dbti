from odoo import models, fields

class ResCompany(models.Model):
    _name = "res.company"
    _inherit = ['res.company','mail.thread']