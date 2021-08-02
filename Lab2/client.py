import socket
from protocol import encode

# Hospedeiro do serviço passivo
HOST = 'localhost'
# Porta de conexão do serviço
PORTA = 9000

# Abrimos o socket, as opções padrões são AF_INET e STREAM
# AF_INET indica que vamos usar ipv4
# STREAM indica que na camada de transporte vamos usar TCP
sock = socket.socket()

# Criamos a conexão
sock.connect((HOST, PORTA))
print("Conectado ao servico", (HOST, PORTA))

# Enquanto não queremos disconectar
while True:
  # Lemos a entrada do dispositivo padrão (stdin)
  filename = input("Digite o arquivo: ")
  word = input("Digite a palavra: ")
  # Codificamos para enviar ao servidor
  data = encode(filename, word)
  # Enviamos os dados lidos para o servidor
  sock.send(data)
  # Esperamos o servidor enviar os dados de volta com a
  # quantidade máxima de 1024
  received = sock.recv(1024)
  # Mostramos os dados recebidos na saída padrão (stdout)
  print(received.decode('utf-8'))

# Fechamos o socket
sock.close()
