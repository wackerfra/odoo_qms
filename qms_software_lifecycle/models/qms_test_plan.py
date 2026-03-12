from odoo import models, fields, api

class QmsTestPlan(models.Model):
    _name = 'qms.test_plan'
    _description = 'Software Test Plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, tracking=True)
    project_id = fields.Many2one('qms.project', string='QMS Project', required=True, tracking=True)
    description = fields.Text(string='Description')
    
    scope = fields.Selection([
        ('release', 'Release'),
        ('module', 'Module'),
        ('feature', 'Feature'),
        ('hotfix', 'Hotfix')
    ], string='Scope', default='release', tracking=True)
    
    strategy = fields.Html(string='Strategy / Approach')
    
    release_id = fields.Many2one('qms.release', string='Release')
    test_case_ids = fields.Many2many('qms.test_case', string='Test Cases')
    
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('archived', 'Archived')
    ], string='Status', default='draft', tracking=True)

    def action_activate_plan(self):
        self.ensure_one()
        self.write({'state': 'active'})

    def action_archive_plan(self):
        self.ensure_one()
        self.write({'state': 'archived'})

    def action_set_draft(self):
        self.ensure_one()
        self.write({'state': 'draft'})
