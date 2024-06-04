from odoo import models, fields, api
import email
from email.policy import default


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    parsed_email_subject = fields.Char(string="Parsed Email Subject")
    parsed_email_body = fields.Text(string="Parsed Email Body")

    @api.model
    def create_sale_order_from_email(self, email_message):
        parsed_data = self.env['email_parser.parsed_email'].parse_email(
            email_message)

        customer_name = self._extract_customer_name(parsed_data['email_body'])
        order_lines = self._extract_order_lines(parsed_data)

        partner = self.env['res.partner'].search(
            [('name', '=', customer_name)], limit=1)
        if not partner:
            partner = self.env['res.partner'].create({'name': customer_name})

        order_vals = {
            'partner_id': partner.id,
            'order_line': [(0, 0, line) for line in order_lines],
            'parsed_email_subject': parsed_data['subject'],
            'parsed_email_body': parsed_data['body'],
        }
        self.create(order_vals)

    def _extract_customer_name(self, email_body):
        # Implement your logic to extract the customer name from the email body
        return "Extracted Customer Name"

    def _extract_order_lines(self, parsed_data):
        # Implement your logic to extract order lines from the parsed data
        return [
            {'product_id': 1, 'product_uom_qty': 10},
            {'product_id': 2, 'product_uom_qty': 5},
        ]
