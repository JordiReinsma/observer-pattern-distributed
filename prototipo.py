import sys
import time
import random

import os
os.environ["SDL_VIDEO_CENTERED"] = "1"
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as gui

# Cores para a GUI
BLACK  = (  0,   0,   0)
WHITE  = (255, 255, 255)
RED    = (255,  63,  63)
GREEN  = (  0, 240,  15)
BLUE   = ( 64, 127, 255)
YELLOW = (255, 239,   0)
PURPLE = (200,  15, 255)
CYAN   = (  0, 239, 255)
ORANGE = (239, 127,   0)
COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE, CYAN, ORANGE]

# Tamanho da tela
SCREEN_WIDTH  = 1000
SCREEN_HEIGTH = 640

# Raio minimo e maximo dos circulos
MIN_RADIUS = 2
MAX_RADIUS = 12

# Inicializacao da GUI
gui.init()
font = gui.font.SysFont("arial", 12)
gui.display.set_caption("HAPPY LITTLE CIRCLES")
icon = gui.image.load("icon.png")
gui.display.set_icon(icon)
screen = gui.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))

# Classe circulo, possui cor, raio,
# identificador e posicao X e Y
class Circle():
  def __init__(self, i):
    self.id = i + 1
    self.color = random.choice(COLORS)
    self.pos = (random.randint(MAX_RADIUS, SCREEN_WIDTH  - MAX_RADIUS),
                random.randint(MAX_RADIUS, SCREEN_HEIGTH - MAX_RADIUS))
    self.size = random.randint(MIN_RADIUS, MAX_RADIUS)
  
  # Desenha o circulo na tela da GUI
  def draw(self):
    gui.draw.circle(screen, self.color, self.pos, self.size)
    number = font.render(str(self.id), False, BLACK)
    screen.blit(number, self.pos)
  
  # Troca a cor do circulo
  def update_color(self):
    self.color = random.choice(COLORS)
  
  # Troca a posicao do circulo
  def update_position(self):
    self.pos = (random.randint(MAX_RADIUS, SCREEN_WIDTH  - MAX_RADIUS),
                random.randint(MAX_RADIUS, SCREEN_HEIGTH - MAX_RADIUS))
  
  # Troca o raio do circulo
  def update_size(self):
    self.size = random.randint(MIN_RADIUS, MAX_RADIUS)
  
  # Lista das funcoes de update
  update_functions = [update_color, update_position, update_size]

# Inicializa os circulos
NUMBER_CIRCLES = 120
circle_list = [Circle(i) for i in range(NUMBER_CIRCLES)]

def create_circle(i):
  circle_list.append(Circle(i))
  print("Circle %5d [C]reated!" % (i + 1))

def update_circle():
  if len(circle_list) > 0:
    circle = random.choice(circle_list)
    update = random.choice(circle.update_functions)
    update(circle)
    print("Circle %5d [U]pdated!" % circle.id)

def delete_circle():
  if len(circle_list) > 0:
    pos = random.randrange(len(circle_list))
    id = circle_list[pos].id
    circle_list.pop(pos)
    print("Circle %5d [D]eleted!" % id)

def main_loop(time_limit):
  global NUMBER_CIRCLES
  
  screen.fill(WHITE)
  gui.display.update()
  
  running = True
  time_begin = time.time()
  
  while running:
    circle_op = random.uniform(0.0, 1.0)
    if circle_op < 0.2:
      NUMBER_CIRCLES += 1
      create_circle(NUMBER_CIRCLES)
    if circle_op < 0.8:
      update_circle()
    else:
      delete_circle()
    
    screen.fill(WHITE)
    
    for circle in circle_list:
      circle.draw()
    gui.display.update()
    
    for event in gui.event.get():
      if event.type == gui.QUIT:
        running = False
      elif event.type == gui.KEYDOWN:
        if event.key == gui.K_ESCAPE:
          running = False
    
    if time.time() - time_begin > time_limit:
      running = False
  
  gui.quit()

# Funcao main
if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Chamada invalida. Uso correto:")
    print("python tp3.py [tempo_limite_execucao_segundos]")
    sys.exit()
  
  time_limit = int(sys.argv[1])
  
  main_loop(time_limit)
  
  print('\nProgram ended with %d circles' % len(circle_list))