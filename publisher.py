from circle import *

import sys
import time
import multiprocessing as mp

# Inicializacao do queue, para sincronizacao
# das variaveis entre os multiprocessos
q = mp.Queue()

# Numero inicial de circulos
NUMBER_CIRCLES = 120

# Inicializacao da lista de circulos
circle_list = [Circle(i) for i in range(NUMBER_CIRCLES)]

# Chance das operacoes ocorrerem na lista de circulos
# Total deve ser igual a 1.0
OP_CREATE = 0.2
OP_UPDATE = 0.6 + OP_CREATE
OP_DELETE = 0.2 + OP_UPDATE

def create_circle():
  global NUMBER_CIRCLES
  circle_list.append(Circle(NUMBER_CIRCLES))
  NUMBER_CIRCLES += 1
  print("Circle %5d [C]reated!" % (NUMBER_CIRCLES))
  return circle_list[-1]

def update_circle():
  if len(circle_list) > 0:
    circle = random.choice(circle_list)
    update = random.choice(circle.update_functions)
    update(circle)
    print("Circle %5d [U]pdated!" % circle.id)
    return circle

def delete_circle():
  if len(circle_list) > 0:
    pos = random.randrange(len(circle_list))
    id = circle_list[pos].id
    circle_list.pop(pos)
    print("Circle %5d [D]eleted!" % id)
    return Circle(id - 1)

class Publisher():
  def __init__(self, name):
    self.name = name
    self.subscribers = set()
  
  # Para registrar novo assinante
  def register(self, who):
    self.subscribers.add(who)
  
  # Remove assinante que deu timeout
  def unregister(self, who):
    self.subscribers.discard(who)
  
  # Envia a lista de circulos para novo assinante
  def initialize_new_subscriber(self, who):
    'ENVIAR TODA A LISTA DE CIRCULOS PRA UM NOVO OBSERVER'
    subscribers(who).initialize(op, circle_list)
  
  # Cria/Atualiza/Deleta circulos
  # e notifica assinantes apenas das mudanças
  def crud(self):
    chance = random.uniform(0.0, 1.0)
    
    if chance <= OP_CREATE:
      op = 1
      circle = create_circle()
    elif chance <= OP_UPDATE:
      op = 2
      circle = update_circle()
    elif chance <= OP_DELETE:
      op = 3
      circle = delete_circle()
    
    for subscriber in self.subscribers:
      'ESTA FUNCAO PRECISA SER APRIMORADA VIA SOCKET'
      subscriber.receive(op, circle)

publisher = Publisher()

def circle_CRUD_loop(time_limit):
  running = True
  time_begin = time.time()
  
  publisher.crud()
    
    if time.time() - time_begin > time_limit:
      running = False

# Funcao main
if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Chamada invalida. Uso correto:")
    print("python publisher.py [tempo_limite_execucao_segundos]")
    sys.exit()
  
  time_limit = int(sys.argv[1])
  
  circle_CRUD_loop(time_limit)
  
  print('\nProgram ended with %d circles' % len(circle_list))
