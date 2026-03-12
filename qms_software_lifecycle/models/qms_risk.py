from odoo import models, fields, api

class QmsRisk(models.Model):
    _name = 'qms.risk'
    _description = 'Project/Product Risk'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    title = fields.Char(string='Title', required=True, tracking=True)
    project_id = fields.Many2one('qms.project', string='QMS Project', required=True, tracking=True)
    
    description = fields.Text(string='Description')
    
    category = fields.Selection([
        ('technical', 'Technical'),
        ('org', 'Organizational'),
        ('compliance', 'Compliance'),
        ('security', 'Security'),
        ('resource', 'Resource'),
        ('other', 'Other')
    ], string='Category', default='technical', tracking=True)
    
    probability = fields.Selection([
        ('1', 'Low'),
        ('2', 'Medium'),
        ('3', 'High')
    ], string='Probability', default='1', tracking=True)
    
    impact = fields.Selection([
        ('1', 'Low'),
        ('2', 'Medium'),
        ('3', 'High')
    ], string='Impact', default='1', tracking=True)
    
    risk_grade = fields.Char(string='Risk Grade', compute='_compute_risk_grade', store=True)
    
    mitigation_plan = fields.Html(string='Mitigation Plan')
    user_id = fields.Many2one('res.users', string='Owner', default=lambda self: self.env.user, tracking=True)
    
    state = fields.Selection([
        ('identified', 'Identified'),
        ('mitigated', 'Mitigated'),
        ('closed', 'Closed'),
        ('occurred', 'Occurred')
    ], string='Status', default='identified', tracking=True)
    
    requirement_ids = fields.Many2many('qms.requirement', string='Requirements')
    change_request_ids = fields.Many2many('qms.change_request', string='Change Requests')
    release_ids = fields.Many2many('qms.release', string='Releases')

    def action_set_identified(self):
        self.ensure_one()
        self.write({'state': 'identified'})

    def action_mitigate(self):
        self.ensure_one()
        self.write({'state': 'mitigated'})

    def action_occur(self):
        self.ensure_one()
        self.write({'state': 'occurred'})

    def action_close(self):
        self.ensure_one()
        self.write({'state': 'closed'})

    @api.depends('probability', 'impact')
    def _compute_risk_grade(self):
        for rec in self:
            p = int(rec.probability or 1)
            i = int(rec.impact or 1)
            score = p * i
            if score <= 2:
                rec.risk_grade = 'Low'
            elif score <= 4:
                rec.risk_grade = 'Medium'
            else:
                rec.risk_grade = 'High'
