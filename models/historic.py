from odoo import models, fields, api
from datetime import date

class Historic(models.Model):
    _name = 'filaes.historic'
    _description = 'Històric de Socis'

    soci_id = fields.Many2one('res.partner', string='DNI Soci', required=True)
    fila_id = fields.Many2one('filaes.filaes', string='Filà', required=True)
    fila_nom = fields.Char(string="Nom Filà", related='fila_id.nom', store=True)

    accio = fields.Selection([('alta', 'Alta'), ('baixa', 'Baixa')], string='Acció', required=True)
    data_accio = fields.Date(string='Data Acció Alta/Baixa', required=True)
    certificat_minusvalidesa = fields.Image(string='Certificat Minusvalidesa')
    condicio = fields.Selection([
        ('jovenil', 'Jovenil'),
        ('actiu', 'Actiu'),
        ('baixa', 'Baixa'),
        ('honorari', 'Honorari'),
        ('social', 'Social')
    ], string='Condició', compute='_compute_condicio', store=True)
    antiguitat = fields.Integer(string='Antiguitat', compute='_compute_antiguitat', store=True)

    @api.depends('accio', 'data_accio', 'antiguitat')
    def _compute_condicio(self):
        for record in self:
            if record.accio == 'baixa':
                record.condicio = 'baixa'
            elif record.accio == 'alta':
                if record.antiguitat < 18:
                    record.condicio = 'jovenil'
                elif record.antiguitat >= 30:
                    record.condicio = 'honorari'
                else:
                    record.condicio = 'actiu'
            
            if record.certificat_minusvalidesa:
                record.condicio = 'social'

    @api.depends('data_accio')
    def _compute_antiguitat(self):
        for record in self:
            if record.data_accio:
                record.antiguitat = (date.today() - record.data_accio).days // 365
            else:
                record.antiguitat = 0

    @api.model
    def create(self, vals):
        """Gestiona la relación Many2many con la filà al dar de alta o baja un soci."""
        historic = super(Historic, self).create(vals)

        fila = historic.fila_id
        soci = historic.soci_id

        if vals.get('accio') == 'alta':
            # Asegurar que el socio no esté duplicado
            if soci in fila.socios_ids:
                raise models.ValidationError("Aquest soci ja està donat d'alta en aquesta filà.")

            # Agregar el socio a la filà
            soci.fila_ids = [(4, fila.id)]  # 4: Añadir a Many2many

        elif vals.get('accio') == 'baixa':
            # Si se da de baja, eliminar la relación
            soci.fila_ids = [(3, fila.id)]  # 3: Eliminar de Many2many

        return historic

    def write(self, vals):
        """Asegurar que al modificar un registro de histórico también se actualiza la relación Many2many."""
        for record in self:
            if 'accio' in vals:
                nueva_accio = vals.get('accio')
                fila = record.fila_id
                soci = record.soci_id

                if nueva_accio == 'alta' and fila not in soci.fila_ids:
                    soci.fila_ids = [(4, fila.id)]

                elif nueva_accio == 'baixa' and fila in soci.fila_ids:
                    soci.fila_ids = [(3, fila.id)]

        return super(Historic, self).write(vals)
