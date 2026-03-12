from odoo import models, fields, api

class QmsDefect(models.Model):
    _name = 'qms.defect'
    _description = 'Software Defect'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='ID', required=True, copy=False, readonly=True, default=lambda self: 'NEW')
    title = fields.Char(string='Title', required=True, tracking=True)
    project_id = fields.Many2one('qms.project', string='QMS Project', required=True, tracking=True)
    
    description = fields.Html(string='Description')
    
    severity = fields.Selection([
        ('0', 'Low'),
        ('1', 'Minor'),
        ('2', 'Major'),
        ('3', 'Critical'),
        ('4', 'Blocker')
    ], string='Severity', default='2', tracking=True)
    
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High'),
        ('3', 'Urgent')
    ], string='Priority', default='1', tracking=True)
    
    state = fields.Selection([
        ('new', 'New'),
        ('analysis', 'In Analysis'),
        ('progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('verified', 'Verified'),
        ('closed', 'Closed'),
        ('rejected', 'Rejected')
    ], string='Status', default='new', tracking=True)
    
    root_cause = fields.Text(string='Root Cause')
    corrective_action = fields.Text(string='Corrective Action')
    preventive_action = fields.Text(string='Preventive Action (CAPA)')
    
    test_run_line_id = fields.Many2one('qms.test_run_line', string='Originating Test Run Line')
    requirement_ids = fields.Many2many('qms.requirement', string='Linked Requirements')
    test_case_ids = fields.Many2many('qms.test_case', string='Linked Test Cases')
    release_ids = fields.Many2many('qms.release', string='Found in Releases')
    
    user_id = fields.Many2one('res.users', string='Assigned To', tracking=True)

    def action_set_draft(self):
        self.ensure_one()
        self.write({'state': 'new'})

    def action_analyze(self):
        self.ensure_one()
        self.write({'state': 'analysis'})

    def action_progress(self):
        self.ensure_one()
        self.write({'state': 'progress'})

    def action_resolve(self):
        self.ensure_one()
        self.write({'state': 'resolved'})

    def action_verify(self):
        self.ensure_one()
        self.write({'state': 'verified'})

    def action_close(self):
        self.ensure_one()
        self.write({'state': 'closed'})

    def action_reject(self):
        self.ensure_one()
        self.write({'state': 'rejected'})

    @api.model
    def create(self, vals):
        if vals.get('name', 'NEW') == 'NEW':
            vals['name'] = self.env['ir.sequence'].next_by_code('qms.defect') or 'DEF-NEW'
        return super(QmsDefect, self).create(vals)
