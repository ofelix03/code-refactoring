"""
Code Quality Issues:

-> complex control flow (nested if statements)
-> unnecessary nested conditionals
-> write(...) method is cluttered because it's doing more than it's responsibly for.
-> poor variable names ex. payment_lines_vendor_ids_todo,
payment_lines_vendor_ids_already_existing
"""

from odoo import models


class AccountPaymentProcess(models.Model):
    _name = "account.payment.process"

    def write(self, values):
        if "vendor_ids" in values:
            vendor_ids = set(values.get("vendor_ids")[0][2])
            payment_lines_vendor_ids_todo = set()

            if "payment_line_ids" in values:
                payment_lines_vendor_ids_todo = {
                    each[2].get("vendor_id")
                    for each in values.get("payment_line_ids")
                    if each[2]
                }

            for record in self:
                payment_lines_vendor_ids_already_existing = set(
                    record.payment_line_ids.mapped("vendor_id.id")
                )
                payment_lines_vendor_ids = payment_lines_vendor_ids_todo.union(
                    payment_lines_vendor_ids_already_existing
                )
                new_vendor_ids = list(vendor_ids.intersection(payment_lines_vendor_ids))
                values["vendor_ids"] = [(6, 0, new_vendor_ids)]

        return super(AccountPaymentProcess, self).write(values)