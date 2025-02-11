from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Montepios(models.Model):
    _name = 'filaes.montepios'

    soci_id = fields.Many2one(
        'res.partner',
        string='Soci',
        required=True,
        default= False
    )
   
    fila_id = fields.Many2one(
        'filaes.filaes',
        string='Filà',
        required=True,
        default= False
    )

    aportacio = fields.Float(string='Aportació', required=True)
    data_aportacio = fields.Date(string='Data Aportació', required=True)
   

    @api.model
    def create(self, vals):
        # Obtenemos soci_id y fila_id de los valores
        soci_id = vals.get('soci_id')
        fila_id = vals.get('fila_id')
       
        # Validar que soci_id y fila_id existan
        if not soci_id or not fila_id:
            raise ValidationError("El soci i la filà són obligatoris.")

        # Validar si el soci pertenece a la filà
        soci = self.env['res.partner'].browse(soci_id)
        if fila_id not in soci.fila_ids.ids:
            raise ValidationError("El soci no pertenece a la filà.")

        # Validar si el soci está de baja
        historic = self.env['filaes.historic'].search([
            ('soci_id', '=', soci_id),
            ('accio', '=', 'baixa')
        ], limit=1)
        if historic:
            raise ValidationError("El soci està de baixa i no pot fer una aportació.")    

        # Crear el registro si todas las validaciones pasaron
        return super(Montepios, self).create(vals)