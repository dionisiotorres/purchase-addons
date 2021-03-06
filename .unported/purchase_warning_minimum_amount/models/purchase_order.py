# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-v3).

from odoo import models, fields, api


class PurchaseOrder(models.Model):

    _inherit = "purchase.order"

    min_purchase_amount = fields.Float(
        string="Minimum Purchase amount", related="partner_id.min_purchase_amount"
    )

    def display_alert_wizard(self, context):
        view = self.env.ref("purchase_warning_minimum_amount.wizard_alert_message")
        wiz = self.env["wizard.alert"].create({"order_id": self.id})
        return {
            "name": "Warning",
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "wizard.alert",
            "views": [(view.id, "form")],
            "view_id": view.id,
            "target": "new",
            "res_id": wiz.id,
            "context": context,
        }

    @api.multi
    def button_confirm(self):
        context = self._context.copy()
        if context.get("confirm_order", False):
            return super(PurchaseOrder, self).button_confirm()
        if self.amount_untaxed < self.min_purchase_amount:
            context.update({"to_confirm": True})
            return self.display_alert_wizard(context)
        return super(PurchaseOrder, self).button_confirm()

    @api.multi
    def button_approve(self, force=False):
        context = self._context.copy()
        if context.get("confirm_order", False):
            return super(PurchaseOrder, self).button_approve(force)
        if self.amount_untaxed < self.min_purchase_amount:
            context.update({"to_approve": True})
            return self.display_alert_wizard(context)
        return super(PurchaseOrder, self).button_approve(force)
