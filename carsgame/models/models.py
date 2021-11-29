# -*- coding: utf-8 -*-

from odoo import models, fields, api
import random
import logging
import re
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class piloto(models.Model):
    _name = 'carsgame.piloto'
    _description = 'carsgame.piloto'

    name = fields.Char(string="Nombre", readonly=False, required=True, help='Este es el nombre')
    numero_acreditacio = fields.Char(string="Numero Acreditacio Entrada Circuit")
    
    @api.constrains('numero_acreditacio')
    def _check_numero_acreditacio(self):
        regex = re.compile('[0-9]{3}[a-z]\Z', re.I)
        for s in self:
            if regex.match(s.numero_acreditacio):
                _logger.info('El numero acreditacio es valid')
            else:
                raise ValidationError('El numero de acreditacio no es valid. (3 numeros i una lletra)')

    _sql_constraints = [('numero_acreditacio_uniq','unique(numero_acreditacio)','El numero de acreditacio no es pot repetir')]

    car = fields.Text()

    @api.depends('name', 'car')
    def compute_display_name(self):
        # This will be called every time the field is viewed
        pass

    victories = fields.Integer(default='0')

    @api.onchange('victories')
    def _onchange_victories(self):
        if self.victories < 0:
            self.victories = 0
            return {
                'warning' :
                {
                'title':'Number of victories',
                'message':'Number of victories cant be less than 0',
                'type':'notification'
                }
            }

    country_of_birth = fields.Text()
    is_pilot = fields.Boolean(default="1")
    photo = fields.Image() 

    def _get_votos(self):
            print('\033[94m',piloto,'\033[0m')
            numeroRandom = random.randint(0,280000)
            votos_final_carrera = numeroRandom
            _logger.debug('\033[94m'+str(numeroRandom)+'\033[0m')
            return votos_final_carrera

    votos_final_carrera = fields.Integer(default=_get_votos, help='Este es el numero de vots recibits per el pilot de la gent')
    
    def regenerar_votos(self):        
        for s in self:
            numeroRandom = random.randint(0,280000)
            votos_final_carrera_reg = numeroRandom
            s.write({'votos_final_carrera':votos_final_carrera_reg})


    escuderia = fields.Many2one('carsgame.escuderia', ondelete='set null', help='La escuderia a la que pertany')
    favourite_circuit = fields.Many2one('carsgame.circuito', help='Molts pilots tenen un circuit favorit')
    state = fields.Selection([('1','Campionat en proces'),('2','Campionat acabat')], default='1')

class escuderia(models.Model):
    _name = 'carsgame.escuderia'
    _description = 'Las escuderias'

    name = fields.Char(string="Nombre escuderia")
    photo_escuderia = fields.Image() 
    pilotos = fields.One2many('carsgame.piloto','escuderia', help='Una escuderia te molts pilots')
    circuitos = fields.Many2many('carsgame.circuito', help='Una escuderia pot tindre molts circuits')
    piloto_lider_escuderia = fields.Many2one('carsgame.piloto', compute='_get_piloto_lider', string="Piloto lider del equip", help='El pilot que mes punts te dins de la escuderia')

    def _get_piloto_lider(self):
        for escuderia in self:
            escuderia.piloto_lider_escuderia = escuderia.pilotos[0].id


class circuito(models.Model):
    _name = 'carsgame.circuito'
    _description = 'Los circuitos'

    name = fields.Char(string="Nombre circuito")
    escuderia = fields.Many2many('carsgame.escuderia', string="Escuderias que tienen este circuito como favorito", help='Una circuit pot tindre moltes escuderies')

    def _get_votos(self):
            print('\033[94m',circuito,'\033[0m')
            numeroRandomAsistencia = random.randint(0,780000)
            numero_asistentes_carrera = numeroRandomAsistencia
            _logger.debug('\033[94m'+str(numeroRandomAsistencia)+'\033[0m')
            return numero_asistentes_carrera

    numero_asistentes_carrera = fields.Integer(default=_get_votos, help='Este es el numero de asistents de la carrera')
    
    dia_de_la_carrera = fields.Date(default=lambda self: fields.Date.today())
    dia_final_de_la_carrera = fields.Date(default=lambda self: fields.Date.today())

    def _random_name(self):
        noms = ["Baku", "Red Bull Ring", "Hungaroring", "Spa-Francorchamps", "Zandvoort", "Monza", "Sochi", "Losail", "Monaco", "Enzo e Dino Ferrari"]
        rand = random.randint(0,9)
        randNom = noms[rand]
        return randNom

    def crear_circuit(self):     
        self.write({'name': self._random_name()})   
        self.write({'dia_de_la_carrera': fields.Date.today()})   
        self.write({'dia_final_de_la_carrera': fields.Date.today()})   
        