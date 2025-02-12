from odoo import models, fields, api

class Filaes(models.Model):
    _name = 'filaes.filaes'
    _description = 'Filaes'

    # Campos principales de la filà
    cif = fields.Char(string='CIF', required=True)
    nom = fields.Char(string='Nom', required=True)
    color = fields.Integer(string='Color Index')
    any_fundacio = fields.Date(string='Any Fundació')
    nombre_components = fields.Integer(string='Nombre de Components', compute='_compute_nombre_components', store=True)

    # Relaciones con otros modelos
    historic_ids = fields.One2many('filaes.historic', 'fila_id', string="Historial")
    montepios_ids = fields.One2many('filaes.montepios', 'fila_id', string="Aportaciones")
    socios_ids = fields.Many2many('res.partner', string="Miembros")

    @api.depends('historic_ids')
    def _compute_nombre_components(self):
        #Cuenta los socios activos en la filà considerando solo su último registro en el histórico
        for fila in self:
            # Obtener todos los registros históricos de esta filà
            socios_historico = self.env['filaes.historic'].search([
                ('fila_id', '=', fila.id)
            ])

            # Diccionario para almacenar el último estado de cada socio
            ultimo_estado_por_socio = {}

            for hist in socios_historico:
                soci_id = hist.soci_id.id
                if soci_id not in ultimo_estado_por_socio or hist.data_accio > ultimo_estado_por_socio[soci_id].data_accio:
                    ultimo_estado_por_socio[soci_id] = hist

            # Contar solo los socios cuyo último estado sea 'alta'
            fila.nombre_components = sum(1 for hist in ultimo_estado_por_socio.values() if hist.accio == 'alta')
