from odoo import models, fields

class Socies(models.Model):
    _inherit = 'res.partner'

    fila_nom = fields.Char(
        string="Nombre de la Fila",
        related="fila_ids.nom",
        store=True,
    )

    data_naixement = fields.Date(string='Data de Naixement')
    fila_ids = fields.Many2many('filaes.filaes', string='Filaes')  # Bloqueamos la edición manual
