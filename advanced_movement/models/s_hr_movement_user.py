from odoo import models, fields, api


class HrMovementUser(models.Model):
    _name = "hr.movement.user"
    _description = "HR Movement User"

    movement_id = fields.Many2one('hr.movement', string='Movement')
    user_id = fields.Many2one('res.users', string='User')
    status = fields.Selection([
        ('refused', 'Refused'),
        ('approved', 'Approved')
    ], string="Status", tracking=True)
