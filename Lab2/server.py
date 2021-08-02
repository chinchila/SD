import socket
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

# Esperamos uma conexão
novoSock, endereco = sock.accept()
print ('Conectado com:', endereco)

# Depois da conexão setamos uma flag
connected = True

# Enquanto o ativo está conectado
while connected:
  # Espera uma mensagem da conexão com a quantidade máxima de 1024
  data = novoSock.recv(1024)
  if data:
    # Decodificamos os dados
    filename, word = decode(data)
    # Imprimimos a mensagem recebida
    print("Busca de ocorrências da palavra", word.decode("utf-8"), "no arquivo", filename.decode("utf-8"))
    # Envia a mensagem recebida de volta a quem enviou
    novoSock.send(search(filename, word))
  else:
    connected = False

# Já que a conexão acabou, fechamos os dois sockets
novoSock.close()
sock.close()
print("Desconectado")
