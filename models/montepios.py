from odoo import models, fields, api

class Montepios(models.Model):
    _name = 'filaes.montepios'
    _description = 'Montepios'

    soci_id = fields.Many2one('filaes.socies', string='DNI Soci')
    fila_id = fields.Many2one('filaes.filaes', string='Nom Filà')
    aportacio = fields.Float(string='Aportació')
    data_aportacio = fields.Date(string='Data Aportació')

    @api.model
    def create(self, vals):
        # Implementar validació que el soci no està de baixa
        return super(Montepios, self).create(vals)
