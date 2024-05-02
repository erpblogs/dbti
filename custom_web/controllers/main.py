# -*- coding: utf-8 -*-

import logging
import werkzeug
from werkzeug.urls import url_encode

import re
from odoo import tools, http, _
from odoo.http import request

from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression
from odoo.tools.misc import ustr

from odoo.addons.base.models.ir_mail_server import MailDeliveryException
from odoo.addons.auth_signup.models.res_partner import SignupError, now
from odoo.addons.web.controllers.home import ensure_db, Home, SIGN_UP_REQUEST_PARAMS, LOGIN_SUCCESSFUL_PARAMS
from odoo.addons.auth_signup.controllers.main import AuthSignupHome

# from odoo.addons.auth_oauth.controllers.main import OAuthLogin

# from odoo.exceptions import UserError, AccessDenied, ValidationError
# from odoo.addons.auth_signup.models.res_users import SignupError
# 
# from odoo.addons.auth_totp.controllers.home import Home as auth_totp_Home

TRUSTED_DEVICE_COOKIE = 'td_id'
TRUSTED_USER_COOKIE = 'pre_uid'
REMEMBER_COOKIE = 'remember'
TRUSTED_DEVICE_AGE = 90 * 86400

INCORRECT_EMAIL_WARNING = _('Your email was incorrect. Please try again.')
INACTIVE_EMAIL_WARNING = _('This email address is no longer active. Please use a different account to log in.')
WRONG_EMAIL_PASSWORD = _("Wrong email or password. Please try again.")
WRONG_EMAIL_FORMAT = _('Wrong email format. Please try again.')

_logger = logging.getLogger(__name__)


class AuthSignupHome(Home):

    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):

        response = super().web_login(redirect, **kw)

        not_admin = response.qcontext.get('login', '') != 'admin'
        if not_admin and response.qcontext.get('login') and not tools.email_normalize(
                response.qcontext.get('login', '')):
            response.qcontext['account_error'] = WRONG_EMAIL_FORMAT

        elif response.qcontext.get('error') and not request.params.get('oauth_error'):
            response.qcontext['error'] = WRONG_EMAIL_PASSWORD
            if response.qcontext.get('login'):
                user_count = request.env['res.users'].sudo().search([
                    ('login', '=ilike', response.qcontext['login']),
                    ('active', 'in', [True, False])
                ])
                if not user_count:
                    response.qcontext['account_error'] = INCORRECT_EMAIL_WARNING
                elif not user_count.active:
                    response.qcontext['account_error'] = INACTIVE_EMAIL_WARNING

        if kw.get('remember'):
            name = _("%(browser)s on %(platform)s",
                     browser=request.httprequest.user_agent.browser.capitalize(),
                     platform=request.httprequest.user_agent.platform.capitalize(),
                     )

            if request.geoip.city.name:
                name += f" ({request.geoip.city.name}, {request.geoip.country_name})"

            key = request.env['auth_totp.device']._generate("browser", name)
            response.set_cookie(
                key=TRUSTED_DEVICE_COOKIE,
                value=key,
                max_age=TRUSTED_DEVICE_AGE,
                httponly=True,
                samesite='Lax',

            )

            # start thêm remember vào coockies
            response.set_cookie(
                key=REMEMBER_COOKIE,
                value=kw.get('remember'),
                max_age=TRUSTED_DEVICE_AGE,
                httponly=True,
                samesite='Lax',

            )
            # end thêm remember vào coockies

            if request.session.uid:
                response.set_cookie(
                    key=TRUSTED_USER_COOKIE,
                    value=f'{request.session.uid}',
                    max_age=TRUSTED_DEVICE_AGE,
                    httponly=True,
                    samesite='Lax',
                )

            # Crapy workaround for unupdatable Odoo Mobile App iOS (Thanks Apple :@)
            request.session.touch()
        else:
            response.delete_cookie(REMEMBER_COOKIE)

        if not request.session.uid:

            cookies = request.httprequest.cookies
            pre_uid = cookies.get(TRUSTED_USER_COOKIE)
            user = None
            try:
                user = request.env['res.users'].sudo().browse(int(pre_uid))
            except:
                pass
            key = cookies.get(TRUSTED_DEVICE_COOKIE)
            remember = cookies.get(REMEMBER_COOKIE)
            if key and user:
                user_match = request.env['auth_totp.device']._check_credentials_for_uid(
                    scope="browser", key=key, uid=user.id)
                if user_match:
                    if remember:
                        # request.session.finalize(request.env)
                        # kw['login'] = user.login
                        response.qcontext['login'] = user.login
                        response.qcontext['remember'] = True

        return response

    def _prepare_signup_values(self, qcontext):
        values = { key: qcontext.get(key) for key in ('login', 'name', 'password') }
        if not values:
            raise UserError(_("The form was not properly filled in."))
        if values.get('password') != qcontext.get('confirm_password'):
            raise UserError(_("Passwords do not match; please retype them."))
        if values.get('password').isdigit() :
            raise ValidationError("Password must be numbers, letters, or other characters.")
        if len(values.get('password')) < 8:
            raise ValidationError("Password must be more than 8 characters.")
        if values.get('password').islower():
            raise ValidationError("Password must include at least an upper-case character.")
        supported_lang_codes = [code for code, _ in request.env['res.lang'].get_installed()]
        lang = request.context.get('lang', '')
        if lang in supported_lang_codes:
            values['lang'] = lang
        return values

class CustomAuthSignup(AuthSignupHome):

    @http.route('/web/reset_password', type='http', auth='public', website=True, sitemap=False)
    def web_auth_reset_password(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()

        if not qcontext.get('token') and not qcontext.get('reset_password_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                if qcontext.get('token'):
                    self.do_signup(qcontext)
                    return self.web_login(*args, **kw)
                else:
                    login = qcontext.get('login')
                    assert login, _("No login provided.")
                    _logger.info(
                        "Password reset attempt for <%s> by user <%s> from %s",
                        login, request.env.user.login, request.httprequest.remote_addr)
                    if login != 'admin' and not tools.email_normalize(login):
                        qcontext['error'] = _(f'Wrong email format. Please try again.')
                    else:
                        request.env['res.users'].sudo().reset_password(login)
                        qcontext['message'] = _("Verify link has been sent to your email.")
            except UserError as e:
                qcontext['error'] = e.args[0]
            except SignupError:
                qcontext['error'] = _("Could not reset your password")
                _logger.exception('error when resetting password')
            except Exception as e:
                qcontext['error'] = str(e)

        elif 'signup_email' in qcontext:
            user = request.env['res.users'].sudo().search(
                [('email', '=', qcontext.get('signup_email')), ('state', '!=', 'new')], limit=1)
            if user:
                return request.redirect('/web/login?%s' % url_encode({'login': user.login, 'redirect': '/web'}))

        response = request.render('auth_signup.reset_password', qcontext)
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['Content-Security-Policy'] = "frame-ancestors 'self'"
        return response
