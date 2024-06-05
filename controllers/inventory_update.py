from odoo import http
from odoo.http import request


class InventoryDataUpdateController(http.Controller):

    @http.route('/email_parser/update_inventory', type='http', auth='public', website=True)
    def update_inventory(self, *args, **kwargs):
        email_model = request.env['email_parser.parsed_email']
        inventory_model = request.env['stock.quant']
        emails = email_model.search_read(
            [], ['part_number', 'product_name', 'quantity', 'record'])
        inventorys = inventory_model.search_read(
            [], ['product_id', 'quantity'])
        updated_inventory_records = []
        if emails and inventorys:
            for email in emails:
                for inventory in inventorys:
                    if ('[' + email['part_number'] + '] ' + email['product_name']) == inventory['product_id'][1] and inventory is not None and email['record'] == 0:
                        new_quantity = inventory['quantity'] - \
                            email['quantity']
                        inventory_record = inventory_model.browse(
                            inventory['id'])
                        inventory_record.write({'quantity': new_quantity})
                        email_record = email_model.browse(email['id'])
                        email_record.write({'record': 1})
                        updated_inventory_records.append({
                            "product_name": inventory['product_id'][1],
                            "quantity": new_quantity
                        })

        return request.render('email_parser.inventory_update', {
            "updated_inventory_records": updated_inventory_records
        })
