from odoo import models, fields, api

class QmsSpecification(models.Model):
    _name = 'qms.specification'
    _description = 'Software Specification'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    title = fields.Char(string='Title', required=True, tracking=True)
    project_id = fields.Many2one('qms.project', string='QMS Project', required=True, tracking=True)
    
    type = fields.Selection([
        ('hld', 'High-Level Design'),
        ('lld', 'Detailed Design'),
        ('interface', 'Interface Specification'),
        ('technical', 'Technical Specification'),
        ('functional', 'Functional Specification')
    ], string='Type', default='functional', tracking=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('review', 'In Review'),
        ('approved', 'Approved'),
        ('obsolete', 'Obsolete')
    ], string='Status', default='draft', tracking=True)
    
    content = fields.Html(string='Content')
    version = fields.Char(string='Version', default='1.0', tracking=True)
    
    requirement_ids = fields.Many2many('qms.requirement', string='Requirements')
    document_ids = fields.Many2many('qms.document', string='Documents')
    change_request_ids = fields.Many2many('qms.change_request', string='Change Requests')

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
