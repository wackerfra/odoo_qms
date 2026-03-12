from odoo import models, fields, api

class QmsBaseline(models.Model):
    _name = 'qms.baseline'
    _description = 'QMS Baseline'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Baseline Name', required=True, tracking=True)
    project_id = fields.Many2one('qms.project', string='QMS Project', required=True, tracking=True)
    
    date = fields.Date(string='Baseline Date', default=fields.Date.context_today)
    description = fields.Text(string='Description')
    
    requirement_ids = fields.Many2many('qms.requirement', string='Requirements Snapshot')
    test_case_ids = fields.Many2many('qms.test_case', string='Test Cases Snapshot')
    document_ids = fields.Many2many('qms.document', string='Documents Snapshot')
    release_id = fields.Many2one('qms.release', string='Related Release')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('locked', 'Locked')
    ], string='Status', default='draft', tracking=True)

    def action_lock(self):
        self.ensure_one()
        self.write({'state': 'locked'})

    def action_set_draft(self):
        self.ensure_one()
        self.write({'state': 'draft'})
