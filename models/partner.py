# -*- coding: utf-8 -*-
from odoo import fields, models


class Partner(models.Model):
    _inherit = 'res.partner'
    instructor = fields.Boolean("老师", default=False)

    session_ids = fields.Many2many('odoogoedu.session', string="出席课时", readonly=True)