# pyrefly: ignore [missing-import]
from odoo import models, fields, api, _
#pyrefly: ignore [missing-import]
from odoo.exceptions import ValidationError

class HMSPatient(models.Model):
    _name = 'hms.patient'
    _description = 'HMS Patient'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    birth_date = fields.Date(string='Birth Date')
    history = fields.Html(string='Medical History')
    cr_ratio = fields.Float(string='CR Ratio')
    blood_type = fields.Selection([
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')
    ], string='Blood Type')
    pcr = fields.Boolean(string='PCR Status')
    image = fields.Image(string='Patient Image')
    address = fields.Text(string='Address')
    age = fields.Integer(string='Age')


    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], string='State', default='undetermined')


    department_id = fields.Many2one('hms.department', string='Department', domain=[('is_opened', '=', True)])
    doctor_ids = fields.Many2many('hms.doctor', string='Doctors')
    log_ids = fields.One2many('hms.patient.log', 'patient_id', string='Logs')
    department_capacity = fields.Integer(related='department_id.capacity', string='Department Capacity', readonly=True)


    @api.onchange('age')
    def _onchange_age(self):
        if self.age and self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    'title': _("PCR Auto-Checked"),
                    'message': _("The PCR field has checked cause age under 30."),
                    'type': 'notification'
                }
            }

    @api.model_create_multi
    def create(self, vals_list):
        records = super(HMSPatient, self).create(vals_list)
        for record in records:
            record.env['hms.patient.log'].create({
                'patient_id': record.id,
                'description': f"Patient profile created. Initial state set to: {dict(record._fields['state'].selection).get(record.state)}"
            })
        return records

    def write(self, vals):
        if 'state' in vals:
            for record in self:
                old_state_label = dict(record._fields['state'].selection).get(record.state)
                new_state_label = dict(record._fields['state'].selection).get(vals['state'])
                if old_state_label != new_state_label:
                    self.env['hms.patient.log'].create({
                        'patient_id': record.id,
                        'description': f"State changed from {old_state_label} to {new_state_label}"
                    })
        return super(HMSPatient, self).write(vals)