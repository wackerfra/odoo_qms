from odoo import models, fields, api

class QmsDocument(models.Model):
    _name = 'qms.document'
    _description = 'QMS Document'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    title = fields.Char(string='Title', required=True, tracking=True)
    project_id = fields.Many2one('qms.project', string='QMS Project', required=True, tracking=True)
    
    type = fields.Selection([
        ('req_spec', 'Requirements Specification'),
        ('design_doc', 'Design Document'),
        ('test_plan', 'Test Plan'),
        ('test_report', 'Test Report'),
        ('user_manual', 'User Manual'),
        ('sop', 'Standard Operating Procedure (SOP)'),
        ('template', 'Template'),
        ('other', 'Other')
    ], string='Type', default='other', tracking=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('review', 'In Review'),
        ('approved', 'Approved'),
        ('obsolete', 'Obsolete')
    ], string='Status', default='draft', tracking=True)
    
    version = fields.Char(string='Version', default='1.0', tracking=True)
    
    content = fields.Html(string='Rich Text Content')
    file = fields.Binary(string='Document File')
    file_name = fields.Char(string='File Name')
    
    template_id = fields.Many2one('qms.document', string='Template', domain=[('type', '=', 'template')])
    
    requirement_ids = fields.Many2many('qms.requirement', string='Linked Requirements')
    test_plan_ids = fields.Many2many('qms.test_plan', string='Linked Test Plans')
    release_ids = fields.Many2many('qms.release', string='Linked Releases')
    change_request_ids = fields.Many2many('qms.change_request', string='Linked Change Requests')
    specification_ids = fields.Many2many('qms.specification', string='Linked Specifications')

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
    
    is_user_manual = fields.Boolean(string='Is User Manual', compute='_compute_is_user_manual', store=True)

    @api.depends('type')
    def _compute_is_user_manual(self):
        for rec in self:
            rec.is_user_manual = (rec.type == 'user_manual')
