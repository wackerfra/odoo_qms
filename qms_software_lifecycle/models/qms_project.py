from odoo import models, fields, api

class QmsProject(models.Model):
    _name = 'qms.project'
    _description = 'QMS Project'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, tracking=True)
    code = fields.Char(string='Code', required=True, tracking=True)
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('archived', 'Archived')
    ], string='Status', default='draft', tracking=True)
    
    project_id = fields.Many2one('project.project', string='Odoo Project')
    quality_objectives = fields.Html(string='Quality Objectives')
    
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    user_id = fields.Many2one('res.users', string='Quality Manager', default=lambda self: self.env.user, tracking=True)

    requirement_ids = fields.One2many('qms.requirement', 'project_id', string='Requirements')
    specification_ids = fields.One2many('qms.specification', 'project_id', string='Specifications')
    test_case_ids = fields.One2many('qms.test_case', 'project_id', string='Test Cases')
    test_plan_ids = fields.One2many('qms.test_plan', 'project_id', string='Test Plans')
    defect_ids = fields.One2many('qms.defect', 'project_id', string='Defects')
    change_request_ids = fields.One2many('qms.change_request', 'project_id', string='Change Requests')
    release_ids = fields.One2many('qms.release', 'project_id', string='Releases')
    document_ids = fields.One2many('qms.document', 'project_id', string='Documents')
    risk_ids = fields.One2many('qms.risk', 'project_id', string='Risks')
    baseline_ids = fields.One2many('qms.baseline', 'project_id', string='Baselines')

    def action_activate_project(self):
        self.ensure_one()
        self.write({'state': 'active'})

    def action_archive_project(self):
        self.ensure_one()
        self.write({'state': 'archived'})

    def action_set_draft(self):
        self.ensure_one()
        self.write({'state': 'draft'})

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Project code must be unique!'),
    ]
