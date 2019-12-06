from odoo import models, fields, api


class Wizard(models.TransientModel):
    _name = 'odoogoedu.wizard'

    # def _default_session(self):
    #     return self.env['odoogoedu.session'].browse(self._context.get('active_id'))
    def _default_sessions(self):
        return self.env['odoogoedu.session'].browse(self._context.get('active_ids'))

    #操作单个课时
    #session_id = fields.Many2one('odoogoedu.session', string="Session", required=True, default=_default_session)
    #同时操作多个课时
    session_ids = fields.Many2many('odoogoedu.session',string="Sessions", required=True, default=_default_sessions)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")

    # @api.multi
    # def subscribe(self):
    #     self.session_id.attendee_ids |= self.attendee_ids
    #     return {}

    @api.multi
    def subscribe(self):
        for session in self.session_ids:
            session.attendee_ids |= self.attendee_ids
        return {}
