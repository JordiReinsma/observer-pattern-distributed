from circle import *

import sys
import time
import multiprocessing as mp

import os
os.environ["SDL_VIDEO_CENTERED"] = "1"
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as gui

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

class Subscriber:
  def __init__(self, name):
    self.name = name
  
  def subscribe(self, address, port):
    'SE REGISTRA NO PUBLISHER ESPECIFICADO VIA SOCKET'
    
    'QUANDO ESTIVER REGISTRADO, PEDE A LISTA TODA DE CIRCULOS'
    global circle_list
    circle_list = circles
  
  def receive(self, op, circle):
    if op == 1:
      'CRIOU-SE CIRCULO'
    elif op == 2:
      'ALTEROU-SE CIRCULO'
    elif op == 3:
      'DELETOU-SE CIRCULO'

# Execucao da GUI, que fica executando
# ate alguem fechar a janela, apertar ESC
# ou se atingir o tempo limite
def draw_loop(time_limit):
  screen.fill(WHITE)
  gui.display.update()
  
  running = True
  time_begin = time.time()
  
  while running:
    # circle_op = random.uniform(0.0, 1.0)
    # if circle_op < 0.2:
      # number_circles += 1
      # create_circle(number_circles)
    # if circle_op < 0.8:
      # update_circle()
    # else:
      # delete_circle()
    'ESCUTA NOTIFY DO SUBJECT E FAZ UMA DAS ACOES ACIMA'
    
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
