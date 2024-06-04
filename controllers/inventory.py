from odoo import http
from odoo.http import request


class InventoryDataController(http.Controller):

    def get_model(self, name):
        return request.env[name]

    def get_inventory_model(self):
        return self.get_model('stock.quant')

    def get_parsed_email_model(self):
        return self.get_model('email_parser.parsed_email')

    @http.route('/email_parser/inventory', type='http', auth='public', website=True)
    def inventorys(self, *args, **kwargs):
        inventory_model = self.get_inventory_model()
        inventory_records = inventory_model.search_read(
            [], ['product_id', 'quantity'])
        inventory = []
        for rec in inventory_records:
            if rec is not None:
                inventory.append({
                    'product_id': rec['product_id'][1],
                    'quantity': rec['quantity']
                })
        return request.render('email_parser.inventory', {'inventory': inventory})

    @http.route('/email_parser/inventory/<string:product_id>', type='http', auth='public', website=True)
    def inventory(self, product_id, *args, **kwargs):
        inventory_records = self.get_inventory_model()
        fetched_inventorys = inventory_records.search_read(
            [], ['product_id', 'quantity'])
        inventory = []
        for fetched_inventory in fetched_inventorys:
            if fetched_inventory is not None and fetched_inventory['product_id'][1] == product_id:
                inventory.append({
                    'product_id': fetched_inventory['product_id'][1],
                    'quantity': fetched_inventory['quantity']
                })

        return request.render('email_parser.inventory', {'inventory': inventory})
    