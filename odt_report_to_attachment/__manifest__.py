{
    'name': 'Report To Attachment',
    'version': '1.0',
    'category': 'Helpdesk',
    'description': """

     """,
    'author': "Odootec",
    'website': "http://odootec.com",
    'depends': ['base', 'helpdesk', 'sign','odt_helpdesk_edit'],
    'data': [
        'reports/template.xml',
        'reports/report.xml',
        'views/helpdesk_view.xml',
        'views/users_view.xml',
        'views/web_digital_sign_view.xml'

    ],
    'qweb': ['static/src/xml/digital_sign.xml'],
}
