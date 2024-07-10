# Copyright 2017 Luis M. Ontalba <luis.martinez@tecnativa.com>
# Copyright 2018-2020 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountTax(models.Model):
    _inherit = "account.tax"

    def _selection_operation_key(self):
        return self.env["account.move.line"].fields_get(
            allfields=["l10n_es_aeat_349_operation_key"],
        )["l10n_es_aeat_349_operation_key"]["selection"]

    l10n_es_aeat_349_operation_key = fields.Selection(
        selection=_selection_operation_key,
        string="AEAT 349 Operation key",
        compute="_compute_l10n_es_aeat_349_operation_key",
    )

    def _compute_l10n_es_aeat_349_operation_key(self):
        # TODO: Improve performance
        map_349 = self.env["l10n.es.aeat.map.tax.line"].search(
            [
                (
                    "map_parent_id",
                    "=",
                    self.env.ref("l10n_es_aeat_mod349.aeat_mod349_map").id,
                )
            ]
        )
        for tax in self:
            tax.l10n_es_aeat_349_operation_key = False
            for line in map_349:
                taxes_ids = []
                for tax_template in line.tax_xmlid_ids:
                    tax_id = self.company_id._get_tax_id_from_xmlid(tax_template.name)
                    if tax_id:
                        taxes_ids.append(tax_id)
                if taxes_ids and tax.id in taxes_ids:
                    tax.l10n_es_aeat_349_operation_key = line.field_number
                    break
