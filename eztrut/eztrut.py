#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Modulo Eztrut. Resolve elasticidade desenha vigas simples 2d
"""

import numpy as np
import matplotlib.pyplot as plt
import itertools

# Definir class Viga


class Viga:
    """Cria um objeto da classe Viga
    Args:
        L (float): tamanho da viga em metros
        E (float): Módulo de E em MPa
        I (float): Momento de inércia em metros à quarta
        A (float): Área em m2
    """

    def __init__(self, L=1, E=20000, I=1, A=1):
        self.E = E
        self.I = I
        self.L = L
        self.A = A

        # Matriz de rigidez
        self.k = E * I / L**3 * np.array([
            [12., 6 * L, -12, 6 * L],
            [6 * L, 4 * L**2, -6 * L, 2 * L**2],
            [-12, -6 * L, 12, -6 * L],
            [6 * L, 2 * L**2, -6 * L, 4 * L**2]
        ])

    def __str__(self):
        return ('L = ' + str(self.L) + " m, \n"
                + 'Inercia = ' + str(self.I) + ' m^4, \n'
                + 'Elasticidade = ' + str(self.E) + ' MPa \n')

# Definicao da classe Nó
# Tipo 1 = fixo em x (apoiado)
# Tipo 2 = fixo em x elasticidade y (fixo)
# Tipo 3 = fixo em x, y elasticidade z (engastado)


class Elemento:
    """Cria um objeto da classe Elemento
    Args:
        L (float): tamanho da viga em metros
        E (float): Módulo de elasticidade em MPa
        I (float): Momento de inércia em metros à quarta
        A (float): Área em m2
    """

    def __init__(self, L=1, E=20000, I=1, A=1, apoios=[]):
        self.E = E
        self.I = I
        self.L = L
        self.A = A
        self.f = [0, 0, 0, 0, 0, 0]
        self.apoioA = apoios[0]
        self.apoioB = apoios[1]

            # Matriz de rigidez
        self.k = np.array([
            [E*A/L, 0, 0, -E*A/L, 0, 0],
            [0, 12*E*I/L**3, 6*E*I/L**2, 0, -12*E*I/L**3, 6*E*I/L**2],
            [0, 6*E*I/L**2, 4*E*I/L, 0, -6*E*I/L**2, 2*E*I/L],
            [-E*A/L, 0, 0, E*A/L, 0, 0],
            [0, -12*E*I/L**3, -6*E*I/L**2, 0, 12*E*I/L**3, -6*E*I/L**2],
            [0, 6*E*I/L**2, 2*E*I/L, 0, -6*E*I/L**2, 4*E*I/L]
        ])


    def solicitacao(self, carga):
        if isinstance(carga, ForcaC):

            return "forcaC"
        elif isinstance(carga,ForcaD):
            return "forcaD"
        else:
            return "forca invalida"


    def __str__(self):
        return ('Comprimento = ' + str(self.L) + " m, \n"
                + 'Inercia = ' + str(self.I) + ' m^4, \n'
                + 'Area = ' + str(self.A) + ' m^4, \n'
                + 'Elasticidade = ' + str(self.E) + ' MPa \n')

class Apoio:
    """Cria um objeto da classe Apoio
    Args:
        x (float): localizacao do apoio em relacao area ponta esquerda da viga
        # tipo (int): tipo do apoio
        #     1 = fixo em x (apoiado)
        #     2 = fixo em x elasticidade y (fixo)
        #     3 = fixo em x, y elasticidade z (engastado)
        eixos_restritos (int) = [x, y, z]
            1 = restrito, 0 = livre
            ex. Engastado = [1, 1, 1]

    """

    def __init__(self, x, eixos_restritos=[0,1,0]):
        self.x = x
        # self.tipo = tipo
        self.eixos_restritos = eixos_restritos
        self.reacao = 0
        self.nome = ''
        self.rotula = [0, 0] # caso haja rotula no comeco ou fim, trocar por 1

    def __cmp__(self, other):
        if hasattr(other, 'getKey'):
            return self.getKey().__cmp__(other.getKey())

    def getKey(self):
        return self.x

    def __repr__(self):
        return '{} {}: x = {}, eixo_restritos = {}, reacao = {}'.format(
            self.__class__.__name__,
            self.nome,
            self.x,
            self.eixos_restritos,
            self.reacao
        )

class No:
    """Cria um objeto da classe No
    Args:
        x (float): coordenada x do no
        y (float): coordenada y do no
        deslocamento [eixo x, eixo y, eixo z], onde:
            0 = livre
            1 = fixo
            2 = mola
            3 = recalque
    """

    def __init__(self, x, y, deslocamento):
        self.id = 0
        self.x = x
        self.y = y
        self.deslocalemento = deslocamento

class Barra:
    """Cria um objeto da classe Barra
    Args:
        no inicial (int): id do no inicial
        no final (int): id do no final
        rotula inicial (int): 1 = sim, 0 = nao
        rotula final (int): 1 = sim, 0 = nao
        E (float): Módulo de elasticidade em MPa
        I (float): Momento de inércia em metros à quarta
        A (float): Área em m2
    """

    def __init__(self, no_i, no_f, ro_i, ro_f, E, A, I):
        self.nome = ""
        self.x = x
        self.y = y
        self.deslocalemento = deslocamento




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

    def __init__(self, f, x, tipo, eixo):
        self.f = f
        self.x = x
        self.eixo = eixo
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
        self.trechos = self.definir_trechos()
        self.dist = 0
        self.soma_forcas_x = 0
        self.soma_forcas_y = 0
        self.soma_forcas_z = 0
        self.elementos = []
        self.matriz_rigidez_global = np.array([])

        if self.estaticidade() > 3:
            print("! ------ERRO ------ ! \n" +
                  "! ------ ESTRUTURA HIPERESTATICA ----- ! \n")

        for forca in self.cargas:
            if isinstance(forca, ForcaC):
                if forca.tipo == 1:
                    self.soma_forcas_x += forca.f
                elif forca.tipo == 2:
                    self.soma_forcas_y += forca.f
                elif forca.tipo == 3:
                    self.soma_forcas_z += forca.f


    def __str__(self):
        return 'Viga = ' + str(self.viga) + " m, \n"

    def estaticidade(self):
        """Retorna grau de estaticidade"""
        estaticidade = 0
        for apoio in self.apoios:
            for eixo in apoio.eixos_restritos:
                estaticidade = estaticidade + eixo
        return "Grau de estaticidade = ", estaticidade

    def plotagem_apoios(self):
        """Plota apoios"""
        for apoio in self.apoios:
            plt.plot([apoio.x], [0], marker=6, markersize=15, fillstyle='full')

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
        plt.plot([0, self.viga.L], [0, 0], linewidth=4, alpha=0.3)
        plt.xlabel('x [m]')
        # plt.ylabel('Momento fletor [kNm]')
        plt.yticks([])

    def plotagem_reacao_apoio(self):
        """Plota as flechas de reacao de apoio """
        for apoio in self.apoios:
            if apoio.reacao != 0:

                if apoio.reacao > 0:
                    posicao_texto = 40
                else:
                    posicao_texto = -40

                plt.annotate(
                    "{} kN".format(abs(apoio.reacao/1000)),
                    xy=(apoio.x, 0),
                    xytext=(0, posicao_texto),
                    textcoords='offset pixels',
                    arrowprops=dict(
                        arrowstyle='simple',
                        facecolor='red'
                    ),
                    horizontalalignment='center'
                )


    def mostrar_figura(self):
        """Plota viga, forcas e apoios"""
        self.fig.add_subplot(211)
        self.plotagem_viga()
        self.plotagem_apoios()
        self.plotagem_forcasC()
        plt.margins(0.2, 0)
        plt.show()

    def ordenar_nos(self, nos_array):
        """Retorna uma lista ordenada em funcao de X (posicao) e da nome aos apoios"""

        def getKey(elemento):
            return elemento.x

        array_ordenado = sorted(nos_array, key=getKey)
        indice = 1

        for no in array_ordenado:
            no.id = indice
            indice += 1

        return array_ordenado

    def ordenar_apoios(self, apoios_array):
        """Retorna uma lista ordenada em funcao de X (posicao) e da nome aos apoios"""

        def getKey(elemento):
            return elemento.x

        array_ordenado = sorted(apoios_array, key=getKey)
        letra = 'A'

        for apoio in array_ordenado:
            apoio.nome = letra
            letra = chr(ord(letra) + 1)

        return array_ordenado

    def definir_elementos(self):
        """ Retorna array separando a viga em varios elemntos conforme
        levando em consideracao apenas os APOIOS"""
        nos = [0]
        # criar no para o fim da viga
        nos.append(self.viga.L)
        # criar no para cada apoio
        for apoio in self.apoios:
            nos.append(apoio.x)

        nos_unicos = list(set(nos))
        elementos = [(nos_unicos[i], nos_unicos[i+1]) for i in range(len(nos_unicos)-1)]

        return elementos

    def definir_trecho_entre_apoio(self):
        """ Retorna array separando a viga em varios elemntos conforme
        levando em consideracao apenas os APOIOS"""
        # nos = []
        # criar no para o fim da viga
        # nos.append(self.viga.comprimento)
        # criar no para cada apoio
        # for apoio in self.apoios:
            # nos.append(apoio.x)

        # nos_unicos = list(set(nos))
        trechos_entre_apoio = [(self.apoios[i], self.apoios[i+1]) for i in range(len(self.apoios)-1)]
        return trechos_entre_apoio

    def solicitaoes(self, elemento):
        """ Verifica a existencia de forcas externas no elemento.
        este metodo coloca as forcas equiivalentes nos apoios"""

        ## TODO: NO MOMENTO SO FUNCIONA PARA CARGAS PONTUAIS
        atuantes = []
        for carga in self.cargas:
            if elemento.apoioA.x <= carga.x <= elemento.apoioB.x:
                atuantes.append(carga)
                return "forca encontra-se dentro do intervalo do elemento", carga.f, carga.x

        for carga in atuantes:
            p = carga.f
            l = elemento.apoioB.x - elemento.apoioA.x
            a = carga.x - elemento.apoioA.x
            b = l - a

            # para ambos lados engastados
            if (elemento.apoioaA.eixos_restritos[3] == 1) and (elemento.apoioB.eixos_restritos[3] == 1):
                
                # para forca vertical
                if carga.tipo == 2:
                    ma = p*a*(b**2)/(l**2)
                    mb = -p*(a**2)*b/(l**2)
                    va = p*(b**2)*(3*a+b)/(l**3)
                    vb = p*(a**2)*(a+3*b)/(l**3)
                
                # para forca tipo momento
                if carga.tipo == 3:
                    ma = p*b*(2*a-b)/(l**2)
                    mb = p*a*(2*b-a)/(l**2)
                    va = 6*p*a*b/(l**3)
                    vb = 6*p*a*b/(l**3)

            elemento.f[0] += 0
            elemento.f[1] += va
            elemento.f[2] += ma
            elemento.f[3] += 0
            elemento.f[4] += vb
            elemento.f[5] += mb


    def criar_elementos(self):
        trechos = self.definir_trecho_entre_apoio()
        for trecho in trechos:
            self.elementos.append(Elemento(
                A = self.viga.A,
                E = self.viga.E,
                I = self.viga.I,
                L = (trecho[1].x - trecho[0].x),
                apoios = (trecho[0], trecho[1])
            ))
        return trechos

    def gerar_matriz_rotacao(self, graus):
        radianos = np.deg2rad(graus)
        matriz_rotacao = np.array([
            [np.cos(radianos), np.sin(radianos), 0, 0, 0, 0],
            [-np.sin(radianos), np.cos(radianos), 0, 0, 0, 0],
            [0,0, 1, 0, 0, 0],
            [0, 0, 0, np.cos(radianos), np.sin(radianos), 0],
            [0, 0, 0, -np.sin(radianos), np.cos(radianos),  0],
            [0, 0, 0, 0, 0, 1],
        ])

        return matriz_rotacao

    def coordenadas2comprimento(self, xi, yi, xf, yf):
        l = np.sqrt((xf-xi)**2+(yf-yi)**2)
        return l
    
    def determinar_angulo_barra(self, xi, yi, xf, yf):
        delta_x = xf - xi
        delta_y = yf - yi
        tangente = delta_y / delta_x
        radianos = np.arctan(tangente)
        graus = np.rad2deg(radianos)

        return graus
        

    def definir_trechos(self):
        nos = [0]
        # criar no para o fim da viga
        nos.append(self.viga.L)
        # criar no para cada apoio
        for apoio in self.apoios:
            nos.append(apoio.x)
        # criar no para cada forca concentrada ou distribuida
        for forca_c in self.cargas:
            if isinstance(forca_c, ForcaC):
                nos.append(forca_c.x)
            else:
                for forca_d in self.cargas:
                    nos.append(forca_d.x_i)
                    nos.append(forca_d.x_f)

        nos_unicos = list(set(nos))
        trechos = [(nos_unicos[i], nos_unicos[i+1]) for i in range(len(nos_unicos)-1)]

        return trechos

    def cortante(self):
        pass


    def reacao_apoio_biapoiada_isoestatica(self):
        # determinar cortante em viga bi apoiada isoestatica

        # momento causado pela forca no apoio A
        m = 0

        # ordenar em ordem crescente da esquuerda para a direita os apoios
        self.apoios = self.ordenar_apoios(self.apoios)

        # posicao do apoio A
        x = self.apoios[0].x

        for carga in self.cargas:
            if carga.tipo == 2: # se a carga for do tipo vertical apenas
                # self.soma_forcas_y += carga.f
                if carga.x < x: # se a forca estiver aa esquerda do apoio A
                    m += carga.f * (x - carga.x)
                else:
                    m -= carga.f * (carga.x - x)

        # A reacao do apoio B tem que ser m dividido pela distancia dos apoios
        # (M = Rb * dist) -> (Rb = M / dist)
        # Eh importante que os apoios estejam em ordem da esquerda para direita
        self.dist = self.apoios[1].x - self.apoios[0].x
        self.apoios[1].reacao = m / self.dist
        self.apoios[0].reacao = - self.soma_forcas_y - self.apoios[1].reacao

        return print(" Soma de forcas em y: {} kN \n Apoio A: {} kN \n Apoio B: {} kN \n".format(
            self.soma_forcas_y/1000, self.apoios[0].reacao/1000, self.apoios[1].reacao/1000))


    def memorial_reacao(self):
        from IPython.display import display, Math, Latex, Markdown

        def forca_x():
            completo = False
            for forca in self.cargas:
                if forca.tipo == 1:
                    completo  = True

            if completo == True:
                frase = (r'\sum F_x = 0 \rightarrow R_a + R_b = ' +
                    str(self.soma_forcas_x) + r'\\')
            else:
                frase = r'\sum F_x = 0 \\'

            return frase

        def forca_y():
            completo = False
            for forca in self.cargas:
                if forca.tipo == 2:
                    completo  = True

            if completo == True:
                frase = (r'\sum F_y = 0 \rightarrow R_a + R_b = ' +
                    str(self.soma_forcas_y) + r'\\')
            else:
                frase = r'\sum F_y = 0 \\'

            return frase

        def forca_z():
            completo = False
            dist_forcas = []
            for forca in self.cargas:
                if forca.tipo == 2:
                    completo = True
                    dist_forcas.append(forca)
                    def gen():
                        for forca in self.cargas:
                            if forca.tipo == 2:
                                yield forca

            if completo == True:
                dist_forca_apoio = []
                for dist in dist_forcas:
                    dist_forca_apoio.append(dist.x - self.apoios[0].x)
                # print("dist forca apoio", dist_forca_apoio)
                frase = (r'\sum M_a = 0 \rightarrow ' )
                for forca in gen():
                    frase += (str(forca.x - self.apoios[0].x))
                    frase += r' \cdot '
                    frase += r'(' + str(forca.f) + r')'

                frase += r' = R_b \cdot '
                frase += r'(' + str(-self.apoios[1].reacao)+ r')'
            else:
                frase = r'\sum M = 0 \\'

            return frase


        sums = Math(
            forca_x() +
            forca_y() +
            forca_z()
        )
        return sums
