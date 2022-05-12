"""
Code Quality Imrpovements:
-> simplify control flow by
--> performing checks for prerequisite states and exiting immediately if not met
"""

from odoo import models


class EmployeeReimbursement(models.Model):
    _name = "hr.medical.employee.bill.reimbursement"

    @staticmethod
    def _write_amount_data(self, employee_id):
        bill_cap = self.env["hr.medical.employee.bill.cap"].search(
            [("employee_id", "=", employee_id)], order="id desc", limit=1
        )

        medical_debt = self.env["hr.medical.employee.debt"].search(
            [("employee_id", "=", employee_id)], limit=1
        )

        if not bill_cap and not medical_debt:
            return

        cap_amounts = self.update_bill_cap_amounts(bill_cap)
        medical_debt.write(
            {
                "total_debt_amount": cap_amounts["total_debt_amount"],
                "total_remaining_debt_amount": cap_amounts[
                    "total_remaining_debt_amount"
                ],
                "total_reimbursed_amount": cap_amounts[
                    "total_reimbursed_amount"
                ],
            }
        )