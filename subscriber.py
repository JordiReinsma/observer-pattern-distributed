from circle import *

import sys
import time
import multiprocessing as mp
import pickle
import os
os.environ["SDL_VIDEO_CENTERED"] = "1"
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as gui
import socket

ipSubscriber = "0.0.0.0" #não modificar
portSubscriber = 5050

ipPublisher = "0.0.0.0"
portPublisher = 5454

# Inicializacao da GUI
gui.init()
font = gui.font.SysFont("arial", 12)
gui.display.set_caption("HAPPY LITTLE CIRCLES")
icon = gui.image.load("icon.png")
gui.display.set_icon(icon)
screen = gui.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))

# Lista de circulos do Observer inicia vazia
# para ser preenchida e atualizada pelo Subject
circle_list = []

# Desenha o circulo na tela da GUI
def draw_circle(circle):
  gui.draw.circle(screen, circle.color, circle.pos, circle.size)
  number = font.render(str(circle.id), False, BLACK)
  screen.blit(number, circle.pos)


# Execucao da GUI, que fica executando
# ate alguem fechar a janela, apertar ESC
# ou se atingir o tempo limite

def draw_loop(time_limit):
  global ipSubscriber,portSubscriber,ipPublisher,portPublisher
  tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  dest = (str(ipPublisher), int(portPublisher))
  tcp.connect(dest)
  tcp.send("1")
  tcp.close() 

  screen.fill(WHITE)
  gui.display.update()
  
  running = True
  time_begin = time.time()
  
  while running:
    
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    orig = (str(ipSubscriber),int(portSubscriber))
    tcp.setsockopt(socket .SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp.bind(orig)
    tcp.listen(1)
    objSocket, ipSubscriber = tcp.accept()
    msg = objSocket.recv(8096)
    circle_list = pickle.loads(msg)
    tcp.close()


    screen.fill(WHITE)
    
    for circle in circle_list:
      draw_circle(circle)
    gui.display.update()
    
    # Verifica fim de execucao
    for event in gui.event.get():
      if event.type == gui.QUIT:
        running = False
      elif event.type == gui.KEYDOWN:
        if event.key == gui.K_ESCAPE:
          running = False
    
    if time.time() - time_begin > time_limit:
      running = False
  
  # Termina programa
  tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  dest = (str(ipPublisher), int(portPublisher))
  tcp.connect(dest)
  tcp.send("2")
  tcp.close()
  gui.quit()

# Funcao main
if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Chamada invalida. Uso correto:")
    print("python subscriber.py [tempo_limite_execucao_segundos]")
    sys.exit()
  
  time_limit = int(sys.argv[1])
  
  draw_loop(time_limit)
  
  print('\nProgram ended with %d circles' % len(circle_list))
