#!/usr/bin/python
# -*- coding: utf-8 -*-

# Importar bibliotecas
import eztrut as ez
import numpy as np
import matplotlib.pyplot as plt

# Criar uma viga de tamanho 4. Momento, inercia e area serao padrao.
viga1 = ez.Viga(4)

# Criar dois apoios. Um apoio fixo na ponta esquerda (x = 0) e outro livre no fim (x = 4)
apoioA = ez.Apoio(x=1, tipo=2)
apoioB = ez.Apoio(x=3, tipo=1)

# Criar uma forca CONCENTRADA vertical (de cima para baixo) de 10kN no meio da viga (x = 2)
forca1 = ez.ForcaC(f=-10000, x=2, tipo=2)

# Criar a estrutura para resolver os diagramas
apoios = [apoioA, apoioB]
forcas = [forca1]

estrut1 = ez.Eztrut(viga1, apoios, forcas)

# Mostrar uma figura  da viga com os apoios e forcas
print(estrut1.plotagem_cortante())