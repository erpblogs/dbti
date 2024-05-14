from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class HrMovement(models.Model):
    _name = "hr.movement"
    _description = "Employee movement"
    _inherit = "mail.thread"
    _order = "movement_type_id"
    _rec_name = "name"

    active = fields.Boolean(default=True)
    name = fields.Char(compute="_compute_name")
    movement_type_id = fields.Many2one("approval.flow", string="Movement Type", required=True)
    used_id = fields.Many2one("res.users", string="Create By", default=lambda self: self.env.user, readonly=True)
    s_employee_name = fields.Many2one('hr.employee', string='Employee Name', required=True)
    s_employee_id = fields.Integer(string='Employee Id', related='s_employee_name.id', store=True)
    s_company = fields.Char(string='Company', related='s_employee_name.company_id.name', store=True)
    posting_date = fields.Datetime(string="Posting Date", default=fields.Datetime.now)
    effective_date = fields.Datetime(string="Effective On", required=True, default=fields.Datetime.now)
    approved_date = fields.Datetime(string='Approved Date', compute="_compute_approved_date", store=True)
    remark = fields.Char(string="Remark", size=100, required=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('to_submit', 'Submit'),
        ('to_approve', 'To Approve'),
        ('refused', 'Refused'),
        ('approved', 'Approved')
    ], string="Status", default="to_submit", required=True, tracking=True)
    department_id = fields.Many2one("hr.department", string="Department ID")
    salary_adjustment_type = fields.Char(string="Salary Adjustment Type")
    retirement_type = fields.Selection([
        ('temporary', 'Temporary'),
        ('lateral', 'Lateral')
    ], string="Retirement Type", tracking=True, default="temporary", required=True
    )
    termination_due_to = fields.Selection([
        ('just_cause', 'Just cause'),
        ('authorized_cause', 'Authorized cause'),
        ('work_abandoment', 'Work Abandonment')
    ], string="Termination Due To", default="just_cause", required=True
    )
    end_of_contract_due_to = fields.Selection([
        ('end_of_probation', 'End of Probation'),
        ('end_of_contract', 'End of Contract')
    ], string="End of Contract Due To", default="end_of_probation", required=True
    )

    current_company = fields.Char(string="Current Company")
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

    current_no_hours = fields.Float(string="Current No.Hours")
    current_period_group = fields.Char(string="Current Period Group")
    current_date_hired = fields.Char(string="Current Date Hired")
    current_rate_classification = fields.Char(string="Current Rate Classification", readonly=True)

    s_new_employee_status = fields.Selection(
        [('active', 'Active'), ('inactive', 'Inactive'), ('retire', 'Retire'), ('resign', 'Resign'),
         ('terminated', 'Terminated'), ('end_of_contract', 'End of contract'), ('on_hold', 'On hold')],
        string="New Employee Status")
    new_job_level_ids = fields.Char(string="New Job Levl")

    new_rate_classification = fields.Char(string="New Rate Classification", readonly=True)
    new_preiod_group = fields.Char(string="New Preiod Group")
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
    new_phic_frequency = fields.Char(String="New PHIC Frequency")
    new_whtax_mode = fields.Char(string="New WHTax Mode")
    new_whtax_frequency = fields.Char(string="New WHTax Mode")
    s_new_date_hired = fields.Datetime(string="New Date Hired")

    s_current_position = fields.Many2one(string="Current Position", related='s_employee_name.s_position_title',
                                         store=True)
    s_type = fields.Selection([('other', 'Other'), ('upgrade', 'Upgrade')], string="Type", default="other")
    s_current_job_level = fields.Many2one(string="Current Job Level", related='s_employee_name.s_job_level', store=True)
    s_current_rate_type = fields.Selection(string="Current Rate Type", related='s_employee_name.s_rate_type',
                                           store=True)
    s_current_rate = fields.Integer(string="Current Rate", related='s_employee_name.s_monthly_rate', store=True)
    s_current_minimum_take_home = fields.Float(string="Current Minimum Take Home",
                                               related='s_employee_name.s_minimum_take_home', store=True)
    s_current_cost_center = fields.Char(string="Current Cost Center", related='s_employee_name.s_cost_center',
                                        store=True)
    s_current_total_year_days = fields.Selection(string="Current Total Year days",
                                                 related='s_employee_name.s_total_year_days', store=True)
    s_current_other = fields.Float(string='Other', related='s_employee_name.s_other', store=True)
    s_current_is_other = fields.Boolean(string='Is Other', related='s_employee_name.s_is_other', store=True)
    s_current_no_hours = fields.Float(string="Current No. Hours", related='s_employee_name.s_no_hours', store=True)
    s_current_period_group = fields.Char(string="Current Period Group", readonly=1)
    s_new_period_group = fields.Char(string="New Period Group", readonly=1)
    s_current_job_grade = fields.Char(string="Current Job Grade", readonly=1)
    s_new_job_grade = fields.Char(string="New Job Grade", readonly=1)
    s_current_payroll_schedule = fields.Selection(string="Current Payroll Schedule",
                                                  related='s_employee_name.s_payroll_schedule', store=True)
    s_current_attendance_based = fields.Boolean(string="Current Attendance Based",
                                                related='s_employee_name.s_attendance_base', store=True)
    s_new_job_level = fields.Many2one('hr.job.level', string="New Job Level")
    s_new_position_title = fields.Many2one('hr.job', string="New Position Title")
    s_new_rate_type = fields.Selection(
        [('hourly_rate', 'Hourly Rate'), ('daily_rate', 'Daily Rate'), ('monthly_rate', 'Monthly Rate')],
        string="New Rate Type")
    s_new_rate = fields.Integer(string="New Rate", required=True, size=12)
    s_new_minimum_take_home = fields.Float(string="New Minimum Take Home", required=True, size=15)
    s_new_cost_center = fields.Char(string="New Cost Center", size=50)
    s_new_total_year_days = fields.Selection(
        [('365', '365'), ('313', '313'), ('312', '312'), ('264', '264'), ('261', '261'), ('394.4', '394.4'),
         ('other', 'Other')], string="New Total Year days")
    s_is_other_total_year_days = fields.Boolean(string="Is Other Total Year days")
    s_other_total_year_days = fields.Float(string="Other Total Year days")
    s_new_no_hours = fields.Float(string="New No. Hours", required=True, size=5)
    # s_new_period_group = fields.
    s_new_payroll_schedule = fields.Selection(
        [('semi_monthly', 'Semi-Monthly'), ('monthly', 'Monthly'), ('weekly', 'Weekly')], string="New Payroll Schedule")
    s_is_processed = fields.Boolean(string="Is Processed", default=False)
    s_current_department = fields.Many2one(string="Current Department", related='s_employee_name.s_department',
                                           store=True)
    s_transfer_type = fields.Selection([('temporary', 'Temporary'), ('lateral', 'Lateral')], string="Transfer Type")
    s_salary_adjustment_type = fields.Selection(
        [('merit_increase', 'Merit Increase'), ('salary_adjustment', 'Salary Adjustment'),
         ('promotional_increase', 'Promotional Increase')], string="Salary Adjustment Type")
    s_current_location = fields.Many2one(string="Current Location", related='s_employee_name.s_location', store=True)
    s_current_date_hired = fields.Date(string="Current Date Hired", related='s_employee_name.s_date_hired',
                                           store=True)
    s_new_end_of_contract = fields.Datetime(string="New End of Contract")
    s_new_end_of_contract = fields.Datetime(string="New End of Contract")
    s_current_end_of_contract_date = fields.Char("Current End of Contract Date",readonly=True)
    s_current_employee_status = fields.Selection(string="Current Employment Status",
                                                 related='s_employee_name.s_employee_status', store=True)
    s_new_company = fields.Many2one('res.company', string="New Company")
    s_new_department = fields.Many2one('hr.department', string="New Department")
    s_new_location = fields.Many2one('hr.work.location', string="New Location")
    is_type_job_rotation_request = fields.Boolean(string="Is Type Job Rotation Request")
    is_type_regularization_request = fields.Boolean(string="Is Type Regularization Request")
    is_type_transfer_request = fields.Boolean(string="Is Type Transfer Request")
    is_type_salary_adjustment_request = fields.Boolean(string="Is Type Salary Adjustment request")
    is_type_extension_of_service_request = fields.Boolean(string="Is Type Extension of Service request")

    # start field dùng để ẩn button
    is_invisible_button = fields.Boolean(string="Is Invisible Button", compute="_compute_invisible_button")
    action_user_ids = fields.One2many('hr.movement.user', 'movement_id', string='Action Users')

    # end field dùng để ẩn button

    # start logic màn job_rotation_request
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
            if rec.s_new_no_hours == 0 and (rec.is_type_job_rotation_request or rec.is_type_regularization_request):
                raise ValidationError("The value of Hours must be different from 0.")

    @api.onchange('movement_type_id')
    def onchange_movement_type_id(self):
        for rec in self:
            rec.is_type_job_rotation_request = False
            rec.is_type_regularization_request = False
            rec.is_type_transfer_request = False
            rec.is_type_salary_adjustment_request = False
            if rec.movement_type_id.is_type_job_rotation_request:
                rec.is_type_job_rotation_request = True
            elif rec.movement_type_id.is_type_regularization_request:
                rec.is_type_regularization_request = True
            elif rec.movement_type_id.is_type_transfer_request:
                rec.is_type_transfer_request = True
            elif rec.movement_type_id.is_type_salary_adjustment_request:
                rec.is_type_salary_adjustment_request = True
            elif rec.movement_type_id.is_type_extension_of_service_request:
                rec.is_type_extension_of_service_request = True

    # end logic màn job_rotation_request

    @api.depends('movement_type_id', 'used_id')
    def _compute_name(self):
        for r in self:
            r.name = str(r.used_id.name) + ' on ' + str(r.movement_type_id.movement_type)

    @api.depends('status')
    def _compute_approved_date(self):
        approved_date = fields.Datetime.now()
        for r in self:
            if r.status == "approved":
                r.approved_date = approved_date

    @api.depends('status')
    def _compute_employee_status(self):
        for r in self:
            if r.status != "approved":
                r.current_employee_status = r.s_employee_name.s_employee_status
            else:
                if r.approved_date < r.effective_date:
                    r.current_employee_status = r.s_employee_name.s_employee_status
                else:
                    movement_type = r.movement_type_id.movement_type
                    if movement_type == "Retirement":
                        r.s_employee_name.write({'s_employee_status': 'retire'})
                        r.current_employee_status = r.s_employee_name.s_employee_status
                    if movement_type == "Resignation":
                        r.s_employee_name.write({'s_employee_status': 'resign'})
                        r.current_employee_status = r.s_employee_name.s_employee_status
                    if movement_type == "Termination":
                        r.s_employee_name.write({'s_employee_status': 'terminated'})
                        r.current_employee_status = r.s_employee_name.s_employee_status
                    if movement_type == "End of Contract":
                        r.s_employee_name.write({'s_employee_status': 'end_of_contract'})
                        r.current_employee_status = r.s_employee_name.s_employee_status

    # start logic button movement
    def create(self, vals):
        res = super(HrMovement, self).create(vals)
        if res.movement_type_id:
            movement_type_id = res.movement_type_id
            if movement_type_id.stage_id:
                stage_id = movement_type_id.stage_id
                if stage_id.user_ids:
                    approvers = stage_id.user_ids
                    if approvers:
                        for approver in approvers:
                            res.action_user_ids = [(0, 0, {'user_id': approver.id})]
        return res

    @api.depends('movement_type_id')
    def _compute_invisible_button(self):
        for rec in self:
            rec.is_invisible_button = False
            if rec.movement_type_id and rec.status not in ['refused', 'approved'] and rec.status == 'to_approve':
                stage_id = rec.movement_type_id.stage_id.sorted('sequence')
                if stage_id and stage_id.user_ids:
                    ids_approve = stage_id.user_ids.ids
                    user_id = rec.env.uid
                    if user_id in ids_approve:
                        index_user_id = ids_approve.index(user_id)
                        if rec.movement_type_id.sequence:
                            count = sum(1 for i in range(0, index_user_id) if rec.action_user_ids.filtered(
                                lambda r: r.user_id == stage_id.user_ids[i] and r.status == 'approved'))
                            if count == index_user_id and not rec.action_user_ids.filtered(
                                    lambda r: r.user_id.id == rec.env.uid and r.status):
                                rec.is_invisible_button = True
                        elif rec.movement_type_id.parallel:
                            rec.is_invisible_button = True
                else:
                    rec.write({'status': 'approved'})

    def action_draft_movement(self):
        for r in self:
            if r.status != 'refused':
                raise UserError(_("You can not approve while its status is not Refused."))
        self.write({'status': 'to_submit'})
        return True

    def action_confirm_movement(self):
        for rec in self:
            if rec.status != 'to_submit':
                raise UserError(_("You can not approve while its status is not Submit."))
            rec.action_user_ids.write({'status': False})
        self.write({'status': 'to_approve'})
        return True

    def action_approved_movement(self):
        for rec in self:
            user = rec.action_user_ids.filtered(lambda r: r.user_id == rec.env.user)
            if user:
                user.status = 'approved'
            all_status_user = rec.action_user_ids.mapped('status')
            if all([status == 'approved' for status in all_status_user]):
                rec.write({'status': 'approved'})
        return True

    def action_refused_movement(self):
        for rec in self:
            user = rec.action_user_ids.filtered(lambda r: r.user_id == rec.env.user)
            if user:
                user.status = 'refused'
            all_status_user = rec.action_user_ids.mapped('status')
            if ([status == 'refused'] for status in all_status_user):
                rec.write({'status': 'refused'})
        return True
    # end logic button movement
