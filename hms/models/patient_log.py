# pyrefly: ignore [missing-import]
from odoo import models, fields

class HmsPatientLog(models.Model):
    _name = 'hms.patient.log'
    _description = 'Patient History Log'
    _order = 'create_date desc'

    description = fields.Text(string='Description', required=True)
    patient_id = fields.Many2one('hms.patient', string='Patient', ondelete='cascade')