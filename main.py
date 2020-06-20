# -*- coding: utf-8 -*-
from vpython import *
from graficos import *
import sys
import tkinter as tk
import tkinter.ttk as ttk
import os.path
from visual import *



def inicializaInterface():
    global val, w, root
    global prog_location
    prog_call = sys.argv[0]
    prog_location = os.path.split(prog_call)[0]
    root = tk.Tk()
    top = JanelaPrincipal (root)
    root.resizable(0, 0)
    root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='assets/root.png'))
    root.mainloop()

w = opcSelecionada = None

def create_JanelaPrincipal(root, *args, **kwargs):
    global w, w_win, rt
    global prog_location
    prog_call = sys.argv[0]
    prog_location = os.path.split(prog_call)[0]
    rt = root
    w = tk.Toplevel (root)
    top = JanelaPrincipal (w)
    return (w, top)

def destroy_JanelaPrincipal():
    global w
    w.destroy()
    w = None

class JanelaPrincipal:
    def __init__(self, top=None):
        top.geometry("647x499+340+115")
        top.title("Projeto Ora Bolas")
        top.configure(background="#d9d9d9")

        # =============================#
        #           FUNDO
        # =============================#
        # Plano de fundo dinâmico (variado se o robô interceptar ou não)
        if intercept:
            imgFundo = os.path.join(prog_location,"assets/bg_success.png")
        else:
            imgFundo = os.path.join(prog_location, "assets/bg_fail.png")
        self._fundo = tk.PhotoImage(file=imgFundo)

        self.Fundo = tk.Label(top)
        self.Fundo.place(relx=-0.015, rely=-0.02, height=524, width=664)
        self.Fundo.configure(background="#d9d9d9", disabledforeground="#a3a3a3", foreground="#000000", image=self._fundo,
                             text='''Label''', width=664)


        #RELATORIO
        def verRelatorio():

            mensagem =  "Dados sobre o robô: " \
                        "\n• Robô: Small Size" \
                        "\n• Raio da bola: 21 mm" \
                         "\n• Raio: 90mm" \
                        "\n• Velocidade máxima: 2.3 m/s" \
                        "\n• Aceleração: 4 m/s²"
            if intercept:
                mensagem += "\n\nDados sobre a interceptação:"\
                            "\n• O robô interceptou a bola com sucesso! ;-)"\
                            "\n• Tempo de interceptação: {}s"\
                            "\n• Coordenada em X da interceptação: {}"\
                            "\n• Coordenada em Y da interceptação: {}".format(menorDistT, menorDistX, menorDistY)
            else:
                mensagem += "\n\nDados sobre a interceptação:"\
                            "\n• O robô não interceptou a bola :-("\

            mensagem += "\n\nSoftwares Utilizados: " \
                        "\n• Pycharm - IDE para o desenvolvimento do código"\
                        "\n• EXCEL - x(t) da bola: x = -0,008t^3 - 0,15t^2 + 2,5t + 1"\
                        "\n• MATLAB - y(t) da bola: y = -0.2*t^(1.5) + 1.6*t + 1"

            print(messagebox.showinfo("Dados obtidos:", mensagem))



        # =============================================#
        #      RELATÓRIO (botão - abrirá outra janela)
        # =============================================#
        self.BotaoRelatorio = tk.Button(top, command=verRelatorio)
        self.BotaoRelatorio.place(relx=0.263, rely=0.521, height=44, width=260)
        self.BotaoRelatorio.configure(activebackground="#ececec", activeforeground="#000000", background="#d9d9d9",
        disabledforeground="#a3a3a3", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black",
        pady="0", text='''Visualizar Dados''', width=157)


        # =============================#
        #      GRÁFICOS (combobox)
        # =============================#
        self.box_value = tk.StringVar()
        self.box_value.set("Selecione um gráfico")
        self.OpcGraficos = ttk.Combobox(top, textvariable= self.box_value,
                                state='readonly')

        self.OpcGraficos.place(relx=0.263, rely=0.681, relheight=0.082
                , relwidth=0.553)
        self.OpcGraficos.configure(width=240)

        # Captura o valor selecionado no combobox (pelo primeiro caracter = número) e o retorna para a variável opcSelecionada
        def callback(eventObject):
            global opcSelecionada
            try:
                opcSelecionada = int(self.OpcGraficos.get().split()[0])
                self.viewGrafico['state'] = 'normal'
            except:
                self.viewGrafico['state'] = 'disabled' #Desativa o botão se o usuário selecionar uma opção inválida, como: "PARA O ROBÔ"

        # Lista as opções de gráficos no combobox
        self.OpcGraficos['values']=('------------------- PARA A BOLA: ---------------------',
                                    '1 - Coordenadas x(t) e y(t)',
                                    '2 - Componentes vx(t) e vy(t) da velocidade',
                                    '3 - Componentes ax(t) e ay(t) da aceleração',
                                    '4 - Bola ao Gol',
                                    '-------------------  PARA O ROBÔ: --------------------',
                                    '5 - Coordenadas x(t) e y(t) do robô',
                                    '6 - Componentes vx(t) e vy(t) da velocidade do robô',
                                    '7 - Componentes ax(t) e ay(t) da aceleração do robô',
                                    '8 - Velocidade do robô em função do tempo',
                                    '9 - Aceleração do robô em função do tempo',
                                    '-------------------  PARA AMBOS: --------------------',
                                    '10 - Trajetória da bola e do robô num plano',
                                    '11 - Distância relativa entre o robô e a bola em função do tempo')

        self.OpcGraficos.current(0) # Varia as seleções do combobox
        self.OpcGraficos.bind("<<ComboboxSelected>>", callback)
        self.OpcGraficos.set("Selecione um gráfico") #Texto inicial - para quando não houver nada selecionado

        # ====================================================================#
        #         CHAMA GRÁFICOS - Através das numerações dadas no combobox
        # ====================================================================#

        def invocaGrafico():

            # global bolaX, bolaY, xRobo, menorDistX, yRobo, menorDistY, menorDistT, intercept

            if opcSelecionada == 1:
                doublePlot(arr_t, arr_x, "x(t) da bola", 't/s', 'x/m', 'x(t)', # Gráfico da posição em X da bola em função do tempo
                           arr_t, arr_y, "y(t) da bola", 't/s', 'y/m', 'y(t)') # Gráfico da posição em Y da bola em função do tempo

            elif opcSelecionada == 2:
                # equações encontradas x(t) da bola: x = -0,008t^3 - 0,15t^2 + 2,5t + 1
                #                      y(t) = -0.2*t^(1.5) + 1.6*t + 1
                # Decompondo a VELOCIDADE, basta derivar uma vez
                decompVetor(diff(-0.008 * t ** 3 - 0.15 * t ** 2 + 2.5 * t + 1, t),
                            diff( -0.2*t**1.5 + 1.6*t + 1,t),
                            "da bola","v")

            elif opcSelecionada == 3:
                # Decompondo a ACELERAÇÃO, basta derivar duas vezes
                decompVetor(diff(diff( -0.008*t**3 - 0.15*t**2 + 2.5*t + 1,t),t),
                            diff(diff( -0.2*t**1.5 + 1.6*t + 1,t),t),
                            "da bola", "a")


            elif opcSelecionada == 4:
                plotGrafico(bolaGol_x,bolaGol_y, "Bola ao Gol", 'x/m', 'y/m')

            elif opcSelecionada == 5:
                doublePlot(tRoboIntercept, xRoboIntercept, "x(t) do Robô", "t/s", "x/m", 'x(t)',  # Gráfico x(t) do robô
                           tRoboIntercept, yRoboIntercept, "y(t) do robô", "t/s", "y/m", 'y(t)')  # Gráfico y(t) do robô

            elif opcSelecionada == 6:
                doublePlot(arr_t_Aux, vxRobo, "Vx(t) do robô", "t(s)", "Vx(m/s)", 'Vx(t)',  # Gráfico vx(t) do robô
                           arr_t_Aux, vyRobo, "Vy(t) do robô", "t(s)", "Vy(m/s)", 'Vy(t)')  # Gráfico vy(t) do robô

            elif opcSelecionada == 7:
                doublePlot(arr_t_Aux, axRobo, "Ax(t) do robô", "t(s)", "Ax(m/s^2)", 'Ax(t)',  # Gráfico sx(t) do robô
                           arr_t_Aux, ayRobo, "Ay(t) do robô", "t(s)", "Ay(m/s^2)", 'Ay(t)')  # Gráfico sy(t) do robô

            elif opcSelecionada == 8:
                plotGrafico(arr_t_Aux, vRobo, "V(t) do robô", 's', 'm/s')

            elif opcSelecionada == 9:
                plotGrafico(arr_t_Aux, acRobo, "a(t) do robô", 's', 'm/s^2')

            elif opcSelecionada == 10:
                # Caso intercepte, analisa as coordenadas da bola até o menor tempo encontrado (instante de interceptação)
                if intercept:
                    plotTrajetorias(bolaX, bolaY, [xRobo, menorDistX], [yRobo, menorDistY], menorDistT, intercept)
                # senão analisa todas as coordenadas extreídas do arquivo trajetoria.txt
                else:
                    plotTrajetorias(arr_x, arr_y, [xRobo, menorDistX], [yRobo, menorDistY], menorDistT, intercept)

            elif opcSelecionada == 11:
                plotGrafico(tRoboIntercept, distRoboBola, "Distância relativa entre o robô e a bola em função do tempo", 's', 'm')



        # Botão para que o usuário informe o gráfico a ser exibido
        eyeImg = os.path.join(prog_location,"assets/eye.png")
        self._img1 = tk.PhotoImage(file=eyeImg)

                            # O botão só é ativado quando a opção selecionada for um gráfico
        #                                             /\
        #                                             ||
        self.viewGrafico = tk.Button(top, state = 'disabled', command=invocaGrafico)

        self.viewGrafico.place(relx=0.82, rely=0.681)
        self.viewGrafico.configure(height=34, width=50, activebackground="#ececec", activeforeground="#000000",
                               background="#d9d9d9", disabledforeground="#a3a3a3", foreground="#000000",
                               highlightbackground="#d9d9d9", highlightcolor="black", image=self._img1,
                               pady="0", text='''Visualizar''')

if __name__ == "__main__":
    inicializaInterface()







