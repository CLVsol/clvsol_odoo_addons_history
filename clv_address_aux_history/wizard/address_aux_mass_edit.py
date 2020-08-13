# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AddressAuxMassEdit(models.TransientModel):
    _inherit = 'clv.address_aux.mass_edit'

    phase_id = fields.Many2one(
        comodel_name='clv.phase',
        string='Phase'
    )
    phase_id_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Phase:', readonly=False, required=False
    )

    @api.model
    def default_get(self, field_names):

        defaults = super().default_get(field_names)

        param_value = self.env['ir.config_parameter'].sudo().get_param(
            'clv.global_settings.current_phase_id', '').strip()
        phase_id = False
        if param_value:
            phase_id = int(param_value)

        phase_id_selection = self.env['clv.default_value'].search([
            ('model', '=', 'clv.address_aux'),
            ('parameter', '=', 'mass_edit_phase_id_selection'),
            ('enabled', '=', True),
        ]).value

        defaults['phase_id'] = phase_id
        defaults['phase_id_selection'] = phase_id_selection

        return defaults

    def do_address_aux_mass_edit(self):
        self.ensure_one()

        super().do_address_aux_mass_edit()

        for address_aux in self.address_aux_ids:

            _logger.info(u'%s %s', '>>>>>', address_aux.name)

            if self.phase_id_selection == 'set':
                address_aux.phase_id = self.phase_id
            if self.phase_id_selection == 'remove':
                address_aux.phase_id = False

        return True
