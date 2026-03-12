{
    'name': 'QMS for Software Lifecycle',
    'version': '19.0.1.0.0',
    'category': 'Quality/Software',
    'summary': 'Structured, auditable Quality Management System for software companies',
    'description': """
<p>A robust Quality Management System (QMS) specifically designed for software development companies.</p>
<p>It covers the complete software lifecycle, from requirements to final documentation.</p>
<p>ISO 9001 aligned and built for Odoo 19 CE.</p>
    """,
    'author': 'Aries Software',
    'website': 'https://odoo.aries-software.net',
    'depends': ['base', 'mail', 'project'],
    'data': [
        'security/qms_security.xml',
        'security/ir.model.access.csv',
        'views/qms_project_views.xml',
        'views/qms_requirement_views.xml',
        'views/qms_specification_views.xml',
        'views/qms_test_case_views.xml',
        'views/qms_test_plan_views.xml',
        'views/qms_test_run_views.xml',
        'views/qms_defect_views.xml',
        'views/qms_change_request_views.xml',
        'views/qms_release_views.xml',
        'views/qms_document_views.xml',
        'views/qms_risk_views.xml',
        'views/qms_baseline_views.xml',
        'views/qms_menus.xml',
        'data/qms_data.xml',
    ],
    'demo': [
        'data/qms_demo.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'images': ['static/description/banner.png'],
    'price': 199.0,
    'currency': 'EUR',
}
