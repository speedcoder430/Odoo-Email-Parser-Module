from odoo import models, fields

class Inventory(models.Model):
    _name = 'email_parser.inventory'
    _description = 'Inventory'

    product_id = fields.Many2one('product.product', string='Product')
    quantity = fields.Float(string='Quantity On Hand')
