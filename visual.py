# -*- coding: utf-8 -*-
from graficos import *
from vpython import *
from robo import *
from sympy import *

# Declara algumas variáveis como globais, serão explicadas durante o código
bolaGol_x = []
bolaGol_y = []
distRoboBola = []
tRoboIntercept = []
xRoboIntercept = []
yRoboIntercept = []
equacaoGol = 0

# Rotaciona objetos
def rotateObj(objeto, angulo, vetor):
    objeto.rotate(angle=angulo, axis=vetor)

# Chute até o gol
def chutaBola(equacao, x):
    # Arrays utilizados para armazenar as coordenadas da bola ao gol
    # (posteriormente utilizados em plotagem de gráficos)
    global bolaGol_x, bolaGol_y

    while bola.pos.x > gol.pos.x and bola.pos.y + bola.radius >= campo.height:
        rate(100)
        bola.rotate(angle=dtheta, axis=vector(0, 1, 0), origin=bola.pos)
        bola.pos.x -= 0.2
        bola.pos.y = 1.6 + equacao.subs(x, bola.pos.x)/80
        bola.pos.z -= 0.02

        bolaGol_x.append(bola.pos.x)
        bolaGol_y.append(bola.pos.y)

    # Imprime comemoração na tela do navegador quando o gol for finalizado
    scene.append_to_caption('<b style="font-size: 24px; color: green; text-shadow: 2px 2px 2px #000; margin-left: 1em">GOOOOOOOOOL!</b>\n\n')  # Mensagem para quando o gol ser feito

    scene.append_to_caption('<b>Ponto de interceptação em Y:</b> {}\n'.format(menorDistY))
    scene.append_to_caption('<b>Ponto de interceptação em X:</b> {}\n'.format(menorDistX))
    scene.append_to_caption('<b>Tempo de interceptação:</b> {}s'.format(menorDistT))


#Encontra a trajetória que a bola levará até o gol (parábola)
def findEquacao():
    global equacaoGol
    p = Symbol('p')
    # Encontra a função quadrática que tem como raízes o x da bola e o x do gol
    equacaoGol = -p**2 +(gol.pos.x + bola.pos.x +1)*p - bola.pos.x*gol.pos.x

    chutaBola(equacaoGol, p)


# Cria o objeto 3D da bola
bola = sphere(pos=vector(1,1.7,1), radius=0.45, make_trail=True, trail_color=color.red, interval = 1,
              texture='assets/textures/bola.png')


# Cria os objetos 3D do campo
campo = box(pos=vector(0, 1, 0), texture='assets/textures/field.jpg', length=90, height=0.5, width=60)
gol = box(pos=vector(-campo.length/2 + 5, 4.5, 0), color=color.white, length=0.5, height=7, width=10)


# Cria e rotaciona o objeto 3D do robô
robo = cylinder(pos=vector(xRobo, 1.4, yRobo), length=1, height=1, width=1, texture='assets/textures/small_size.png',
                make_trail=True, trail_color=color.blue, interval = 1)
roboHead = cylinder(pos=vector(xRobo, robo.height + 0.65, yRobo),
                texture='assets/textures/small_sizetop.png', length=0.8, height=0.8, width=0.8)
rodaEsquerda = cylinder(pos=vector(xRobo, 1.7, yRobo+robo.width-0.5), length=0.1, height=0.7, width=0.7,
                texture='assets/textures/wheel.png')
rodaDireita = cylinder(pos=vector(xRobo, 1.7, yRobo-robo.width+0.5), length=0.1, height=0.7,
                width=0.7, texture='assets/textures/wheel.png')

rotateObj(rodaEsquerda, -pi/2, vector(0,1,0))
rotateObj(rodaDireita, pi/2, vector(0,1,0))
rotateObj(robo, pi/2, vector(0,0,1))
rotateObj(roboHead, pi/2, vector(0,0,1))


#Imprime as instruções iniciais no navegador
scene.caption = """<b>Instruções:</b>
    1) Pressione qualquer tecla para iniciar"""
scene.append_to_caption('\n\n')

scene.append_to_caption("\nPontos iniciais do robô: <b>X</b>: {:.2f} e <b>Y</b>: {:.2f}\n\n".format(xRobo, yRobo))


# Laço esperando que alguma tecla seja pressionada
while True:
    ev = scene.waitfor('keydown')   # Informa ao vPython para que ele aguarde alguma tecla ser pressionada

    # Se alguma tecla for pressionada, inicia a simulação
    if ev.event == 'keydown':

        k = 0 # Contador para atualização das coordenadas do robô em campo
        i = 1 # Contador para atualização das coordenadas da bola em campo
        dtheta=0.08

        # Laço - interrompido quando o robô interceptar a bola ou quando as coordenadas da bola estiverem fora do campo
        while (i < len(arr_x) and bola.pos.x - bola.radius > -campo.length/2):
            rate(120)  # FPS - Taxa de quadros por segundo

            # Atualiza as posições da bola de acordo com os dados extraídos do arquivo e armazenados em arrays
            bola.pos.x += arr_x[i] - bola.pos.x
            bola.pos.z += arr_y[i] - bola.pos.z

            # Animação de rotação da bola
            bola.rotate(angle=dtheta, axis=vector(0, 1, 0), origin=bola.pos)

            i += 1


            # Atualiza as posições do robô de acordo dos dados extraídos da equação da reta e armazenados em arrays
            if k < len(arr_xRobo):
                robo.pos.x = arr_xRobo[k]
                robo.pos.z = arr_yRobo[k]
                roboHead.pos.x = arr_xRobo[k]
                roboHead.pos.z = arr_yRobo[k]

                rodaEsquerda.pos.x = arr_xRobo[k]
                rodaEsquerda.pos.z = arr_yRobo[k] + robo.width - 0.5

                rodaDireita.pos.x = arr_xRobo[k]
                rodaDireita.pos.z = arr_yRobo[k] - robo.width + 0.5

                rodaEsquerda.rotate(angle=2*pi/60)
                rodaDireita.rotate(angle=pi/60)

                k += 1

            # Interrompe o laço se o robo tiver interceptado (colidido) a bola
            if (bola.pos.x  > robo.pos.x - robo.length/10 and
                bola.pos.z >= robo.length/2):
                if (intercept != 0):
                    xRoboIntercept.append(robo.pos.x)
                    yRoboIntercept.append(robo.pos.z)
                    distRoboBola.append(distRB(robo.pos.x - robo.length/10, robo.pos.z, bola.pos.x, bola.pos.z))
                    tRoboIntercept.append(arr_t[i])
                    findEquacao() #Encontra a trajetória que a bola levará até o gol
                    break

            if (bola.pos.x <= 6 and bola.pos.z <= 9):
                # Armazena as distâncias entre o robô e a bola
                distRoboBola.append(distRB(robo.pos.x, robo.pos.z, bola.pos.x, bola.pos.z))


                # Armazena as coodenadas do robô em função do tempo
                xRoboIntercept.append(robo.pos.x)
                yRoboIntercept.append(robo.pos.z)

                tRoboIntercept.append(arr_t[i])

        # Para o laço quando a simulação terminar
        break
