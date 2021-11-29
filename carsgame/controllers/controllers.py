# -*- coding: utf-8 -*-
# from odoo import http


# class Carsgame(http.Controller):
#     @http.route('/carsgame/carsgame/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/carsgame/carsgame/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('carsgame.listing', {
#             'root': '/carsgame/carsgame',
#             'objects': http.request.env['carsgame.carsgame'].search([]),
#         })

#     @http.route('/carsgame/carsgame/objects/<model("carsgame.carsgame"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('carsgame.object', {
#             'object': obj
#         })
