# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.exceptions import AccessDenied

from odoo import api, models, fields, registry, SUPERUSER_ID


class SResUsers(models.Model):
    _inherit = "res.users"

    s_hr_res_user_id = fields.Many2one('hr.employee', string='Employee')
