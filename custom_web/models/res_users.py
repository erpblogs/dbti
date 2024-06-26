# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import contextlib
import logging

from ast import literal_eval
from collections import defaultdict
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError
from odoo.osv import expression
from odoo.tools.misc import ustr
from odoo.http import request

from odoo.addons.auth_signup.models.res_partner import SignupError, now

_logger = logging.getLogger(__name__)

INACTIVE_EMAIL_WARNING = _('This email address is no longer active. Please use a different account to log in.')


class ResUsers(models.Model):
    _inherit = 'res.users'

    state = fields.Selection(selection_add=[('inactive', 'Inactive')])
    user_type = fields.Char(compute='_get_user_type', string="User Type")

    # @api.depends('login')
    # def _compute_login_email(self):
    #     for user in self:
    #         if user.login:
    #             user.email = user.login

    def _get_user_type(self):
        for r in self:
            r.user_type = self.env.ref('base.group_user').name if r._is_internal() else self.env.ref(
                'base.group_portal').name

    def _compute_state(self):
        for user in self:
            if not user.active:
                user.state = 'inactive'
            elif user.login_date:
                user.state = 'active'
            else:
                user.state = 'new'

    def reset_password(self, login):
        """ retrieve the user corresponding to login (login or email),
            and reset their password
        """
        inactive_users = self.search_count([('login', '=', login), ('active', '=', False)])
        if inactive_users:
            raise Exception(INACTIVE_EMAIL_WARNING)

        return super().reset_password(login)