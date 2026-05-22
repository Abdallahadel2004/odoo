{
    'name': 'HMS',
    'version': '1.0',
    'summary': 'Manage patients, history, and medical operations',
    'description': """Hospitals Management System (HMS)""",
    'category': 'Healthcare',
    'author': 'Abdallah',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/patient_views.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
}
