# from socket import *
# import pickle
# from constMP import *

# port = GROUPMNGR_TCP_PORT
# membership = []

# def serverLoop():
#   serverSock = socket(AF_INET, SOCK_STREAM)
#   serverSock.bind(('0.0.0.0', port))
#   serverSock.listen(6)
#   while(1):
#     (conn, addr) = serverSock.accept()
#     msgPack = conn.recv(2048)
#     req = pickle.loads(msgPack)
#     if req["op"] == "register":
#       membership.append((req["ipaddr"],req["port"]))
#       print ('Registered peer: ', req)
#     elif req["op"] == "list":
#       list = []
#       for m in membership:
#         list.append(m[0])
#       print ('List of peers sent to server: ', list)
#       conn.send(pickle.dumps(list))
#     else:
#       pass # fix (send back an answer in case of unknown op

#   conn.close()

# serverLoop()
# --------------------------------------------------------------------------------------

from socket import *
import pickle
from constMP import *

port = GROUPMNGR_TCP_PORT
membership = []  # Agora, vai armazenar também o timestamp de Lamport de cada peer

def serverLoop():
    serverSock = socket(AF_INET, SOCK_STREAM)
    serverSock.bind(('0.0.0.0', port))
    serverSock.listen(6)
    
    while(1):
        (conn, addr) = serverSock.accept()
        msgPack = conn.recv(2048)
        req = pickle.loads(msgPack)
        
        # Registro de peer
        if req["op"] == "register":
            ipaddr = req["ipaddr"]
            peer_port = req["port"]
            lamport_clock = req["lamport_clock"]  # Novo campo para o relógio lógico
            
            membership.append((ipaddr, peer_port, lamport_clock))
            print('Registered peer: ', req)
        
        # Listar peers
        elif req["op"] == "list":
            peer_list = [(m[0], m[1]) for m in membership]  # Inclui apenas IP e porta
            print('List of peers sent to server: ', peer_list)
            conn.send(pickle.dumps(peer_list))
        
        else:
            pass  # Responder com erro caso operação desconhecida

        conn.close()

serverLoop()
