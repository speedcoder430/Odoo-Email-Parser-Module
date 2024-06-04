from odoo import http
from odoo.http import request

class FetchEmailController(http.Controller):

    def get_model(self, name):
        return request.env[name]

    def get_mail_message_model(self):
        return self.get_model('mail.message')

    @http.route('/email_parser/fetch', type='http', auth='public', website=True)
    def index(self, *args, **kwargs):
        model = self.get_mail_message_model()
        messages_data = model.search_read(
            [], ['id', 'body'])
        return request.render('email_parser.index', {'messages': messages_data})
