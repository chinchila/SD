# Usamos o \x00 como separador pois ele não pode aparecer no nome de um arquivo
# se usar /, |, : poderia dar problema e não ler o arquivo que queremos.
SEPARATOR = b"\x00"

# Função que decodifica mensagem, recebe uma
# mensagem e separa ela em nome_do_arquivo,palavra
def decode(msg):
  spl = msg.split(SEPARATOR)
  if len(spl) == 2:
    return spl[0], spl[1]
  else:
    return SEPARATOR, None

# Função que codifica mensagem, recebe nome_do_arquivo
# e palavra e retorna nome_do_arquivo + "\x00" + palavra
def encode(filename, word):
  return filename.encode('utf-8') + SEPARATOR + word.encode('utf-8')

# Função que acha número de ocorrências de word no arquivo filename
# retorna -1 se não ter acesso ao arquivo ou o número de ocorrências.
def search(filename, word):
  if filename == SEPARATOR or word == None:
    return b"Mensagem incorreta"
  # Convertemos filename e word para string
  if type(filename) == bytes:
    filename = filename.decode('utf-8')
  if type(word) == bytes:
    word = word.decode('utf-8')
  # Vamos tentar abrir o arquivo
  try:
    fp = open(filename, "r")
    # Vamos separar todas as plalavras
    data = fp.read().split(" ")
    # retornamos o número de vezes que a palavra aparece na lista data
    # como string em bytes
    return str(data.count(word)).encode('utf-8')
  # Se falhar, é porque não temos acesso ao arquivo, então retorna -1
  except IOError:
    return b"Arquivo nao existe ou nao temos permissao de leitura"
