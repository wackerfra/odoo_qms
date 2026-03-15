from odoo import models, fields, api

class QmsTestRun(models.Model):
    _name = 'qms.test_run'
    _description = 'Software Test Run'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, tracking=True)
    test_plan_id = fields.Many2one('qms.test_plan', string='Test Plan', required=True)
    project_id = fields.Many2one('qms.project', related='test_plan_id.project_id', store=True)
    
    date = fields.Date(string='Execution Date', default=fields.Date.context_today)
    environment = fields.Char(string='Environment', default='Staging')
    user_id = fields.Many2one('res.users', string='Executor', default=lambda self: self.env.user)
    
    line_ids = fields.One2many('qms.test_run_line', 'test_run_id', string='Test Results')
    
    summary = fields.Text(string='Result Summary')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ], string='Status', default='draft', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        records = super(QmsTestRun, self).create(vals_list)
        line_vals_list = []
        for record in records:
            if record.test_plan_id:
                for test_case in record.test_plan_id.test_case_ids:
                    line_vals_list.append({
                        'test_run_id': record.id,
                        'test_case_id': test_case.id,
                    })
        if line_vals_list:
            self.env['qms.test_run_line'].create(line_vals_list)
        return records

    def action_pass_all(self):
        self.line_ids.write({'status': 'pass'})

    def action_start(self):
        self.ensure_one()
        self.write({'state': 'in_progress'})

    def action_complete(self):
        self.ensure_one()
        self.write({'state': 'completed'})

    def action_set_draft(self):
        self.ensure_one()
        self.write({'state': 'draft'})

class QmsTestRunLine(models.Model):
    _name = 'qms.test_run_line'
    _description = 'Test Run Line'

    test_run_id = fields.Many2one('qms.test_run', string='Test Run', ondelete='cascade')
    test_case_id = fields.Many2one('qms.test_case', string='Test Case', required=True)
    
    status = fields.Selection([
        ('not_run', 'Not Run'),
        ('pass', 'Pass'),
        ('fail', 'Fail'),
        ('blocked', 'Blocked')
    ], string='Status', default='not_run')
    
    notes = fields.Text(string='Notes')
    defect_ids = fields.Many2many('qms.defect', string='Defects')

    def action_create_defect(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'qms.defect',
            'view_mode': 'form',
            'context': {
                'default_project_id': self.test_run_id.project_id.id,
                'default_title': f"Defect in {self.test_case_id.title}",
                'default_test_run_line_id': self.id,
                'default_requirement_ids': [(6, 0, self.test_case_id.requirement_ids.ids)],
                'default_test_case_ids': [(4, self.test_case_id.id)],
            },
            'target': 'new',
        }
