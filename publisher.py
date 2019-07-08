from circle import *

import sys
import time
from multiprocessing import Process
import socket
import pickle
# Inicializacao do queue, para sincronizacao
# das variaveis entre os multiprocesso


# Numero inicial de circulos
NUMBER_CIRCLES = 120
ipPublisher = "0.0.0.0" #não modificar
portPublisher = 5454
portSubscriber = 5050 
# Inicializacao da lista de circulos
circle_list = [Circle(i) for i in range(NUMBER_CIRCLES)]

# Chance das operacoes ocorrerem na lista de circulos
# Total deve ser igual a 1.0
OP_CREATE = 0.2
OP_UPDATE = 0.6 + OP_CREATE
OP_DELETE = 0.2 + OP_UPDATE
subscribers = set()
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


def listenSubscribers():
  global subscribers,ipPublisher,portPublisher
  while(True):
    print("Aguardando Subscriber")
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    orig = (str(ipPublisher), int(portPublisher))
    tcp.setsockopt(socket .SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp.bind(orig)
    tcp.listen(1)
    objSocket, ipSubscriber = tcp.accept()
    msg = objSocket.recv(1024)
    tcp.close()
    #1 para cadastrar subscriber no publisher ,2 para descadastrar o subscriber
    if(str(msg) == "1"):
      subscribers.add(ipPublisher)
    elif(str(msg) == "2"):
      subscribers.discard(ipSubscriber)



  # Cria/Atualiza/Deleta circulos
  # e notifica assinantes apenas das mudanças

numberOfModification = 0
def crud():
  global numberOfModification,portSubscriber,circle_list
  while(True):
    print("modificando circulo")
    global numberOfModification
    chance = random.uniform(0.0, 1.0)
    numberOfModification += 1
    if chance <= OP_CREATE:
      op = 1
      circle = create_circle()
    elif chance <= OP_UPDATE:
      op = 2
      circle = update_circle()
    elif chance <= OP_DELETE:
      op = 3
      circle = delete_circle()
    

    if(numberOfModification > NUMBER_CIRCLES / 10 ):
      print("Enviando modificações")
      tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      for subscriber in subscribers:
        dest = (str(subscriber), int(portSubscriber))
        tcp.connect(dest)
        data = pickle.dumps(circle_list)
        tcp.send(data)
      numberOfModification = 0
      tcp.close()

if __name__ == '__main__':
  crudOfPublisher = Process(target=crud, args=())
  crudOfPublisher.start()

  listen = Process(target=listenSubscribers, args=())
  listen.start()



