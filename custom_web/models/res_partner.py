# Part of Odoo. See LICENSE file for full copyright and licensing details.

import re

from odoo import api, models, _
from odoo.addons.custom_tools.tools import phone_validation
from odoo.exceptions import UserError


class Partner(models.Model):
    _inherit = 'res.partner'

    # @api.constrains('phone')
    # def _conchange_phone_validation(self):
    #     for r in self:
    #         if r.phone and not phone_validation.phone_check(r.phone):
    #             raise UserError(_("Phone number is invalid"))
                
    # @api.constrains('mobile')
    # def _conchange_mobile_validation(self):
    #     for r in self:
    #         if r.mobile and not phone_validation.phone_check(r.mobile):
    #             raise  UserError(_("Mobile number is invalid"))