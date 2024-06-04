from odoo import models, fields, api
import email
from email.policy import default

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
    total_price = fields.Char(string='Total', required=True)
    record = fields.Boolean(string = 'Record', required=True)

    @api.model
    def parse_email(self, email_message):
        msg = email.message_from_string(email_message, policy=default)
        email_body = msg.get_body(preferencelist=('plain')).get_content()

        # Logic to extract part number, product name, UID, and order ID
        creation_date = self._extract_creation_date(email_body)
        customer_name = self._extract_customer_name(email_body)
        part_number = self._extract_part_number(email_body)
        product_name = self._extract_product_name(email_body)
        uid = self._extract_uid(email_body)
        order_id = self._extract_order_id(email_body)
        quantity = self._extract_quantity(email_body)
        price = self._extract_price(email_body)
        total_price = self._extract_total_price(email_body)
        # record = 

        return {
            'creation_date': creation_date,
            'customer_name': customer_name,
            'part_number': part_number,
            'product_name': product_name,
            'uid': uid,
            'order_id': order_id,
            'quantity': quantity,
            'price': price,
            'total_price': total_price,
            # 'record': record,
        }

    def _extract_creation_date(self, email_body):
        # Logic to extract customer name
        return "extracted_creation_date"
    
    def _extract_customer_name(self, email_body):
        # Logic to extract customer name
        return "extracted_customer_name"
    
    def _extract_part_number(self, email_body):
        # Logic to extract part number
        return "extracted_part_number"

    def _extract_product_name(self, email_body):
        # Logic to extract product name
        return "extracted_product_name"

    def _extract_uid(self, email_body):
        # Logic to extract UID
        return "extracted_uid"

    def _extract_order_id(self, email_body):
        # Logic to extract order ID
        return "extracted_order_id"
    
    def _extract_quantity(self, email_body):
        # Logic to extract quantity
        return "extracted_quantity"
    
    def _extract_price(self, email_body):
        # Logic to extract quantity
        return "extracted_price"
    
    def _extract_total_price(self, email_body):
        # Logic to extract total price
        return "extracted_total_price"
    
    # def _extract_record(self, email_body):
    #     # Logic to extract total price
    #     return "extracted_record"

    # @api.model
    # def update_inventory_from_emails(self):
    #     parsed_emails = self.search([])
    #     for email in parsed_emails:
    #         product = self.env['product.product'].search(
    #             [('default_code', '=', email.part_number)], limit=1)
    #         if product:
    #             quant = self.env['stock.quant'].search(
    #                 [('product_id', '=', product.id)], limit=1)
    #             if quant:
    #                 quant.quantity += 1
