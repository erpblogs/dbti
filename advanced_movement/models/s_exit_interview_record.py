from odoo import models, fields, api
import re
from datetime import datetime
from odoo.exceptions import ValidationError


class SExitInterviewRecord(models.Model):
    _name = 's.exit.interview.record'
    _inherit = 'survey.survey'

    s_employee_name = fields.Many2one('hr.employee', string='Employee Name', required=True)
    s_employee_id = fields.Integer(string='Employee Id', related='s_employee_name.id', store=True)
    s_company = fields.Char(string='Company', related='s_employee_name.company_id.name', store=True)
    s_exit_type = fields.Selection(
        [('retirement', 'Retirement'), ('resignation', 'Resignation'), ('termination', 'Termination'),
         ('end_of_contract', 'End of Contract')], string='Exit Type')
    s_start_date_in_the_organization = fields.Datetime(string='Start Date in the Organization')
    s_start_date_in_the_position = fields.Datetime(string='Start Date in the Position')
    s_total_length_of_service = fields.Float(string='Total Length of Service', size=5)
    s_other_positions_held = fields.Many2one('hr.job', string='Other Positions Held')
    s_primary_reason_in_leaving_the_organization = fields.Char(string='Primary Reason in Leaving the Organization', size=100)
    s_questionnaire = fields.Many2one('survey.survey', string='Questionnaire', store=True)
    s_amended_from = fields.Boolean(string='Amended From')
