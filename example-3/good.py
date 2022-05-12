"""
Code Quality Improvements:

-> simplify control flow (flatten nested if statements)
-> improve control flow by first checking for unmet prerequisite states and exiting
immediately
-> dict.get(...) is verbose, and adds to code cognitive dissonance. If you don't
intent to provide a default value stick to traditional index lookup.
-> poor variable names renamed.
--> payment_lines_vendor_ids_todo renamed to updated_payment_lines_vendor_ids
--> payment_lines_vendor_ids_already_existing renamed to existing_payment_lines_vendor_ids
"""
from odoo import models


class AccountPaymentProcess(models.Model):
    _name = "account.payment.process"

    def _find_new_vendor_ids(self, vals):
        updated_payment_lines_vendor_ids = [line[2]['vendor_id']
                                   for line in vals['payment_line_ids']]

        existing_payment_lines_vendor_ids = self.payment_line_ids.mapped('vendor_id.id')
        new_vendor_ids = updated_payment_lines_vendor_ids.union(existing_payment_lines_vendor_ids)

        return new_vendor_ids

    def write(self, vals):

        if 'vendor_ids' not in vals and 'payment_line_ids' not in vals:
            return super(AccountPaymentProcess, self).write(vals)

        new_vendor_ids = self._find_new_vendor_ids(vals)
        vals["vendor_ids"] = [(6, 0, new_vendor_ids)]

        return super(AccountPaymentProcess, self).write(vals)