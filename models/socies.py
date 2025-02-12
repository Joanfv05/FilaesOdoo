from odoo import models, fields

class Socies(models.Model):
    _inherit = 'res.partner'

    # Campo relacionado con el nombre de la fila
    fila_nom = fields.Char(
        string="Nombre de la Fila",
        related="fila_ids.nom",
        store=True,
    )

    # Campo para la fecha de nacimiento
    data_naixement = fields.Date(string='Data de Naixement')
    
    # Campo Many2many para las filas, bloqueamos la edición manual
    fila_ids = fields.Many2many('filaes.filaes', string='Filaes')
