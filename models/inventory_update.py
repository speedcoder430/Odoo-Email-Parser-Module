from odoo import models, fields

class InventoryUpdate(models.Model):
    _name = 'email_parser.inventory_update'
    _description = 'Inventory Update'

    product_id = fields.Many2one('product.product', string='Product')
    quantity = fields.Float(string='Quantity On Hand')
