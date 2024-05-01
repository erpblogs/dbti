from odoo import http

class SSettingEmployee(http.Controller):

    @http.route('/employee/template', type='http', auth='user')
    def render_employee_template(self):
        return http.request.render('advanced_employee_manager.template_config_fullname_emp')