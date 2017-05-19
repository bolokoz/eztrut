#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Modulo Eztrut. Resolve elasticidade desenha vigas simples 2d
"""

import numpy as np
import matplotlib.pyplot as plt

# Definir class Viga


class Viga:
    """Cria um objeto da classe Viga
    Args:
        comprimento (float): tamanho da viga em metros
        elasticidade (float): Módulo de elasticidade em MPa
        inercia (float): Momento de inércia em metros à quarta
        area (float): Área em m2
    """

    def __init__(self, comprimento=1, elasticidade=20000, inercia=1, area=1):
        self.elasticidade = elasticidade
        self.inercia = inercia
        self.comprimento = comprimento
        self.area = area

        # Matriz de rigidez
        self.k = elasticidade * inercia / comprimento**3 * np.array([
            [12., 6 * comprimento, -12, 6 * comprimento],
            [6 * comprimento, 4 * comprimento**2, -
                6 * comprimento, 2 * comprimento**2],
            [-12, -6 * comprimento, 12, -6 * comprimento],
            [6 * comprimento, 2 * comprimento**2, -
                6 * comprimento, 4 * comprimento**2]
        ])

    def __str__(self):
        return ('Comprimento = ' + str(self.comprimento) + " m, \n"
                + 'Inercia = ' + str(self.inercia) + ' m^4, \n'
                + 'Elasticidade = ' + str(self.elasticidade) + ' MPa \n')

# Definicao da classe Nó
# Tipo 1 = fixo em x (apoiado)
# Tipo 2 = fixo em x elasticidade y (fixo)
# Tipo 3 = fixo em x, y elasticidade z (engastado)


class Apoio:
    """Cria um objeto da classe Apoio
    Args:
        x (float): localizacao do apoio em relacao area ponta esquerda da viga
        tipo (int): tipo do apoio
            1 = fixo em x (apoiado)
            2 = fixo em x elasticidade y (fixo)
            3 = fixo em x, y elasticidade z (engastado)
    """

    def __init__(self, x, tipo=1):
        self.x = x
        self.tipo = tipo


class ForcaC:
    """Cria um objeto da classe Forca concentrada. Positivo = De baixo para cima.
    Args:
        f (float): magnitude da forca em N
        x (float): localizacao da forca em relacao area ponta esquerda da viga
        tipo (int): tipo da forca
            1 = forca em x (vertical)
            2 = forca em y (horizontal)
            3 = forca em z (momento)
    """

    def __init__(self, f, x, tipo):
        self.f = f
        self.x = x
        self.tipo = tipo


class ForcaD:
    """Cria um objeto da classe Forca distribuida. Positivo = De baixo para cima.
    Args:
        f_i (float): magnitude da forca mais area ESQUERDA em [N]
        f_f (float): magnitude da forca mais area DIREITA em [N]
        x_i (float): localizacao da forca mais area ESQUERDA em relacao area ponta esquerda da viga
        x_f (float): localizacao da forca mais area DIREITA em relacao area ponta esquerda da viga
        tipo (int): tipo da forca
            1 = forca em x (horizontal)
            2 = forca em y (vertical)
            3 = forca em z (momento)
    """

    def __init__(self, f_i, f_f, x_i, x_f, tipo):
        self.f_i = f_i
        self.f_f = f_f
        self.x_i = x_i
        self.x_f = x_f
        self.tipo = tipo


class Eztrut:
    """Cria um objeto da classe Eztrut distribuida.
    Args:
        viga (Viga): objeto da classe Viga
        apoios[] (Apoio): um vetor com objetos da classe Apoio
        cargas[] (Forca): um vetor com objetos da classe Forca
    """

    def __init__(self, viga, apoios, cargas):
        self.viga = viga
        self.apoios = apoios
        self.cargas = cargas
        self.fig = plt.figure()

        if self.estaticidade() > 3:
            print("! ------ERRO ------ ! \n" +
                  "! ------ ESTRUTURA HIPERESTATICA ----- ! \n")

    def __str__(self):
        return 'Viga = ' + str(self.viga) + " m, \n"

    def estaticidade(self):
        """Retorna grau de estaticidade"""
        estaticidade = 0
        for apoio in self.apoios:
            estaticidade = estaticidade + apoio.tipo
        return estaticidade

    def plotagem_apoios(self):
        """Plota apoios"""
        for apoio in self.apoios:
            plt.plot([apoio.x, 0], [0, 0], 'bo')

    def plotagem_forcasC(self):
        """Plota forcas concentradas"""
        ax = plt.gca()
        ymax = ax.get_ylim()[1]
        for forca in self.cargas:
            if forca is ForcaC:
                plt.annotate("F{}".format(abs(forca.f)), xy=(forca.x, 0), xytext=(
                    forca.x, ymax / 3), arrowprops=dict(facecolor='black', shrink=0.15),
                             horizontalalignment='center')

    def plotagem_viga(self):
        """Plota viga"""
        plt.plot([0, self.viga.comprimento], [0, 0], linewidth=10, alpha=0.5)
        plt.xlabel('x [m]')
        plt.ylabel('Momento fletor [kNm]')

    def mostrar_figura(self):
        """Plota viga, forcas e apoios"""
        self.fig.add_subplot(211)
        self.plotagem_viga()
        self.plotagem_apoios()
        self.plotagem_forcasC()
        plt.show()
