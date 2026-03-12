from odoo import models, fields, api

class QmsRelease(models.Model):
    _name = 'qms.release'
    _description = 'Software Release'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Version Tag', required=True, tracking=True)
    project_id = fields.Many2one('qms.project', string='QMS Project', required=True, tracking=True)
    
    release_date = fields.Date(string='Release Date', tracking=True)
    type = fields.Selection([
        ('major', 'Major'),
        ('minor', 'Minor'),
        ('patch', 'Patch'),
        ('hotfix', 'Hotfix')
    ], string='Release Type', default='minor', tracking=True)
    
    state = fields.Selection([
        ('planned', 'Planned'),
        ('testing', 'In Testing'),
        ('ready', 'Ready for Release'),
        ('released', 'Released'),
        ('deprecated', 'Deprecated')
    ], string='Status', default='planned', tracking=True)
    
    release_notes = fields.Html(string='Release Notes')
    
    requirement_ids = fields.Many2many('qms.requirement', string='Included Requirements')
    test_plan_ids = fields.Many2many('qms.test_plan', string='Test Plans')
    defect_ids = fields.Many2many('qms.defect', string='Resolved Defects')
    change_request_ids = fields.Many2many('qms.change_request', string='Change Requests')
    document_ids = fields.Many2many('qms.document', string='Documents')

    def action_set_planned(self):
        self.ensure_one()
        self.write({'state': 'planned'})

    def action_test(self):
        self.ensure_one()
        self.write({'state': 'testing'})

    def action_ready(self):
        self.ensure_one()
        self.write({'state': 'ready'})

    def action_release(self):
        self.ensure_one()
        self.write({'state': 'released', 'release_date': fields.Date.today()})

    def action_deprecate(self):
        self.ensure_one()
        self.write({'state': 'deprecated'})

    _sql_constraints = [
        ('name_unique', 'unique(name, project_id)', 'Release version must be unique per project!'),
    ]
