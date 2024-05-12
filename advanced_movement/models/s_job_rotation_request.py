from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SJobRotationRequest(models.Model):
    _name = "s.job.rotation.request"
    _description = "Job Rotation Request"
    _inherit = "survey.survey"

    s_employee_name = fields.Many2one('hr.employee', string='Employee Name', required=True)
    s_employee_id = fields.Integer(string='Employee Id', related='s_employee_name.id', store=True)
    s_company = fields.Char(string='Company', related='s_employee_name.company_id.name', store=True)
    s_effective_on = fields.Datetime(string='Effective On', required=True)
    s_type = fields.Selection([('other', 'Other'), ('upgrade', 'Upgrade')], string="Type", required=True)
    s_remark = fields.Char(string='Remark', size=100, required=True)
    s_current_position = fields.Many2one(string="Current Position", related='s_employee_name.s_position_title', store=True)
    s_current_job_level = fields.Many2one(string="Current Job Level", related='s_employee_name.s_job_level', store=True)
    s_current_rate_type = fields.Selection(string="Current Rate Type", related='s_employee_name.s_rate_type', store=True)
    s_current_rate = fields.Integer(string="Current Rate", related='s_employee_name.s_monthly_rate', store=True)
    s_current_minimum_take_home = fields.Float(string="Current Minimum Take Home",
                                              related='s_employee_name.s_minimum_take_home', store=True)
    s_current_cost_center = fields.Char(string="Current Cost Center", related='s_employee_name.s_cost_center',
                                        store=True)
    s_current_total_year_days = fields.Selection(string="Current Total Year days",
                                            related='s_employee_name.s_total_year_days', store=True)
    s_current_no_hours = fields.Float(string="Current No. Hours", related='s_employee_name.s_no_hours', store=True)
    # s_current_period_group = fields.Char(string="Current Period Group", related='s_employee_name.s_period_group', store=True)
    s_current_payroll_schedule = fields.Selection(string="Current Payroll Schedule",
                                             related='s_employee_name.s_payroll_schedule', store=True)
    # s_current_attendance_based = fields.Boolean(string="Current Attendance Based", related='s_employee_name.s_payroll_schedule', store=True)
    # s_new_job_level = fields.Boolean(string="New Job Level", related='s_employee_name.s_payroll_schedule', store=True)
    # s_new_position_title = fields.Boolean(string="New Position Title", related='s_employee_name.s_payroll_schedule', store=True)
    s_new_rate_type = fields.Selection(
        [('hourly_rate', 'Hourly Rate'), ('daily_rate', 'Daily Rate'), ('monthly_rate', 'Monthly Rate')],
        string="New Rate Type", required=True)
    s_new_rate = fields.Integer(string="New Rate", required=True, size=12)
    s_new_minimum_take_home = fields.Float(string="New Minimum Take Home", required=True, size=15)
    s_new_cost_center = fields.Char(string="New Cost Center", required=True, size=50)
    s_new_total_year_days = fields.Selection(
        [('365', '365'), ('313', '313'), ('312', '312'), ('264', '264'), ('261', '261'), ('394.4', '394.4'),
         ('other', 'Other')], string="New Total Year days", required=True)
    s_is_other_total_year_days = fields.Boolean(string="Is Other Total Year days")
    s_other_total_year_days = fields.Float(string="Other Total Year days")
    s_new_no_hours = fields.Float(string="New No. Hours", required=True, size=5)
    # s_new_period_group = fields.
    s_new_payroll_schedule = fields.Selection(
        [('semi_monthly', 'Semi-Monthly'), ('monthly', 'Monthly'), ('weekly', 'Weekly')], string="New Payroll Schedule",
        required=True)
    s_is_processed = fields.Boolean(string="Is Processed", default=False)

    @api.constrains('s_other_total_year_days')
    def constrain_s_other_total_year_days(self):
        for rec in self:
            if rec.s_new_total_year_days == 'other' and rec.s_other_total_year_days <= 0 and rec.s_is_other_total_year_days:
                raise ValidationError("The value of Total Days in the Year must be greater than 0.")

    @api.onchange('s_new_total_year_days')
    def onchange_s_new_total_year_days(self):
        for rec in self:
            if rec.s_new_total_year_days == 'other':
                rec.s_is_other_total_year_days = True
            else:
                rec.s_is_other_total_year_days = False

    @api.constrains('s_new_no_hours')
    def constrain_s_new_no_hours(self):
        for rec in self:
            if rec.s_new_no_hours == 0:
                raise ValidationError("The value of Hours must be different from 0.")
