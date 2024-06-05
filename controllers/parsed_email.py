from bs4 import BeautifulSoup
from odoo.http import request
from odoo import http


class ParsedEmailController(http.Controller):

    def get_model(self, name):
        return request.env[name]

    def get_mail_message_model(self):
        return self.get_model('mail.message')

    def get_parsed_email_model(self):
        return self.get_model('email_parser.parsed_email')

    def parse_email_body(self, body):
        try:
            soup = BeautifulSoup(body, 'html.parser')
            return {
                'customer_name': soup.find(id='customer-name').text if soup.find(id='customer-name') else '',
                'creation_date': soup.find(id='creation-date').text if soup.find(id='creation-date') else '',
                'part_number': soup.find(id='part-number').text if soup.find(id='part-number') else '',
                'product_name': soup.find(id='product-name').text if soup.find(id='product-name') else '',
                'uid': soup.find(id='uid').text if soup.find(id='uid') else '',
                'order_id': soup.find(id='order-id').text if soup.find(id='order-id') else '',
                'quantity': soup.find(id='quantity').text if soup.find(id='quantity') else '',
                'price': soup.find(id='price').text if soup.find(id='price') else '',
                'total_price': soup.find(id='total-price').text if soup.find(id='total-price') else '',
                'record': 0,
                'processed': 0
            }
        except Exception as e:
            # Log the exception or handle it more gracefully
            request.env['ir.logging'].sudo().create({
                'name': 'ParsedEmailController.parse_email_body',
                'type': 'server',
                'level': 'error',
                'message': str(e),
                'path': 'parsed_email_controller',
                'func': 'parse_email_body',
                'line': 'parse_email_body'
            })
            return None

    @http.route('/email_parser/parsed', type='http', auth='public', website=True)
    def parsed_email(self, **kwargs):
        parsed_messages = []
        new_parsed_messages = []

        try:
            messages = self.get_mail_message_model().search_read(
                [('parent_id', '=', False)], ['id', 'body'])
        except Exception as e:
            request.env['ir.logging'].sudo().create({
                'name': 'ParsedEmailController.parsed_email',
                'type': 'server',
                'level': 'error',
                'message': 'Failed to fetch mail messages: ' + str(e),
                'path': 'parsed_email_controller',
                'func': 'parsed_email',
                'line': 'fetch_mail_message'
            })
            messages = []

        parsed_emails = self.get_parsed_email_model().search([])
        seen_uids = set()

        for message in messages:
            parsed_data = self.parse_email_body(message['body'])
            if parsed_data is not None and parsed_data['customer_name'] != '':
                uid = parsed_data['uid']
                if uid not in seen_uids:
                    existing_email = next(
                        (email for email in parsed_emails if email.uid == uid), None)
                    if existing_email:
                        parsed_messages.append({
                            'id': message['id'],
                            'creation_date': parsed_data['creation_date'],
                            'customer_name': parsed_data['customer_name'],
                            'part_number': parsed_data['part_number'],
                            'product_name': parsed_data['product_name'],
                            'uid': uid,
                            'order_id': parsed_data['order_id'],
                            'quantity': parsed_data['quantity'],
                            'price': parsed_data['price'],
                            'total_price': parsed_data['total_price'],
                            'record': existing_email.record,
                            'processed': existing_email.processed,
                        })
                    else:
                        new_parsed_messages.append({
                            'id': message['id'],
                            'creation_date': parsed_data['creation_date'],
                            'customer_name': parsed_data['customer_name'],
                            'part_number': parsed_data['part_number'],
                            'product_name': parsed_data['product_name'],
                            'uid': uid,
                            'order_id': parsed_data['order_id'],
                            'quantity': parsed_data['quantity'],
                            'price': parsed_data['price'],
                            'total_price': parsed_data['total_price'],
                            'record': False,
                            'processed': False,
                        })
                    seen_uids.add(uid)

        if new_parsed_messages:
            try:
                self.get_parsed_email_model().create(new_parsed_messages)
            except Exception as e:
                request.env['ir.logging'].sudo().create({
                    'name': 'ParsedEmailController.parsed_email',
                    'type': 'server',
                    'level': 'error',
                    'message': 'Failed to create new parsed emails: ' + str(e),
                    'path': 'parsed_email_controller',
                    'func': 'parsed_email',
                    'line': 'create_parsed_email'
                })

        return request.render('email_parser.parsed_email', {'parsed_messages': parsed_messages})
