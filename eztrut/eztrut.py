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
            plt.plot([apoio.x], [0], marker='^', markersize=12, fillstyle='none')

    def plotagem_forcasC(self):
        """Plota forcas concentradas"""
        ax = plt.gca()
        ymax = ax.get_ylim()[1]
        for forca in self.cargas:
            if isinstance(forca, ForcaC):
                plt.annotate("{} kN".format(abs(forca.f / 1000)), xy=(forca.x, 0), xytext=(
                   0, 40), textcoords='offset pixels', arrowprops=dict(arrowstyle="-|>"),
                             horizontalalignment='center')

    def plotagem_viga(self):
        """Plota viga"""
        plt.plot([0, self.viga.comprimento], [0, 0], linewidth=4, alpha=0.3)
        plt.xlabel('x [m]')
        plt.ylabel('Momento fletor [kNm]')

    def mostrar_figura(self):
        """Plota viga, forcas e apoios"""
        self.fig.add_subplot(211)
        self.plotagem_viga()
        self.plotagem_apoios()
        self.plotagem_forcasC()
        plt.margins(0.2, 0)
        plt.show()
    
    def cortante(self):
        fx=0
        fy=0
        fz=0

        # Soma das forcas
        for carga in self.cargas:
            if carga.tipo == 1:
                fx+=carga.f
            if carga.tipo == 2:
                fy+=carga.f
            if carga.tipo == 3:
                fz+=carga.f
        # vetor com a soma das forcas em todas direcoes
        f = [fx, fy, fz]
        

    def reacao_apoio_biapoiada_isoestatica(self):
        # determinar cortante em viga bi apoiada isoestatica

        # momento causado pela forca no apoio A
        m = 0

        # Soma de forcas em y
        fy = 0

        # posicao do apoio A
        x = self.apoios[0].x

        for carga in self.cargas:
            if carga.tipo == 2: # se a carga for do tipo vertical apenas
                fy += carga.f
                if carga.x < x: # se a forca estiver aa esquerda do apoio A
                    m += carga.f * (x - carga.x)
                else:
                    m -= carga.f * (carga.x - x)

        # A reacao do apoio B tem que ser m dividido pela distancia dos apoios
        # (M = Rb * dist) -> (Rb = M / dist)
        # Eh importante que os apoios estejam em ordem da esquerda para direita
        dist = self.apoios[1].x - self.apoios[0].x
        reacao_b = m / dist
        reacao_a = fy - reacao_b

        return "Soma de forcas em y: {} kN \n Apoio A: {} kN \n Apoio B: {} \n".format(
            fy/1000, reacao_a/1000, reacao_b/1000)



