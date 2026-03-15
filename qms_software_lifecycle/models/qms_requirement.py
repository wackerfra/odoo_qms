from odoo import models, fields, api

class QmsRequirement(models.Model):
    _name = 'qms.requirement'
    _description = 'Software Requirement'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='ID / Code', required=True, tracking=True)
    title = fields.Char(string='Title', required=True, tracking=True)
    project_id = fields.Many2one('qms.project', string='QMS Project', required=True, tracking=True)
    user_id = fields.Many2one('res.users', string='Responsible', default=lambda self: self.env.user, tracking=True)
    
    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            if record.project_id.partner_id:
                record.message_subscribe(partner_ids=record.project_id.partner_id.ids)
        return records

    def write(self, vals):
        res = super().write(vals)
        if 'project_id' in vals:
            for record in self:
                if record.project_id.partner_id:
                    record.message_subscribe(partner_ids=record.project_id.partner_id.ids)
        return res

    def _compute_access_url(self):
        for requirement in self:
            requirement.access_url = f'/my/qms/requirements/{requirement.id}'

    type = fields.Selection([
        ('business', 'Business'),
        ('functional', 'Functional'),
        ('non-functional', 'Non-Functional'),
        ('compliance', 'Compliance'),
        ('regulatory', 'Regulatory')
    ], string='Type', default='functional', tracking=True)
    
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High'),
        ('3', 'Critical')
    ], string='Priority', default='1', tracking=True)
    
    risk_level = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], string='Risk Level', default='low', tracking=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('review', 'In Review'),
        ('approved', 'Approved'),
        ('implemented', 'Implemented'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft', tracking=True)
    
    description = fields.Html(string='Description')
    acceptance_criteria = fields.Html(string='Acceptance Criteria')
    
    version = fields.Char(string='Version', default='1.0', tracking=True)
    parent_id = fields.Many2one('qms.requirement', string='Parent Requirement')
    child_ids = fields.One2many('qms.requirement', 'parent_id', string='Child Requirements')
    
    specification_ids = fields.Many2many('qms.specification', string='Specifications')
    test_case_ids = fields.Many2many('qms.test_case', string='Test Cases')
    defect_ids = fields.Many2many('qms.defect', string='Defects')
    change_request_ids = fields.Many2many('qms.change_request', string='Change Requests')
    document_ids = fields.Many2many('qms.document', string='Documents')
    release_ids = fields.Many2many('qms.release', string='Releases')
    risk_ids = fields.Many2many('qms.risk', string='Risks')

    def action_set_draft(self):
        self.ensure_one()
        self.write({'state': 'draft'})

    def action_review(self):
        self.ensure_one()
        self.write({'state': 'review'})

    def action_approve(self):
        self.ensure_one()
        self.write({'state': 'approved'})

    def action_implement(self):
        self.ensure_one()
        self.write({'state': 'implemented'})

    def action_verify(self):
        self.ensure_one()
        self.write({'state': 'verified'})

    def action_reject(self):
        self.ensure_one()
        self.write({'state': 'rejected'})

    _sql_constraints = [
        ('name_unique', 'unique(name, project_id)', 'Requirement ID must be unique per project!'),
    ]
    
    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, f"[{rec.name}] {rec.title}"))
        return result
