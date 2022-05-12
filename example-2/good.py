from odoo import models, _
from exceptions import UserError

"""
Code Quality Improvements
-> keep write(...) method reponsibly for only writing data to model
-> extract the statements that checks the active user's active groups into 
descriptive methods on the same model or if they are employed elsewhere in other 
models, then preferably move these methods into a mixin such as UserGroupMixin.
-> simplify complex conditionals by extracting them into methods.
"""


class AccountPaymentSummaryVendorBill(models.Model):
    _name = 'account.payment.summary.vendor.bill'

    def _is_group_originator(self):
        return self.env.\
            user.has_group('account_payment_process.group_payment_originator')

    def _is_group_previewer(self):
        return self.env.\
            user.has_group('account_payment_process.group_payment_reviewer')

    def _is_missing_required_values(self, vals):
        return all([
            "amount" in vals,
            "invoice_id" in vals,
            "acc_amount" in vals,
            "due_date" in vals,
            ])

    def write(self, values):
        if not self._is_group_previewer() or not self._is_group_originator():
            raise UserError(_("Sorry, you don't have the right permissions to perform "
                            "action"))

        if self._is_missing_required_values(values):
            raise UserError(_("Sorry, you failed to provide some required fields."))

        return super(AccountPaymentSummaryVendorBill, self).write(values)