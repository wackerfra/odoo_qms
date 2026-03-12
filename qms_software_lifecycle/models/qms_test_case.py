from odoo import models, fields, api

class QmsTestCase(models.Model):
    _name = 'qms.test_case'
    _description = 'Software Test Case'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='ID / Code', required=True, tracking=True)
    title = fields.Char(string='Title', required=True, tracking=True)
    project_id = fields.Many2one('qms.project', string='QMS Project', required=True, tracking=True)
    
    type = fields.Selection([
        ('functional', 'Functional'),
        ('regression', 'Regression'),
        ('performance', 'Performance'),
        ('security', 'Security'),
        ('usability', 'Usability'),
        ('other', 'Other')
    ], string='Type', default='functional', tracking=True)
    
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High'),
        ('3', 'Critical')
    ], string='Priority', default='1', tracking=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('review', 'In Review'),
        ('approved', 'Approved'),
        ('obsolete', 'Obsolete')
    ], string='Status', default='draft', tracking=True)
    
    pre_conditions = fields.Html(string='Pre-conditions')
    test_steps = fields.Html(string='Test Steps')
    expected_results = fields.Html(string='Expected Results')
    
    requirement_ids = fields.Many2many('qms.requirement', string='Requirements Coverage')
    release_ids = fields.Many2many('qms.release', string='Releases')
    defect_ids = fields.Many2many('qms.defect', string='Known Defects')

    def action_set_draft(self):
        self.ensure_one()
        self.write({'state': 'draft'})

    def action_review(self):
        self.ensure_one()
        self.write({'state': 'review'})

    def action_approve(self):
        self.ensure_one()
        self.write({'state': 'approved'})

    def action_obsolete(self):
        self.ensure_one()
        self.write({'state': 'obsolete'})

    _sql_constraints = [
        ('name_unique', 'unique(name, project_id)', 'Test Case ID must be unique per project!'),
    ]

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, f"[{rec.name}] {rec.title}"))
        return result
