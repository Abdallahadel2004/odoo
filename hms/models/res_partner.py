# pyrefly: ignore [missing-import]
from odoo import models, fields, api, _
# pyrefly: ignore [missing-import]
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hms.patient', string='Related Patient')

    @api.constrains('related_patient_id', 'email')
    def _check_patient_email_clash(self):
        for record in self:
            if record.related_patient_id and record.email:
                matching_patient = self.env['hms.patient'].search([
                    ('email', '=', record.email),
                    ('id', '!=', record.related_patient_id.id)
                ], limit=1)
                if matching_patient:
                    raise ValidationError(_("This customer's email already belongs to an existing patient record!"))

    def unlink(self):
        for record in self:
            if record.related_patient_id:
                raise ValidationError(_("You cannot delete a customer record that is linked to an active hospital patient."))
        return super(ResPartner, self).unlink()
        