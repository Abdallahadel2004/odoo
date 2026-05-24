{
    'name': 'HMS',
    'version': '1.0',
    'summary': 'Manage patients, history, and medical operations',
    'description': """Hospitals Management System (HMS)""",
    'author': 'Abdallah',
    'depends': ['base','crm'],
    'data': [
        'views/department_views.xml',
        'views/doctor_views.xml',
        'views/patient_views.xml',
        'views/res_partner_views.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
}
