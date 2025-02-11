from odoo import http
from odoo.http import request, Response
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

    from odoo import http
from odoo.http import request, Response
import json
import logging

_logger = logging.getLogger(__name__)

class FilaesController(http.Controller):

    @http.route('/filaes/montepios', type='http', auth='user')
    def get_montepios(self, **kw):
        dni = kw.get('dni')
        fila_id = kw.get('fila_id')
        any = kw.get('any')
        
        _logger.info("Buscando montepios con los siguientes parámetros: DNI=%s, Fila ID=%s, Año=%s", dni, fila_id, any)
        
        domain = [
            ('soci_id.vat', '=', dni),
            ('fila_id', '=', int(fila_id)),
            ('data_aportacio', '>=', f'{any}-01-01'),
            ('data_aportacio', '<=', f'{any}-12-31')
        ]
        
        montepios = request.env['filaes.montepios'].search(domain)
        
        if not montepios:
            _logger.info("No se encontraron montepios para los parámetros dados.")
        
        data = [{'id': m.id, 'aportacio': m.aportacio, 'data_aportacio': m.data_aportacio.strftime('%Y-%m-%d')} for m in montepios]
        
        # Loguear la respuesta JSON antes de enviarla
        _logger.info("Datos de montepios: %s", data)
        
        # Retornar los datos en un script
        return Response(f"<script>window.montepios = {json.dumps(data)};</script>", content_type='text/html')
