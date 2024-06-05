from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class ParsedEmail(models.Model):
    _name = 'email_parser.parsed_email'
    _description = 'Parsed Email Model'

    creation_date = fields.Char(string='Creation Date', required=True)
    customer_name = fields.Char(string='Customer Name', required=True)
    part_number = fields.Char(string='Part Number', required=True)
    product_name = fields.Char(string='Product Name', required=True)
    uid = fields.Char(string='UID', required=True)
    order_id = fields.Char(string='Order ID', required=True)
    quantity = fields.Float(string='Quantity', required=True)
    price = fields.Char(string='Price', required=True)
    total_price = fields.Char(string='Total Price', required=True)
    record = fields.Boolean(string='Record', required=True)
    processed = fields.Boolean(string='Processed', default=False)

    @api.model
    def process_parsed_emails(self):
        unprocessed_emails = self.search([('processed', '=', False)])
        for email in unprocessed_emails:
            try:
                self.create_sales_order_from_email(email)
                email.processed = True
                _logger.info(
                    f"Processed and created sales order for email UID: {email.uid}")
            except Exception as e:
                _logger.error(
                    f"Failed to process email UID: {email.uid}. Error: {e}")

    @api.model
    def create_sales_order_from_email(self, email_data):
        try:
            partner = self.env['res.partner'].search(
                [('name', '=', email_data.customer_name)], limit=1)
            if not partner:
                _logger.error(
                    f"Partner not found for customer name: {email_data.customer_name}")
                raise ValueError(
                    f"Partner not found for customer name: {email_data.customer_name}")

            product = self.env['product.product'].search(
                [('name', '=', email_data.product_name)], limit=1)
            if not product:
                _logger.error(
                    f"Product not found for product name: {email_data.product_name}")
                raise ValueError(
                    f"Product not found for product name: {email_data.product_name}")

            order_data = {
                'partner_id': partner.id,
                'order_line': [(0, 0, {
                    'product_id': product.id,
                    'product_uom_qty': email_data.quantity,
                    'price_unit': float(email_data.price),
                })],
            }
            sale_order = self.env['sale.order'].create(order_data)
            sale_order.action_confirm()  # Confirm the sales order to send it to the customer
            _logger.info(
                f"Sales order {sale_order.id} created and confirmed for email UID: {email_data.uid}")
            return sale_order
        except Exception as e:
            _logger.error(
                f"Error creating sales order from email UID: {email_data.uid}. Error: {e}")
            raise
