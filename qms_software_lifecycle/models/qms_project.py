from odoo import models, fields, api

class QmsProject(models.Model):
    _name = 'qms.project'
    _description = 'QMS Project'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, tracking=True)
    code = fields.Char(string='Code', required=True, tracking=True)
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('archived', 'Archived')
    ], string='Status', default='draft', tracking=True)
    
    project_id = fields.Many2one('project.project', string='Odoo Project')
    partner_id = fields.Many2one('res.partner', string='Customer', tracking=True)
    privacy_visibility = fields.Selection([
        ('followers', 'Invited internal users'),
        ('invited_users', 'Invited internal and portal users'),
        ('employees', 'All internal users'),
        ('portal', 'All internal users and invited portal users'),
    ], string='Visibility', required=True, default='portal', tracking=True)

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

    @api.model_create_multi
    def create(self, vals_list):
        projects = super().create(vals_list)
        for project in projects:
            if project.partner_id:
                project.message_subscribe(partner_ids=project.partner_id.ids)
        return projects

    def write(self, vals):
        res = super().write(vals)
        if 'partner_id' in vals:
            for project in self:
                if project.partner_id:
                    project.message_subscribe(partner_ids=project.partner_id.ids)
        return res

    def _compute_access_url(self):
        for project in self:
            project.access_url = f'/my/qms/projects/{project.id}'

    def action_share_project(self):
        self.ensure_one()
        if self.partner_id:
            self.message_subscribe(partner_ids=self.partner_id.ids)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'portal.share',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_res_model': self._name,
                'default_res_id': self.id,
                'default_partner_ids': [(6, 0, self.partner_id.ids)] if self.partner_id else False,
            },
        }

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
