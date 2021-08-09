import sys
import socket
import select
import threading
from protocol import decode, search

# endereço que queremos disponibilizar o serviço (0.0.0.0 indica todos)
HOST = '0.0.0.0'
# Porta de disponibilidade do serviço
PORTA = 9000

# Abrimos o socket, as opções padrões são AF_INET e STREAM
# AF_INET indica que vamos usar ipv4
# STREAM indica que na camada de transporte vamos usar TCP
sock = socket.socket()

# Criamos o vínculo do endereço para o socket
sock.bind((HOST, PORTA))

# Limitamos as conexões (em espera) para 5
sock.listen(5)

# Muda o socket para não bloqueante (para podermos usar multithreading)
sock.setblocking(False)

inputs = [sys.stdin, sock]

def open_connection(novoSock):
  connected = True
  while connected:
    # Espera uma mensagem da conexão com a quantidade máxima de 1024
    data = novoSock.recv(1024)
    if data:
      # Decodificamos os dados
      filename, word = decode(data)
      # Envia a mensagem recebida de volta a quem enviou
      novoSock.send(search(filename, word))
    else:
      connected = False
  # Fecho o socket conectado
  novoSock.close()

# Enquanto o ativo está conectado
while True:
  # Multiplexo a entrada padrão e a do socket do servidor
  rlist, wlist, xlist = select.select(inputs, [], [])
  # lista de conexões (threads)
  clients = []
  # Para cada input
  for inp in rlist:
    # Se o input for a entrada padrão (stdin)
    if inp == sys.stdin:
      comm = input()
      if comm == 'exit':
        # Espero os clientes disconectarem (as threads finalizarem)
        for c in clients:
          c.join()
        # Fecho o servidor
        sock.close()
        print("Finalizado")
        exit()
    # Senão é o socket do servidor
    else:
      # Esperamos uma conexão
      novoSock, endereco = sock.accept()
      print ('Conectado com:', endereco)
      # Criamos o thread, passando como parâmetro o socket do cliente
      thread = threading.Thread(target = open_connection, args=(novoSock, ))
      # Iniciamos o thread
      thread.start()
      clients.append(thread)
