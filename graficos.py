# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from sympy import *
import numpy as np
from math import *
from numpy import ones,vstack
from numpy.linalg import lstsq
import matplotlib.patches as mpatches

arr_x = []  # array para a posição em x da bola
arr_y = []  # array para a  posição em y da bola
arr_t = []  # array para a  tempo da trajetória da bola

def criaArrays():

    trajetoria = open("trajetoria.txt", "r")

    global arr_x, arr_y, arr_t

    #Armazenando as coordenadas nos arrays
    for coord in trajetoria.readlines():
        linha = coord.split("\t")
        # if float(linha[1].strip("\n").strip("ï»¿").replace(",", ".")) <= 6:
        arr_t.append(float(linha[0].strip("\n").strip("ï»¿").replace(",", ".")))
        arr_x.append(float(linha[1].strip("\n").strip("ï»¿").replace(",", ".")))
        arr_y.append(float(linha[2].strip("\n").strip("ï»¿").replace(",", ".")))

    trajetoria.close()



# PLOTA DOIS GRÁFICOS NUMA ÚNICA FIGURA
def doublePlot(arr, arr2, titulo, xlabel, ylabel, legenda,
               arr3, arr4, titulo2, xlabel2, ylabel2, legenda2):

    plt.subplot(2, 1, 1)
    blue_patch = mpatches.Patch(color='blue', label=legenda)
    plt.legend(handles= [blue_patch])
    plt.grid()
    plt.plot(arr, arr2)

    plt.title(titulo)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.subplot(2, 1, 2)
    orange_patch = mpatches.Patch(color='orange', label=legenda2)
    plt.legend(handles= [orange_patch])
    plt.grid()
    plt.plot(arr3, arr4, color='orange')
    plt.title(titulo2)
    plt.xlabel(xlabel2)
    plt.ylabel(ylabel2)


    plt.subplots_adjust(hspace=0.5)

    plt.show()



#Plota os gráficos de acordo com os parâmetros passados
def plotGrafico(arr, arr2, titulo, xlabel, ylabel):
    plt.plot(arr, arr2)
    plt.title(titulo)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid()

    plt.show()




# Plota as trajetórias do robô e da bola até o ponto de interceptação
def plotTrajetorias(arr, arr2,arr3, arr4, tempo, intercept):

    # Gráfico das trajetórias caso o robô tenha interceptado a bola
    if intercept:

        # Arrays temporários para capturar as posições da bola até o instante de interceptação
        bolaaux_X = []
        bolaaux_Y = []

        # laço para capturar as posições até o instante de interceptação
        i = 0
        while (arr_t[i] <= tempo):
            bolaaux_X.append(arr_x[i])
            bolaaux_Y.append(arr_y[i])
            i += 1

        # Configura e plota os gráficos
        plt.title("Trajetória do Robô à Bola (até a interceptação) num plano xy")
        plt.plot(arr3, arr4)
        plt.plot(bolaaux_X, bolaaux_Y)
        plt.xlabel("x")
        plt.ylabel("y")

        blue_patch = mpatches.Patch(color='blue', label="Trajetória do Robô")
        orange_patch = mpatches.Patch(color='orange', label="Trajetória da Bola")
        plt.legend(handles=[orange_patch, blue_patch])

        plt.xlim(0, 9)
        plt.ylim(0, 6)

        plt.grid()
        plt.show()

    # Gráfico das trajetórias caso o robô não tenha interceptado a bola
    else:
        # Configura e plota os gráficos
        plt.title("Trajetória do Robô e da Bola num plano xy")
        plt.plot(arr3, arr4)
        plt.plot(arr, arr2)
        plt.xlabel("x/m")
        plt.ylabel("y/m")

        blue_patch = mpatches.Patch(color='blue', label="Trajetória do Robô")
        orange_patch = mpatches.Patch(color='orange', label="Trajetória da Bola")
        plt.legend(handles=[orange_patch, blue_patch])
        plt.xlim(0, 9)
        plt.ylim(0, 6)
        plt.grid()
        plt.show()




# ==================================================#
#       DECOMPOSIÇÃO DA VELOCIDADE E ACELERAÇÃO
# ==================================================#

# Declara tempo e espaço como variáveis simbólicas
t, s = symbols('t s')

def decompVetor(derivadax, derivaday, tituloGraf, componente):
    #  EXTRAÇÃO DO VX/AX E VY/AY DA BOLA
    cx = []
    cy = []

    for i in range(len(arr_t)):
        xCoefAng = derivadax.subs(t, arr_t[i]) #substitui o tempo na derivada (encontra a vel. inst./acel. inst.)
        yCoefAng = derivaday.subs(t, arr_t[i]) #substitui o tempo na derivada (encontra a vel. inst./acel. inst.)
        cx.append(xCoefAng)
        cy.append(yCoefAng)


    doublePlot(# Gráfico da componente em x da bola em função do tempo
               arr_t, cx, componente+"x(t) - " + tituloGraf, 's', 'm/s' if componente == "v" else "m/s^2", componente+"x(t)",

               # Gráfico da componente em y da bola em função do tempo
               arr_t, cy, componente+"y(t) - " + tituloGraf, 's', 'm/s' if componente == "v" else "m/s^2", componente+"y(t)")


criaArrays()



