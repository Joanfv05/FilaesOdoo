# -*- coding: utf-8 -*-
# from odoo import http


# class Filaes(http.Controller):
#     @http.route('/filaes/filaes', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/filaes/filaes/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('filaes.listing', {
#             'root': '/filaes/filaes',
#             'objects': http.request.env['filaes.filaes'].search([]),
#         })

#     @http.route('/filaes/filaes/objects/<model("filaes.filaes"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('filaes.object', {
#             'object': obj
#         })

