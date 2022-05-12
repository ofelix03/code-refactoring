from datetime import datetime
from odoo import fields, models, api
from odoo.exceptions import ValidationError

class Order(models.Model):
    _name = 'oms.order'
    _description = 'OMS Order'

    # Good compute: method renamed to reflect the true actions carried out in the
    # method block
    @api.depends("currency_id")
    def _compute_foreign_currency(self):
        self.foreign_currency = self.currency_id != \
                                self.env.user.company_id.currency_id

    #  Good onchange: method name is descriptive and conveys intent without reading
    #  the code block
    @api.onchange('product_id')
    def onchange_set_product_uom(self):
        self.product_uom_id = self.product_id and self.product_id.product_uom_id.id

    # Good onchange: mehtod is descriptive and convey intent without reading
    # the code block
    @api.onchange("partner_id")
    def onchange_filter_source(self):
        partner_category_ids = self.env['res.partner.category'] \
            .search([('name', 'in',
                      ['BDC', 'OMC', 'Product Customer', 'Product Supplier'])
                     ]).ids

        return {
            "domain": {
                "source_id": [('category_id', 'in', partner_category_ids)]
            }
        }


    # Better constraint
    @api.constraints('submitted_on')
    def _check_submitted_date_is_present(self):
        if self.submitted_on < datetime.today():
            raise ValidationError("Submitted date can not be a past date")

    @api.constraints('start_date', 'end_date')
    def _check_period_validity(self):
        if self.start_date and self.start_date < fields.Date.today():
            raise ValidationError("Start date can not be a past date")

        if all([self.end_date, self.start_date]) and self.end_date < self.start_date:
            raise ValidationError("End date can not be before start date")


