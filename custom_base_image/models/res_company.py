from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Company(models.Model):
    _inherit = 'res.company'

    custom_image_1920 = fields.Image(string="Image")

    @api.onchange('custom_image_1920')
    def _onchange_custom_image_1920(self):
        for record in self:
            if record.custom_image_1920:
                byte_data = str(record.custom_image_1920)
                jpeg="b'/9j/"
                png="b'iVBO"
                if not (byte_data.startswith(png,0,6) or byte_data.startswith(jpeg,0,6)):
                    raise ValidationError("The uploaded file is not a supported format. Please upload a suitable file type jpeg or png.")
