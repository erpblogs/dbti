from odoo import models, fields, api
import re
from datetime import datetime
from odoo.exceptions import ValidationError


class STrainingDevelopment(models.Model):
    _name = 's.training.development'

    s_training_development = fields.Char(string='Training & Development description', required=True, size=100)
    s_hr_training_development_id = fields.Many2one('hr.employee')