from odoo import models, fields, api
import re
from datetime import datetime
from odoo.exceptions import ValidationError


class SSurveySurvey(models.Model):
    _inherit = 'survey.survey'

