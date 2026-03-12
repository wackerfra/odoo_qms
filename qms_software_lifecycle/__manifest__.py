{
    'name': 'QMS for Software Lifecycle',
    'version': '19.0.1.0.0',
    'category': 'Quality/Software',
    'summary': 'Structured, auditable Quality Management System for software companies',
    'description': """
A robust Quality Management System (QMS) specifically designed for software development companies.
It covers the complete software lifecycle, from requirements to final documentation.

Key Features:
- **Requirements Management**: Business, functional, non-functional, and compliance requirements.
- **Design & Specification**: High-level design and detailed functional/technical specifications.
- **Test Management**: Test plans, test cases, and test run execution with traceability.
- **Issue / Defect Management**: Full defect lifecycle integrated with test execution.
- **Release & Change Management**: Structured release planning and change request workflows.
- **Risk Management**: Track and mitigate technical and organizational risks.
- **Documentation Management**: Versioned QMS documents, including user manuals.
- **ISO 9001 Alignment**: Designed to provide the documented evidence required for ISO 9001 certification.
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
