from odoo import http
from odoo.http import request
import json

class FilaesController(http.Controller):

    @http.route('/filaes/socis', type='json', auth='user')
    def filter_socis(self, **kw):
        fila_id = kw.get('fila_id')
        condicio = kw.get('condicio')
        
        domain = []
        if fila_id:
            domain.append(('fila_id', '=', int(fila_id)))
        if condicio:
            domain.append(('condicio', '=', condicio))
        
        socis = request.env['filaes.historic'].search(domain)
        return json.dumps([{'id': s.soci_id.id, 'name': s.soci_id.name} for s in socis])

    @http.route('/filaes/montepios', type='json', auth='user')
    def get_montepios(self, **kw):
        dni = kw.get('dni')
        fila_id = kw.get('fila_id')
        any = kw.get('any')
        
        domain = [
            ('soci_id.vat', '=', dni),
            ('fila_id', '=', int(fila_id)),
            ('data_aportacio', '>=', f'{any}-01-01'),
            ('data_aportacio', '<=', f'{any}-12-31')
        ]
        
        montepios = request.env['filaes.montepios'].search(domain)
        return json.dumps([{
            'id': m.id,
            'aportacio': m.aportacio,
            'data_aportacio': m.data_aportacio.strftime('%Y-%m-%d')
        } for m in montepios])
