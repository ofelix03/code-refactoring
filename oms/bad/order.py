from datetime import datetime
from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Order(models.Model):
    _name = 'oms.order'
    _description = 'OMS Order'

    # Bad compute: method name is misleading about the outcome of the method
    # Method sets the value of the foreign_currency field and not the currency_id field
    @api.depends("currency_id")
    def _compute_currency_change(self):
        self.foreign_currency_id = self.currency_id != \
                                     self.env.user.company_id.currency_id

    # Bad onchange: method name unclear and fails to convey intent
    @api.onchange("product_id")
    def onchange_product_id(self):
        if self.product_id:
            self.product_uom_id = self.product_id.uom_id.id

    # Bad constraint:
    # Issues:
    # Lumps up different business constraint checks into one generic constraint method
    @api.constrains("submitted_on", "start_date", "end_date")
    def _check_date(self):
        if self.submitted_on and self.submitted_on < datetime.today():
            raise ValidationError("Submitted date can not be a past date")
        if self.start_date and self.start_date < fields.Date.today():
            raise ValidationError("Start date can not be a past date")
        if all([self.end_date, self.start_date]) and self.end_date < self.start_date:
            raise ValidationError("End date can not be before start date")

