from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    parsed_email_subject = fields.Char(string="Parsed Email Subject")
    parsed_email_body = fields.Text(string="Parsed Email Body")
