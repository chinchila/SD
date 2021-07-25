import socket

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
# Iniciamos o valor de disconect para False pois acabamos de conectar
disconnect = False

# Enquanto não queremos disconectar
while not disconnect:
  # Lemos a entrada do dispositivo padrão (stdin)
  data = input()
  # Se não for a mensagem de sair
  if(data != 'exit'):
    # Enviamos os dados lidos para o servidor
    sock.send(data.encode('utf-8'))
    # Esperamos o servidor enviar os dados de volta com a
    # quantidade máxima de 1024
    received = sock.recv(1024)
    # Mostramos os dados recebidos na saída padrão (stdout)
    print(received.decode('utf-8'))
  # Se for, então disconectamos
  else:
    disconnect = True

# Fechamos o socket
sock.close()
