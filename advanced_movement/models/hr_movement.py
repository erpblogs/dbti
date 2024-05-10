from odoo import models, fields, api, _
from odoo.exceptions import UserError


class HrMovement(models.Model):
    _name = "hr.movement"
    _description = "Employee movement"
    _inherit = "mail.thread"
    _order = "movement_type_id"
    _rec_name= "name"
    
    active = fields.Boolean(default=True)
    name = fields.Char(compute="_compute_name")
    movement_type_id = fields.Many2one("approval.flow", string="Movement Type", required=True)
    used_id = fields.Many2one("res.users", string="Create By", default=lambda self: self.env.user, readonly=True)
    employee_id = fields.Many2one("hr.employee", string="Employee", required=True)
    employeeid = fields.Char(string="Employee ID", compute="_compute_employee_id", store=True)
    employee_name = fields.Char(string="Employee Name", related="employee_id.name", store=True, depends=['employee_id'])
    posting_date = fields.Datetime(string="Posting Date", default=fields.Datetime.now)
    effective_date = fields.Datetime(string="Effective On", required=True, default=fields.Datetime.now)
    approved_date = fields.Datetime(string='Approved Date', compute="_compute_approved_date", store=True)
    remark = fields.Char(string="Remark", size=100, required=True)
    status = fields.Selection([
        ('draft','Draft'),
        ('to_submit','Submit'),
        ('to_approve','To Approve'),
        ('refused','Refused'),
        ('approved','Approved')
        ], string="Status", default="draft", required=True, tracking=True
    )
    company_id = fields.Many2one("res.company", string="Company", compute="_compute_employee_id", store=True)
    type = fields.Selection([
        ('other','Other'),
        ('upgrade','Upgrade')
        ], string="Type", default="other", required=True, tracking=True
    )
    department_id = fields.Many2one("hr.department", string="Department ID")
    salary_adjustment_type = fields.Char(string="Salary Adjustment Type")
    retirement_type = fields.Selection([
        ('temporary','Temporary'),
        ('lateral','Lateral')
        ], string="Retirement Type", tracking=True, default="temporary", required=True
    )
    termination_due_to = fields.Selection([
        ('just_cause','Just cause'),
        ('authorized_cause','Authorized cause'),
        ('work_abandoment','Work Abandonment')
        ], string="Termination Due To", default="just_cause", required=True
    )
    end_of_contract_due_to = fields.Selection([
        ('end_of_probation','End of Probation'),
        ('end_of_contract','End of Contract')
        ], string="End of Contract Due To", default="end_of_probation", required=True
    )

    current_company = fields.Char(string="Current Company")
    current_department = fields.Char(string="Current Department") 
    current_job_grade = fields.Char(string="Current Job Grade")
    current_location = fields.Char(string="Current Location")
    current_position_title = fields.Char(string="Current Position Title")
    current_employee_status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('retire', 'Retire'),
        ('resign', 'Resign'),
        ('terminated', 'Terminated'),
        ('end_of_contract', 'End of contract'),
        ('on_hold', 'On hold')
        ], string='Current Employee Status', compute='_compute_employee_status', store=True
    )
   
    current_position = fields.Char(string="Current Position")
    current_job_level = fields.Char(string="Current Job Level")
    current_rate = fields.Integer(string="Current Rate")
    current_minimum_take_home = fields.Float(string="Current Minimum Take Home")
    current_cost_center = fields.Integer(string="Current Cost Center")
    current_total_year_days = fields.Float(string="Current Total Year Days")
    current_no_hours = fields.Float(string="Current No.Hours")
    current_rate_classification = fields.Char(string="Current Rate Classification")
    current_period_group = fields.Char(string="Current Period Group")
    current_payroll_schedule = fields.Char(string="Current Payroll Schedule")
    current_attendance_based = fields.Boolean(string="Current Attendance Based")
    current_date_hired = fields.Char(string="Current Date Hired")
    
    new_company = fields.Char(string="New Company")
    new_department = fields.Char(string="New Department") 
    new_job_grade = fields.Char(string="New Job Grade")
    new_location = fields.Char(string="New Location")
    new_position_title = fields.Char(string="New Position Title")
    new_employee_status = fields.Char(string="New Employee Status")
    new_position_title_ids = fields.Char(string="New Position Title")
    new_job_level_ids = fields.Char(string="New Job Levl")
    new_rate_type = fields.Selection([
        ('hourly_rate','Hourly Rate'),
        ('daily_rate','Daily Rate'),
        ('monthly_rate','Monthly Rate')
        ], string="New Rate Type", tracking=True, required=True, default="hourly_rate"
    )
    new_rate = fields.Integer(string="New Rate")
    new_minimum_take_home = fields.Float(string="New Minimum Take Home")
    new_cost_center = fields.Integer(string="New Cost Center")
    new_total_year_days = fields.Float(string="New Total Year Days")
    new_no_hours = fields.Float(string="New No.Hours")
    new_rate_classification = fields.Char(string="New Rate Classification")
    new_preiod_group = fields.Char(string="New Preiod Group")
    new_payroll_schedule = fields.Selection([
        ('semi_monthly','Semi-Monthly'),
        ('monthly','Monthly'),
        ('weekly','Weekly')
        ], string="New Payroll Schedule", tracking=True
    )
    new_business_email = fields.Char(string="New Business Email")
    new_personal_email = fields.Char(string="New Personal Email")
    new_biometrics_id = fields.Char(string="New Biometrics ID")
    new_role_profile = fields.Char(string="New Role Profile")
    new_project = fields.Char(string="New Project")
    new_sss_mode = fields.Char(string="New SSS Mode")
    new_sss_frequency = fields.Char(string="New SSS Frequency")
    new_hdmf_mode = fields.Char(string="New HDMF Mode")
    new_hdmf_frequency = fields.Char(string="New HDMF Frequency")
    new_phic_mode = fields.Char(String="New PHIC Mode")
    new_phic_frequency= fields.Char(String="New PHIC Frequency")
    new_whtax_mode = fields.Char(string="New WHTax Mode")
    new_whtax_frequency = fields.Char(string="New WHTax Mode")
    new_date_hired = fields.Char(string="New Date Hired")
    
    amended_from = fields.Boolean(string="Amended From")
    is_processed = fields.Boolean(string="Is Processed")

    
    @api.depends('movement_type_id','used_id')
    def _compute_name(self):
        for r in self:
            r.name = str(r.used_id.name) + ' on ' + str(r.movement_type_id.movement_type)
            
    @api.depends('employee_id')
    def _compute_employee_id(self):
        for r in self:
            if r.employee_id:
                r.company_id = r.employee_id.company_id
                r.employeeid = r.employee_id.id

    def action_to_submit_movement(self):
        for r in self:
            if r.status != 'draft':
                raise UserError(_("You can not submit  while its status is not Draft."))
        self.write({'status': 'to_submit'})
        return True

    def action_to_approve_movement(self):
        for r in self:
            if r.status != 'to_submit':
                raise UserError(_("You can not approve while its status is not Submit."))
        self.write({'status': 'to_approve'})
        return True

    
    def action_approved_movement(self):
        for r in self:
            if r.status != 'to_approve':
                raise UserError(_("You can not set approved while its status is not Approve."))
        self.write({'status': 'approved'})
    
    @api.depends('status')
    def _compute_approved_date(self):
        approved_date = fields.Datetime.now()
        for r in self:
            if r.status == "approved":
                r.approved_date = approved_date

    @api.depends('status','employee_id')
    def _compute_employee_status(self):
        current_emp_status = self.employee_id.s_employee_status
        for r in self:
            if r.status != "approved":
                r.employee_id.write({'s_employee_status': 'retire'})
                r.current_employee_status = r.employee_id.s_employee_status
            else:
                if  r.approved_date < r.effective_date:
                    r.current_employee_status = r.employee_id.s_employee_status
                else:
                    r.employee_id.write({'s_employee_status': 'active'})
                    r.current_employee_status = r.employee_id.s_employee_status

    def action_draft_movement(self):
        for r in self:
            if r.status != 'refused':
                raise UserError(_("You can not Reset to Draft while its status is not Refused."))
        self.write({'status': 'draft'})
        return True

    def action_refused_movement(self):
        for r in self:
            if r.status in ['draft', 'refused']:
                raise UserError(_("You can not refused while its status is not To Approve or Approve or Approved."))
        self.write({'status': 'refused'})
        return True
