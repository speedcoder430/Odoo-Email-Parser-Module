from odoo import http
from odoo.http import request

class SaleOrderController(http.Controller):

    @http.route('email_parser/sales_orders', type='http', auth='user', website=True)
    def list_sales_orders(self, **kwargs ):
        sales_orders = request.env['sale.order'].sudo().search([])
        return request.render('email_parser.sale_order', {'sales_orders': sales_orders})
