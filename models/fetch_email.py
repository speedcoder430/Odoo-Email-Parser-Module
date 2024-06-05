from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class FetchEmail(models.Model):
    _name = 'email_parser.fetch'
    _description = 'Email Parser Fetch'

    subject = fields.Char(string='Subject')
    body = fields.Html(string='Body')

    @api.model
    def fetch_emails(self):
        email_messages = self.env['mail.message'].search([])
        for message in email_messages:
            subject = message.subject
            body = message.body
            self.process_message(subject, body)

    def process_message(self, subject, body):
        try:
            self.create({
                'subject': subject,
                'body': body,
            })
            _logger.info(f'Processed and saved email with subject: {subject}')
        except Exception as e:
            _logger.error(f"Failed to save email message: {e}")
