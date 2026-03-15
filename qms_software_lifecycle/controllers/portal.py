from odoo import http, _, SUPERUSER_ID
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import AccessError, MissingError
from odoo.http import request

class QmsProjectPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        QmsProject = request.env['qms.project']
        if 'qms_project_count' in counters:
            if QmsProject.check_access_rights('read', raise_exception=False):
                values['qms_project_count'] = QmsProject.search_count([])
            else:
                values['qms_project_count'] = 0
        return values

    def _qms_project_get_page_view_values(self, project, access_token, **kwargs):
        values = {
            'page_name': 'qms_project',
            'project': project,
        }
        return self._get_page_view_values(project, access_token, values, 'my_qms_projects_history', False, **kwargs)

    def _prepare_qms_searchbar_sortings(self):
        return {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
        }

    @http.route(['/my/qms/projects', '/my/qms/projects/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_qms_projects(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        QmsProject = request.env['qms.project']
        domain = []

        searchbar_sortings = self._prepare_qms_searchbar_sortings()
        if not sortby:
            sortby = 'name'
        order = searchbar_sortings[sortby]['order']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # projects count
        qms_project_count = QmsProject.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/qms/projects",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=qms_project_count,
            page=page,
            step=self._items_per_page
        )

        # content according to pager
        projects = QmsProject.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_qms_projects_history'] = projects.ids[:100]

        values.update({
            'date': date_begin,
            'date_end': date_end,
            'projects': projects,
            'page_name': 'qms_project',
            'default_url': '/my/qms/projects',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby
        })
        return request.render("qms_software_lifecycle.portal_my_qms_projects", values)

    @http.route(['/my/qms/projects/<int:project_id>'], type='http', auth="public", website=True)
    def portal_my_qms_project(self, project_id=None, access_token=None, **kw):
        try:
            project_sudo = self._document_check_access('qms.project', project_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        values = self._qms_project_get_page_view_values(project_sudo, access_token, **kw)
        return request.render("qms_software_lifecycle.portal_my_qms_project", values)

    @http.route(['/my/qms/requirements/<int:requirement_id>'], type='http', auth="public", website=True)
    def portal_my_qms_requirement(self, requirement_id=None, access_token=None, **kw):
        try:
            requirement_sudo = self._document_check_access('qms.requirement', requirement_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        values = {
            'page_name': 'qms_requirement',
            'requirement': requirement_sudo,
            'project': requirement_sudo.project_id,
        }
        values = self._get_page_view_values(requirement_sudo, access_token, values, 'my_qms_requirements_history', False, **kw)
        return request.render("qms_software_lifecycle.portal_my_qms_requirement", values)

    @http.route(['/my/qms/requirements/<int:requirement_id>/save'], type='http', auth="user", methods=['POST'], website=True)
    def portal_my_qms_requirement_save(self, requirement_id, **kw):
        try:
            requirement_sudo = self._document_check_access('qms.requirement', requirement_id)
        except (AccessError, MissingError):
            return request.redirect('/my')

        requirement_sudo.write({
            'title': kw.get('title'),
            'description': kw.get('description'),
            'priority': kw.get('priority'),
        })
        return request.redirect(requirement_sudo.access_url)

    @http.route(['/my/qms/defects/<int:defect_id>/save'], type='http', auth="user", methods=['POST'], website=True)
    def portal_my_qms_defect_save(self, defect_id, **kw):
        try:
            defect_sudo = self._document_check_access('qms.defect', defect_id)
        except (AccessError, MissingError):
            return request.redirect('/my')

        defect_sudo.write({
            'title': kw.get('title'),
            'description': kw.get('description'),
            'severity': kw.get('severity'),
            'priority': kw.get('priority'),
        })
        return request.redirect(defect_sudo.access_url)

    @http.route(['/my/qms/projects/<int:project_id>/defect/create'], type='http', auth="user", methods=['POST'], website=True)
    def portal_my_qms_defect_create(self, project_id, **kw):
        try:
            project_sudo = self._document_check_access('qms.project', project_id)
        except (AccessError, MissingError):
            return request.redirect('/my')

        defect = request.env['qms.defect'].sudo().create({
            'title': kw.get('title'),
            'project_id': project_sudo.id,
            'description': kw.get('description'),
            'severity': kw.get('severity'),
            'priority': kw.get('priority'),
        })
        # Add the portal user as a follower if they are not the partner
        defect.message_subscribe(partner_ids=request.env.user.partner_id.ids)
        return request.redirect(defect.access_url)

    @http.route(['/my/qms/defects/<int:defect_id>'], type='http', auth="public", website=True)
    def portal_my_qms_defect(self, defect_id=None, access_token=None, **kw):
        try:
            defect_sudo = self._document_check_access('qms.defect', defect_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        values = {
            'page_name': 'qms_defect',
            'defect': defect_sudo,
            'project': defect_sudo.project_id,
        }
        values = self._get_page_view_values(defect_sudo, access_token, values, 'my_qms_defects_history', False, **kw)
        return request.render("qms_software_lifecycle.portal_my_qms_defect", values)
