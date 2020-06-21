{
    'name': 'Report To Attachment',
    'version': '1.0',
    'category': 'Helpdesk',
    'description': """

     """,
    'author': "Odootec",
    'website': "http://odootec.com",
    'depends': ['base', 'helpdesk_timesheet', 'sign', 'odt_helpdesk_edit', 'project','hr'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'wizard/sign_generate_wiz.xml',
        'views/sign_generate.xml',
        'reports/layout.xml',
        'reports/template.xml',
        'reports/report.xml',
        'views/helpdesk_view.xml',
        'views/task_view.xml',
        'views/user_view.xml'
    ],
    'qweb': ['static/src/xml/digital_sign.xml'],
}
