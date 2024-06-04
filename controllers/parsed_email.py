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
                'part_number': soup.find(id='part-number').text,
                'product_name': soup.find(id='product-name').text,
                'uid': soup.find(id='uid').text,
                'order_id': soup.find(id='order-id').text,
            }
        except Exception as e:
            # Log the exception or handle it more gracefully
            return None

    @http.route('/email_parser/parsed', type='http', auth='public', website=True)
    def parsed_email(self, *args, **kwargs):
        parsed_messages = []
        new_parsed_messages = []

        messages = self.get_mail_message_model().search_read(
            [('parent_id', '=', False)], ['id', 'body'])

        existing_uids = set(
            self.get_parsed_email_model().search([]).mapped('uid'))

        seen_uids = set()

        for message in messages:
            parsed_data = self.parse_email_body(message['body'])
            if parsed_data is not None:
                uid = parsed_data['uid']
                if uid not in existing_uids and uid not in seen_uids:
                    new_parsed_messages.append({
                        'id': message['id'],
                        'part_number': parsed_data['part_number'],
                        'product_name': parsed_data['product_name'],
                        'uid': uid,
                        'order_id': parsed_data['order_id'],
                    })
                    seen_uids.add(uid)
                elif uid not in seen_uids:
                    parsed_messages.append({
                        'id': message['id'],
                        'part_number': parsed_data['part_number'],
                        'product_name': parsed_data['product_name'],
                        'uid': uid,
                        'order_id': parsed_data['order_id'],
                    })
                    seen_uids.add(uid)

        if new_parsed_messages:
            self.get_parsed_email_model().create(new_parsed_messages)

        return request.render('email_parser.parsed_email', {'parsed_messages': parsed_messages})