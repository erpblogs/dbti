from odoo import models, fields, api
import re
from datetime import datetime
from odoo.exceptions import ValidationError
import math


class SHrEmployee(models.Model):
    _inherit = 'hr.employee'

    s_last_name = fields.Char(string='Last name', size=100, required=True)
    # s_first_name = fields.Char(string='First name', size=100, required=True)
    s_middle_name = fields.Char(string='Middle name', size=100)
    s_full_name = fields.Char(string='Full name', compute='_compute_full_name')
    # s_birthdate = fields.Datetime(string='Birthdate', required=True)
    s_generation = fields.Selection(([]), string='Generation')
    s_age = fields.Integer(string='Age', compute='_compute_age', store=True)
    # s_gender = fields.Selection([
    #     ('male', 'Male'),
    #     ('female', 'Female')
    # ], string='Gender', required=True)
    s_suffix = fields.Char(string='Suffix', size=20)
    s_nick_name = fields.Char(string='Nick name', size=100)
    s_maiden_name = fields.Char(string='Maiden name', size=100)
    s_personal_email = fields.Char(string='Personal email', size=100, unique=True)
    s_corporate_email = fields.Char(string='Corporate email', size=100, unique=True)

    s_employee_id = fields.Char(string='Employee ID', readonly=True)
    s_biometrics_id = fields.Char(string='Biometrics ID', size=10, unique=True)
    s_role_profile = fields.One2many('res.groups', 's_hr_res_groups_id', string='Role profile', required=True)
    s_employee_status = fields.Selection(
        [('active', 'Active'), ('inactive', 'Inactive'), ('retire', 'Retire'), ('resign', 'Resign'),
         ('terminated', 'Terminated'), ('end_of_contract', 'End of contract'), ('on_hold', 'On hold')],
        string='Employee status', default='active', readonly=True)
    s_resigned_date = fields.Date(string='Resigned date', readonly=True)
    s_department = fields.Many2one('hr.department', string='Department')
    # s_date_hired = fields.Date(string='Date hired')
    s_date_of_separation = fields.Integer(string='Date of separation', readonly=True)
    s_date_of_regularization = fields.Integer(string='Date of regularization', readonly=True)
    s_month_in_service = fields.Integer(string='Month in service', compute="_compute_month_in_service_and_years_in_service")
    s_years_in_service = fields.Integer(string='Years in service', compute="_compute_month_in_service_and_years_in_service")

    s_position_title = fields.Many2one('hr.job', string='Position title', size=100)
    s_job_level = fields.Many2one('hr.job.level', string='Job level', size=100)
    s_default_schedule = fields.Integer(string='Default schedule', readonly=True)
    # s_leave_balance_setup = fields.Many2one(string='Leave balance setup', size=100)
    s_project_project_ids = fields.One2many('project.project', 's_hr_employee_id', string='Project')
    s_is_active = fields.Boolean(string='Is active')
    s_location = fields.Many2one('hr.work.location', string='Location')
    s_date_hired = fields.Datetime(string='Date hired', required=True)

    @api.depends('s_date_hired')
    def _compute_month_in_service_and_years_in_service(self):
        for rec in self:
            if rec.s_date_hired:
                day_in_service = datetime.now().day - rec.s_date_hired.day
                year_in_service = datetime.now().year - rec.s_date_hired.year
                if day_in_service < 0:
                    rec.s_month_in_service = (datetime.now().month - rec.s_date_hired.month - 1) + year_in_service*12
                else:
                    rec.s_month_in_service = (datetime.now().month - rec.s_date_hired.month) + year_in_service*12
                rec.s_years_in_service = year_in_service

    @api.onchange('s_is_active')
    def _onchange_s_is_active(self):
        for rec in self:
            if rec.s_is_active:
                rec.s_employee_status = 'active'
                if rec.s_on_hold:
                    rec.s_on_hold = False
            else:
                rec.s_employee_status = 'inactive'

    @api.depends('s_last_name', 'name', 's_middle_name', 's_suffix')
    def _compute_full_name(self):
        for rec in self:
            ir_config = self.env['ir.config_parameter'].sudo()
            last_name_in_fullname = ir_config.get_param('advanced_employee_manager.s_last_name_in_fullname')
            first_name_in_fullname = ir_config.get_param('advanced_employee_manager.s_first_name_in_fullname')
            middle_name_in_fullname = ir_config.get_param('advanced_employee_manager.s_middle_name_in_fullname')
            suffix_in_fullname = ir_config.get_param('advanced_employee_manager.s_suffix_in_fullname')
            # Create a list of tuples, each containing a field and its order
            fields_and_orders = [
                (rec.s_last_name, last_name_in_fullname),
                (rec.name, first_name_in_fullname),
                (rec.s_middle_name, middle_name_in_fullname),
                (rec.s_suffix, suffix_in_fullname)
            ]
            fields_and_orders = [(field if field else "", order if order else '0') for field, order in
                                 fields_and_orders]
            fields_and_orders = [item for item in fields_and_orders if item[1] != '0']
            # Sort the list by the order
            fields_and_orders.sort(key=lambda x: x[1])

            # Build the full name by concatenating the fields in the sorted order
            full_name = " ".join(field for field, order in fields_and_orders if field)

            # Assign the full name to s_full_name
            rec.s_full_name = full_name

    @api.onchange('s_last_name', 'name', 's_middle_name', 's_suffix')
    def _onchange_full_name(self):
        self._compute_full_name()

    @api.onchange('birthday', 's_full_name', 's_suffix')
    def _onchange_employee_id(self):
        for rec in self:
            ir_config = self.env['ir.config_parameter'].sudo()
            suffix_in_emp_id = ir_config.get_param('advanced_employee_manager.s_suffix_in_emp_id')
            bod_year_in_emp_id = ir_config.get_param('advanced_employee_manager.s_bod_year_in_emp_id')
            bod_month_in_emp_id = ir_config.get_param('advanced_employee_manager.s_bod_month_in_emp_id')
            fullname_in_emp_id = ir_config.get_param('advanced_employee_manager.s_fullname_in_emp_id')
            bod_year, bod_month = "", ""

            if rec.birthday:
                bod_year = rec.birthday.year
                bod_month = rec.birthday.month
            # Create a list of tuples, each containing a field and its order
            fields_and_orders = [
                (rec.s_suffix, suffix_in_emp_id),
                (bod_year, bod_year_in_emp_id),
                (bod_month, bod_month_in_emp_id),
                (rec.s_full_name, fullname_in_emp_id)
            ]
            fields_and_orders = [(field if field else "", order if order else '0') for field, order in
                                 fields_and_orders]
            fields_and_orders = [item for item in fields_and_orders if item[1] != '0']
            # Sort the list by the order
            fields_and_orders.sort(key=lambda x: x[1])

            # Build the full name by concatenating the fields in the sorted order
            employee_id = " ".join(field for field, order in fields_and_orders if field)

            # Assign the full name to s_full_name
            rec.s_employee_id = employee_id

    @api.constrains('s_role_profile')
    def _check_s_role_profile(self):
        for record in self:
            if not record.s_role_profile:
                raise ValidationError("The Role profile field is required.")

    ### start Compensation and Benefits

    s_total_year_days = fields.Selection(
        [('365', '365'), ('313', '313'), ('312', '312'), ('264', '264'), ('261', '261'), ('394.4', '394.4'),
         ('other', 'Other')], string="Total Year days", required=True)
    s_other = fields.Float(string='Other')
    s_is_other = fields.Boolean(string='Is Other', default=False)

    s_rate_type = fields.Selection(
        [('hourly_rate', 'Hourly Rate'), ('daily_rate', 'Daily Rate'), ('monthly_rate', 'Monthly Rate')],
        string='Rate Type', required=True)
    s_monthly_rate = fields.Integer(string='Monthly Rate', size=12)
    s_daily_rate = fields.Float(string='Daily Rate', compute="_compute_daily_rate", store=True, readonly=True)
    s_hourly_rate = fields.Float(string='Hourly Rate', compute="_compute_hourly_rate", store=True, readonly=True)
    s_payroll_schedule = fields.Selection(
        [('semi_monthly', 'Semi Monthly'), ('monthly', 'Monthly'), ('weekly', 'Weekly')],
        string='Payroll Schedule', required=True)
    # s_period_group = fields.Many2one(string="Period Group")
    # s_rate_classification = fields.Many2one(string="Rate Classification")
    s_minimum_take_home = fields.Float(string='Minimum Take Home', size=15)
    s_cost_center = fields.Char(string='Cost Center', size=50)
    s_mode_of_payment = fields.Selection([('cash', 'Cash'), ('bank', 'Bank'), ('cheque', 'Cheque')],
                                         string='Mode of Payment')
    s_on_hold = fields.Boolean(string='On hold', default=False)
    s_minimum_take_home_as_percentage = fields.Boolean(string='Minimum Take Home as Percentage', default=False)
    s_minimum_take_home_as_percentage_textbox = fields.Float(string='Enter Minimum Take Home as Percentage')
    s_compensation_benefit_ids = fields.One2many('s.compensation.benefit', 's_hr_compensation_benefit_id',
                                                 string='Other Compensation and Benefits')

    @api.onchange('s_total_year_days')
    def _onchange_s_total_year_days(self):
        s_is_other = False
        for rec in self:
            if rec.s_total_year_days == 'other':
                s_is_other = True
            rec.s_is_other = s_is_other

    @api.constrains('s_other')
    def _check_s_other(self):
        for record in self:
            if record.s_total_year_days == 'other' and record.s_other == 0:
                raise ValidationError("The value must be different from 0")

    @api.depends('s_monthly_rate', 's_total_year_days')
    def _compute_daily_rate(self):
        for rec in self:
            if rec.s_total_year_days != 'other':
                if rec.s_total_year_days:
                    rec.s_daily_rate = round((rec.s_monthly_rate * 12) / int(rec.s_total_year_days), 2)
            elif rec.s_total_year_days == 'other':
                if rec.s_other:
                    rec.s_daily_rate = round((rec.s_monthly_rate * 12) / rec.s_other, 2)

    @api.depends('s_daily_rate', 's_no_hours')
    def _compute_hourly_rate(self):
        for rec in self:
            if rec.s_no_hours != 0:
                rec.s_hourly_rate = round(rec.s_daily_rate / rec.s_no_hours, 2)

    @api.onchange('s_on_hold')
    def _onchange_s_on_hold(self):
        for rec in self:
            if rec.s_on_hold:
                rec.s_employee_status = 'on_hold'
                if rec.s_is_active:
                    rec.s_is_active = False
            else:
                rec.s_employee_status = 'active'

    @api.onchange('s_minimum_take_home_as_percentage_textbox')
    def _onchange_s_minimum_take_home_as_percentage_textbox(self):
        for rec in self:
            if rec.s_minimum_take_home_as_percentage_textbox:
                rec.s_minimum_take_home = 0

    @api.onchange('s_minimum_take_home')
    def _onchange_s_minimum_take_home(self):
        for rec in self:
            if rec.s_minimum_take_home:
                if rec.s_minimum_take_home_as_percentage:
                    rec.s_minimum_take_home_as_percentage = 0
                    rec.s_minimum_take_home_as_percentage_textbox = ""

    ### end Compensation and Benefits

    # start Government IDs and Tax Information3
    s_sss_number = fields.Integer(string='SSS Number', size=11)
    s_hdmf_number = fields.Integer(string='HDMF Number', size=12)
    s_phic_number = fields.Integer(string='PHIC Number', size=12)
    s_tin = fields.Integer(string='TIN', size=12)
    s_rdo_code = fields.Integer(string='RDO Code', size=4)
    s_sss_mode = fields.Selection([('table_default', 'Table Default'), ('me_table', 'ME Table'), ('manual', 'Manual')],
                                  string='SSS Mode', required=True)
    s_hdmf_mode = fields.Selection(
        [('table', 'Table'), ('manual', 'Manual'), ('me_table', 'ME Table'), ('me_table_manual', 'ME Table Manual'),
         ('table_percentage', 'Table Percentage')], string='HDMF Mode', required=True)
    s_phic_mode = fields.Selection([('me_table', 'ME Table'), ('manual', 'Manual')], string='PHIC Mode', required=True)
    s_whtax_mode = fields.Selection([('table', 'Table')], string='WHTAX Mode', required=True)
    s_sss_manual = fields.Float(string='SSS Manual', size=10)
    s_hdmf_manual = fields.Float(string='HDMF Manual', size=10)
    s_sss_frequency = fields.Selection([('2nd', '2nd'), ('both', 'Both'), ('all', 'All')], string='SSS Frequency',
                                       required=True)
    s_hdmf_frequency = fields.Selection([('2nd', '2nd'), ('both', 'Both'), ('all', 'All')], string='HDMF Frequency',
                                        required=True)
    s_phic_frequency = fields.Selection([('2nd', '2nd'), ('both', 'Both'), ('all', 'All')], string='PHIC Frequency',
                                        required=True)
    s_whtax_frequency = fields.Selection([('2nd', '2nd'), ('both', 'Both'), ('all', 'All')], string='WHTax Frequency',
                                         required=True)
    # end Government IDs and Tax Information

    # start Work Preferences and Attributes
    s_part_time_only = fields.Boolean(string='Part Time Only', default=False)
    s_attendance_base = fields.Boolean(string='Attendance Base', default=True)
    s_ignore_late = fields.Boolean(string='Ignore Late', default=False)
    s_ignore_undertime = fields.Boolean(string='Ignore Undertime', default=False)
    s_ignore_nightdiff = fields.Boolean(string='Ignore Nightdiff', default=False)
    s_no_hours = fields.Float(string='No. Hours', required=True, size=5)
    s_birth_place = fields.Char(string='Birth Place', size=100)
    s_religion = fields.Char(string='Religion', size=100)
    s_nationality = fields.Char(string='Nationality', required=True, size=100)
    s_blood_type = fields.Selection(
        [('a+', 'A+'), ('a-', 'A-'), ('b+', 'B+'), ('b-', 'B-'), ('ab+', 'AB+'), ('ab-', 'AB-'), ('o-', 'O-'),
         ('o+', 'O+')], string='Blood Type')
    s_civil_status = fields.Selection([('single', 'Single'), ('married', 'Married')], string='Civil Status')
    s_spouse_name = fields.Char(string='Spouse name', size=100)
    s_current_address = fields.Char(string='Current Address', size=100)
    s_is_solo_parent = fields.Boolean(string='Is solo parent', default=False)
    s_is_widowed = fields.Boolean(string='Is Widowed', default=False)
    s_current_address_postal_code = fields.Integer(string="Current Address Postal Code", size=5)
    s_permanent_address_postal_code = fields.Integer(string="Permanent Address Postal Code", size=5)

    s_contact_numbers = fields.One2many('s.contact.number', 's_hr_contact_number_id', string="Contact Numbers")
    s_valid_ids = fields.One2many('s.valid.ids', 's_hr_valid_id', string="Valid IDs")
    s_family_members = fields.One2many('s.family.member', 's_hr_family_member', string="Family Members")

    # end Work Preferences and Attributes

    # start Work History and Qualifications
    s_education_ids = fields.One2many('s.education', 's_hr_education_id', string="Education")
    s_external_work_history = fields.One2many('s.external.work.history', 's_hr_external_work_history_id',
                                              string="External Work History")
    s_internal_work_history = fields.One2many('s.internal.work.history', 's_hr_internal_work_history_id',
                                              string="Internal Work History")
    s_license_ids = fields.One2many('s.license', 's_hr_license_id', string="License")
    s_trainings_development = fields.One2many('s.training.development', 's_hr_training_development_id',
                                              string="Trainings & Development")

    # end Work History and Qualifications

    @api.constrains('s_personal_email')
    def _check_s_personal_email(self):
        pattern = "[a-zA-Z0-9._-]+@[a-zA-Z]+\.[a-zA-Z]+"
        for record in self:
            if record.s_personal_email:
                if not re.match(pattern, record.s_personal_email):
                    raise ValidationError("The email address is not valid")

    @api.constrains('s_no_hours')
    def _check_s_no_hours(self):
        for record in self:
            if record.s_no_hours == 0:
                raise ValidationError("The value must be different from 0")

    @api.constrains('s_corporate_email')
    def _check_s_corporate_email(self):
        pattern = "[a-zA-Z0-9._-]+@[a-zA-Z]+\.[a-zA-Z]+"
        for record in self:
            if record.s_corporate_email:
                if not re.match(pattern, record.s_corporate_email):
                    raise ValidationError("The email address is not valid")

    @api.depends('birthday')
    def _compute_age(self):
        time_now = datetime.now()
        for rec in self:
            if rec.birthday:
                rec.s_age = int(time_now.year) - int(rec.birthday.year)
