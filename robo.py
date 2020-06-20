# -*- coding: utf-8 -*-
import math
from graficos import *
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

# Declara algumas variáveis como globais, serão explicadas durante o código
bolaY = bolaX = xRobo = yRobo = menorDistX = menorDistY = menorDistT = m = c = 0
arr_yRobo = []
arr_xRobo = []
arr_t_Aux = []
vRobo = []
acRobo = []
vxRobo = []
axRobo = []
vyRobo = []
ayRobo = []
intercept = False


#Calcula a distância entre o robô e a bola
def distRB(x, y, x2, y2):
    return math.sqrt( (x2-x)**2 + (y2-y)**2 )

#Calcula o tempo da trajetória do robô à bola em função do tempo (enquanto ele possui velocidade constante)
def tempoRB(distancia, velocidade):
    tempo = distancia/velocidade
    return tempo


# Encontra a equação da reta que o robô percorrerá para interceptar a bola (posteriormente utilizada para locomover o robô no vPython)
# Além disso, calcula as componentes e coordenadas do robô, contribuindo para os gráficos
def eqDaReta(ps0Robo, psfRobo, xRobo, yRobo,
             menorDistX, menorDistY, menorDistT,
             vRobo, acRobo, arr_t_Aux):

    global m, c # Coeficiente angular e linear
    global arr_yRobo, arr_xRobo, vxRobo, vyRobo, axRobo, ayRobo # Arrays para armazenar as posições em X e Y do Robô


    # Encontra a equação da reta da trajetória do robô num plano xy
    points = [(ps0Robo[0], ps0Robo[1]), (psfRobo[0], psfRobo[1])]
    x_coords, y_coords = zip(*points)
    A = vstack([x_coords, ones(len(x_coords))]).T
    m, c = lstsq(A, y_coords, rcond=-1)[0]
    # print("Equação da reta = {m}x + {c}".format(m=m, c=c))

    # variável temporária para armazenar a posição inicial do robô em x
    xRoboAux = xRobo

    # ============================================================
    #        ENCONTRA AS COMPONENTES VX/AX E VY/AY DO ROBÔ
    # ============================================================

    vxRobo = []
    axRobo = []
    vyRobo = []
    ayRobo = []

    x = Symbol('x')
    # Derivada da posição da bola
    ds = diff(m*x + c, x)

    for i in range(len(vRobo)):
        # if xRobo != menorDistX and yRobo != menorDistY:
        theta = atan(ds)
        # vx = v*cos(theta)    ax = a*cos(theta)

        vxRobo.append(vRobo[i] * cos(theta))
        axRobo.append(acRobo[i] * cos(theta))

        # vy = v*sen(theta)    ay = a*sen(theta)
        vyRobo.append(vRobo[i] * sin(theta))
        ayRobo.append(acRobo[i] * sin(theta))


    xRoboAux = xRobo
    # ============================================================
    #           ENCONTRA AS COORDENADAS X E Y DO ROBÔ
    # ============================================================
    # Laço para capturar os valores de y e x (utilizando a equação encontrada)
    # Cria-se um array para cada posição, x e y, usados para informar ao vPython as posições que o robô deve seguir.


    i = cte = 0

    cte = 0.02 if intercept == 1 else 0.016
    if (xRoboAux < menorDistX):
        while(xRoboAux < menorDistX):
            arr_yRobo.append(m*xRoboAux + c)
            arr_xRobo.append(xRoboAux)
            if i < len(vxRobo):
                xRoboAux += vxRobo[i]*cte #Incrementa a posição do robô de acordo com o vx encontrado
            else:
                xRoboAux += vxRobo[len(vRobo)-1]*cte
            i+=1
    else:
        while (xRoboAux > menorDistX):
            arr_yRobo.append(m * xRoboAux + c)
            arr_xRobo.append(xRoboAux)
            if i < len(vxRobo):
                xRoboAux -= vxRobo[i]*cte
            else:
                xRoboAux -= vxRobo[len(vxRobo)-1]*cte #decrementa a posição do robô de acordo com o vx encontrado
            i += 1

        for i in range(len(vxRobo)):
            vxRobo[i] *= -1
            vyRobo[i] *= -1
            axRobo[i] *= -1
            ayRobo[i] *= -1



def main():
    global bolaY, bolaX, xRobo, yRobo, menorDistX, menorDistY, menorDistT

    # PARA A BOLA
    bolaX = []
    bolaY = []

    # -------------------------------
    #           PARA O ROBÔ
    # -------------------------------

    # Inicializa uma caixa de diálogo para que o usuário forneça as coordenadas do robô
    master = tk.Tk()

    # Cria as Labels para informar ao usuário a coordenada a ser digitada
    tk.Label(master, text="Digite a coordenada x do robô:").grid(row=0)
    tk.Label(master, text="Digite a coordenada y do robô:").grid(row=1)

    # Cria duas caixas de diálogo, uma para cada coordenada
    xRobo_input = tk.Entry(master)
    yRobo_input = tk.Entry(master)

    # Separa cada campo entrada em uma linha e coluna
    xRobo_input.grid(row=0, column=1)
    yRobo_input.grid(row=1, column=1)

    # Envia as coordenadas fornecidas pelo usuário
    def enviaDados():
        # Instancia o uso global de variáveis utilizáveis em mais de um módulo
        global bolaX, bolaY, xRobo, menorDistX, yRobo, menorDistY, menorDistT, intercept, vRobo, acRobo, arr_t_Aux

        # Verifica se as caixas de diálogo estão vazias, se estiverem o programa não dá continuidade até que esta condição seja falsa
        if xRobo_input.get() != "" and yRobo_input.get() != "":
            xRobo = float(xRobo_input.get())
            yRobo = float(yRobo_input.get())

            # Verifica se as coordenadas digitas obedecem à regra de estarem dentro das dimensões do campo
            if (xRobo < 0.0 or xRobo > 9.0 or yRobo < 0.0 or yRobo > 6.0):
                messagebox.showinfo("Alerta",
                                    "As coordenadas informadas são inválidas! \n"
                                    "Verifique se as mesmas atendem ao requisito de estarem dentro das dimensões do campo.")
            elif (xRobo == 1 and yRobo == 1):
                messagebox.showinfo("Alerta",
                                    "Digite outra coordenada, o robô não pode ter a mesma coordenada incial que a bola devido ao raio!")
            else:
                messagebox.showinfo("Alerta",
                                    "Coordenadas enviadas com sucesso! \nX = {:.2f} \nY = {:.2f}".format(xRobo, yRobo))

                # ---------------------------------------------
                # VERIFICAÇÃO DE POSSIBILIDADE DE INTERCEPTAÇÃO
                # ---------------------------------------------

                # Raio de interceptação = raio do robô + raio da bola
                raio = 0.09 + 0.021

                # Para encontrarmos a equação de velocidade do robô basta integrarmos a aceleração (4m/s^2)
                s, t = symbols('s t') #Declara as variáveis de posição e tempo como simbólicas
                v = integrate(4, t)

                # Calculando o instante em que o robô atinge a sua velocidade máxima
                #(ponto em que ele passa a se movimentar com velocidade cte)
                vMaxT = solve(v - 2.3, t) #Iguala a velocidade máxima (2.3 m/s) à equação da velocidade para calcular o instante
                vMaxT = vMaxT[0]


                #Para encontrarmos a distância percorrida até que o robô atinja a vel. máx, basta integrarmos
                # a equação da velocidade com os limites de integração de 0s até vMaxT(0.575) s
                s_vMax = integrate(v, (t, 0,  vMaxT))


                # Distância máxima do robô em campo
                max = 10.816653826391969

                for i in range(len(arr_x)):
                    # Distância do robô à bola em cada ponto da trajetória
                    if arr_x[i] >= 0.0 and arr_x[i] <= 9.0 and arr_y[i] >= 0.0 and arr_y[i] <= 6.0:
                        distTotal = (distRB(xRobo, yRobo, arr_x[i], arr_y[i])) - raio

                        # Armazena as coordenadas da bola enquanto ela estiver em campo
                        bolaX.append(arr_x[i])
                        bolaY.append(arr_y[i])

                        # armazena a mínima distância possível e o tempo levado para o robô realizá-la
                        if (distTotal < max):
                            max = distTotal
                            menorDistX = arr_x[i]
                            menorDistY = arr_y[i]
                            menorDistT = arr_t[i]

                # ================================================================================================
                # DESCOBRINDO O TEMPO QUE O ROBÔ LEVA PARA COMPLETAR O TRAJETO EM QUE POSSUI VELOCIDADE CONSTANTE
                # ================================================================================================

                # para descobrir esse trajeto basta subtrairmos a menor distância encontrada pela distância que o robô possui vel. variada
                vCteDist = max - s_vMax

                #  após isso, basta aplicarmos a fórmula da velocidade média para descobrirmos o tempo que o robô possui velocidade cte
                tRobo = tempoRB(vCteDist, 2.3)

                # por fim, tendo os dois tempos t1 e t2, basta somá-los para obtermos o tempo total
                tRobo = tRobo + vMaxT # Soma o tempo dos trajetos encontrados t1 e t2 (vel. variada e cte)


                # ======================================================================
                #                  VELOCIDADE E ACELERAÇÃO DO ROBÔ
                # ======================================================================
                # Captura a velocidade e aceleração robô a cada 20 ms até o instante de interceptação
                vRobo = []
                acRobo = []
                arr_t_Aux = []

                i = dv = 0
                while (arr_t[i] != menorDistT):
                    vRobo.append(dv)
                    arr_t_Aux.append(arr_t[i])

                    if arr_t[i] <= vMaxT:
                        dv += 0.08
                        acRobo.append(4)
                    else:
                        dv += 0
                        acRobo.append(0)
                    i += 1



                # Verifica se o tempo levado para o robô percorrer a trajetória encontrada
                # é menor ou igual ao tempo da bola no instante encontrado
                if (tRobo <= menorDistT):

                    global intercept
                    intercept = True

                    # Caixa de diálogo - interceptou
                    print(messagebox.showinfo("Alerta",
                                              "O robô interceptou a bola com sucesso!"))
                    master.destroy() #Fecha a caixa de diálogo e parte para o vPython

                    # Gráfico da bola em campo
                    # plotGrafico([menorDistX, 0], [menorDistY, 3], "Bola ao Gol", 'x(m)', 'y(m)')

                    # Gráfico da bola em campo
                    # plotGrafico(bolaX, bolaY, "Bola em campo", 'x(m)', 'y(m)')

                    # Gráfico x do Robô em função do tempo
                    # plotGrafico([0, tRobo], [xRobo, menorDistX], "X do Robô em função do tempo", 't(s)', 'x(m)')

                    # Gráfico y do Robô em função do tempo
                    # plotGrafico([0, tRobo], [yRobo, menorDistY], "Y do Robô em função do tempo", 't(s)', 'y(m)')

                    # Encontra a equação da reta que o robô percorrerá para interceptar a bola
                    # (posteriormente utilizada para locomover o robô no vPython)
                    eqDaReta([xRobo, yRobo], [menorDistX, menorDistY], xRobo, yRobo,
                             menorDistX, menorDistY, menorDistT, vRobo, acRobo, arr_t_Aux)

                else:
                    # Caixa de diálogo - não interceptou
                    print(messagebox.showinfo("Alerta",
                                              "O robô não conseguiu interceptar a bola"))
                    master.destroy() #Fecha a caixa de diálogo e parte para o vPython

                    # Encontra a equação da reta que o robô percorrerá para interceptar a bola
                    # (posteriormente utilizada para locomover o robô no vPython)
                    eqDaReta([xRobo, yRobo], [menorDistX, menorDistY], xRobo, yRobo,
                             menorDistX, menorDistY, menorDistT, vRobo, acRobo, arr_t_Aux)
        else:
            messagebox.showinfo("Alerta",
                                "Preencha ambos os campos!")


    # Botão para o envio dos dados fornecidos pelo usuário
    btn = tk.Button(master, command=enviaDados)
    btn.grid(row=2, column=1)
    btn.configure(text="Enviar")

    # Dimensões da janela
    master.geometry("300x80")
    master.title("Coordenadas do robô")

    master.mainloop()


main()