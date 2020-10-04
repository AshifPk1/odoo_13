# See LICENSE file for full copyright and licensing details.

{
    'name': 'Odoo Whatsapp Integration',
    'summary': 'This module is used for Whatsapp Connection.',
    'version': '13.0.1.0.0',
    'license': 'LGPL-3',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'website': 'http://www.serpentcs.com',
    'description': """
		This module is used for Whatsapp Connection.
        Odoo Whatsapp Integration
		Whatsapp odoo Integration
		whatsapp integration in odoo 
		whatsapp integration with odoo 
		Odoo Whatsapp Connector
		odoo whatsapp integration app
		odoo whatsapp connector code
		odoo whatsapp connector github
		odoo whatsapp connector guide
		odoo whatsapp connector key
		odoo whatsapp connector list
		odoo whatsapp connector location
		odoo whatsapp connector online
		odoo whatsapp connector tutorial
		Sale Odoo Whatsapp Integration
		Sale Odoo Whatsapp Connector
		Stock Odoo WhatsApp Integration
		Stock Odoo WhatsApp Connector
		Account Odoo Whatsapp Integration
		Account Odoo Whatsapp Connector
		HR Odoo WhatsApp Integration
		HR Odoo WhatsApp Connector
		HR Payroll Odoo WhatsApp Integration
		HR Payroll Odoo WhatsApp Connector
		Odoo Whatsapp Integration
		Integration of odoo Whatsapp
		Whatsapp livechat
		Whatsapp odoo Integration
		WhatsApp Odoo Integration
		Integrate Odoo with WhatsApp
		whatsapp connector
		Whatsapp integration
		odoo whatsapp
		whatsapp odoo
		Whatsapp
    """,
    'sequence': 1,
    'category': 'Extra Tools',
    'depends': [
        'contacts'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/whatsapp_error_log_cron.xml',
        'views/res_company_view.xml',
        'views/res_partner_view.xml',
        'views/whatsapp_message_log_view.xml',
        'views/mail_template.xml',
        'wizard/whatsapp_message_view.xml',
    ],
    'images': ['static/description/odoo-whatsapp-main.gif'],
    'installable': True,
    'price': 79,
    'external_dependencies': {'python': ['phonenumbers']},
    'currency': 'EUR'
}
