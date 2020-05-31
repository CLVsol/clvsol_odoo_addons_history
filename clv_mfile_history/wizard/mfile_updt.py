# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class MediaFileUpdate(models.TransientModel):
    _inherit = 'clv.mfile.updt'

    history_marker_id = fields.Many2one(
        comodel_name='clv.history_marker',
        string='History Marker'
    )
    history_marker_id_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='History Marker', default=False, readonly=False, required=False
    )

    # @api.multi
    def do_mfile_updt(self):
        self.ensure_one()

        super(MediaFileUpdate, self).do_mfile_updt()

        for mfile in self.mfile_ids:

            _logger.info(u'%s %s', '>>>>>', mfile.name)

            if self.history_marker_id_selection == 'set':
                mfile.history_marker_id = self.history_marker_id
            if self.history_marker_id_selection == 'remove':
                mfile.history_marker_id = False

        return True
