from odoo import models
from exceptions import UserError

"""
Code Quality Issues:

-> write(...) method appears cluttered
-> write(...) method appears to be concerned with more than it responsibly for
--> determining the active user's group(s)
-> complex conditionals. each visit to the code requires a considerable amount of 
time and attention to deduce what the condition's domain function is
"""


class AccountPaymentSummaryVendorBill(models.Model):
    _name = "account.payment.summary.vendor.bill"

    def write(self, values):
        is_group_originator = self.env.user.has_group(
            "account_payment_process.group_payment_originator"
        )
        is_group_reviewer = self.env.user.has_group(
            "account_payment_process.group_payment_reviewer"
        )
        if (not any([is_group_reviewer, is_group_originator])) and all(
                [
                    values,
                    any(
                        [
                            "amount" in values,
                            "invoice_id" in values,
                            "acc_amount" in values,
                            "due_date" in values,
                        ]
                    ),
                ]
        ):
            raise UserError(_("Sorry, You are not allowed to modify this record."))

        return super(AccountPaymentSummaryVendorBill, self).write(values)