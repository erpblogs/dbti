# -*- coding: utf-8 -*-

import re
import phonenumbers
from odoo.addons.phone_validation.tools import phone_validation

from odoo import _
from odoo.exceptions import ValidationError


def phone_check(phone_number, country_code=None):
    error_message = _(
            "Please enter the phone number in the correct international format.\n"
            "For example: +84123456789, where +84 is the country code." )
    
    if not phone_number:
        return False

    if not phone_number.startswith('+'):
        phone_number = f'+{phone_number}'
        
    try:
        phone_nbr = phone_validation.phone_parse(phone_number, country_code) # otherwise library not installed
        
    except phonenumbers.phonenumberutil.NumberParseException:
        raise ValidationError(error_message)
    
    if not phonenumbers.is_valid_number(phone_nbr):
            raise ValidationError(error_message)
    
    return True