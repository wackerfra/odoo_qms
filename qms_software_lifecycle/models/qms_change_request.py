from odoo import models, fields, api

class QmsChangeRequest(models.Model):
    _name = 'qms.change_request'
    _description = 'Software Change Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='ID', required=True, copy=False, readonly=True, default=lambda self: 'NEW')
    title = fields.Char(string='Title', required=True, tracking=True)
    project_id = fields.Many2one('qms.project', string='QMS Project', required=True, tracking=True)
    
    description = fields.Html(string='Description')
    
    type = fields.Selection([
        ('feature', 'New Feature'),
        ('defect', 'Defect Fix'),
        ('refactor', 'Refactor'),
        ('risk', 'Risk Mitigation'),
        ('doc', 'Documentation Change')
    ], string='Type', default='feature', tracking=True)
    
    impact_scope = fields.Text(string='Scope Impact')
    impact_risk = fields.Text(string='Risk Impact')
    impact_cost = fields.Float(string='Estimated Cost')
    impact_schedule = fields.Text(string='Schedule Impact')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('review', 'Under Review'),
        ('approved', 'Approved'),
        ('progress', 'In Implementation'),
        ('implemented', 'Implemented'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft', tracking=True)
    
    requirement_ids = fields.Many2many('qms.requirement', string='Requirements')
    defect_ids = fields.Many2many('qms.defect', string='Defects')
    release_ids = fields.Many2many('qms.release', string='Releases')
    document_ids = fields.Many2many('qms.document', string='Documents')
    
    approver_ids = fields.Many2many('res.users', 'qms_change_request_approver_rel', 'cr_id', 'user_id', string='Approvers')

    def action_set_draft(self):
        self.ensure_one()
        self.write({'state': 'draft'})

    def action_review(self):
        self.ensure_one()
        self.write({'state': 'review'})

    def action_approve(self):
        self.ensure_one()
        self.write({'state': 'approved'})

    def action_progress(self):
        self.ensure_one()
        self.write({'state': 'progress'})

    def action_implement(self):
        self.ensure_one()
        self.write({'state': 'implemented'})

    def action_reject(self):
        self.ensure_one()
        self.write({'state': 'rejected'})

    @api.model
    def create(self, vals):
        if vals.get('name', 'NEW') == 'NEW':
            vals['name'] = self.env['ir.sequence'].next_by_code('qms.change_request') or 'CR-NEW'
        return super(QmsChangeRequest, self).create(vals)
