import hashlib
import hmac
import json
from datetime import date
import time

import requests
from odoo import http, SUPERUSER_ID
from odoo import fields, models, api


class ResConfigFullnameEmployee(models.TransientModel):
    _inherit = ['res.config.settings']

    s_last_name_in_fullname = fields.Integer(string='Last name', config_parameter='advanced_employee_manager.s_last_name_in_fullname', default=0)
    s_first_name_in_fullname = fields.Integer(string="First name", config_parameter='advanced_employee_manager.s_first_name_in_fullname', default=0)
    s_middle_name_in_fullname = fields.Integer(string="Middle name", config_parameter='advanced_employee_manager.s_middle_name_in_fullname', default=0)
    s_suffix_in_fullname = fields.Integer(string="Suffix", config_parameter='advanced_employee_manager.s_suffix_in_fullname', default=0)

    s_suffix_in_emp_id = fields.Integer(string="Suffix", config_parameter='advanced_employee_manager.s_suffix_in_emp_id', default=0)
    s_bod_year_in_emp_id = fields.Integer(string="Birthday Year", config_parameter='advanced_employee_manager.s_bod_year_in_emp_id', default=0)
    s_bod_month_in_emp_id = fields.Integer(string="Birthday Month", config_parameter='advanced_employee_manager.s_bod_month_in_emp_id', default=0)
    s_fullname_in_emp_id = fields.Integer(string="Full Name", config_parameter='advanced_employee_manager.s_fullname_in_emp_id', default=0)

    # def btn_config_fullname_employee(self):
    #     return {
    #         'name': 'Authorization',
    #         'type': 'ir.actions.act_url',
    #         'url': "/employee/template",  # Replace this with tracking link
    #         'target': 'current',  # you can change target to current, self, new.. etc
    #     }
