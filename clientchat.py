import socket
import select
import errno
import sys
from BlockChain import BlockChain
from Block import Block  
from Validations import isChainValid
from Cuenta import Cuenta
from tipoTrans import tipoTrans

Chain = BlockChain(2) 
# transfer valeria 20
# mining block 
# new block  info del bloque
# Collision 


def typeMessage(username,message):
    vec = message.split(" ")
    if(vec[0] == "transfer"):
        fromAdd = Chain.find(username)
        toAdd = Chain.find(vec[1])
        val = int(vec[2])
        Chain.createTransaction(fromAdd,toAdd,tipoTrans.TRANSFERENCIA, val)
        return 0

    elif (vec[0] == "newBlock"):
        for c in Chain.pendingTransactions:
            c.execute()
        blocklineal = transform(vec[1],Chain.pendingTransactions)
        Chain.pendingTransactions = []
        Chain.addBlock(blocklineal)
        return 0

    elif(vec[0]== "newAccount"):
        c = Cuenta(vec[1])
        Chain.agregarCuenta(c)
        message = "newAccount "+ my_username
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)
        
        return 1




def ignore(message):
    #return True
    #print(message)
    message = str(message)
    if(message.find("newAccount") != -1):
        return False
    return True


def transform (blockLineal,copia):
    print("Original:    ",blockLineal)
    print("copia: ", copia)
    vec = blockLineal.split(";")
    date = vec[0]
    prevHash = vec[1]
    hashA = vec[2]
    nonce = vec[3]
    Bl = Block(date,copia,prevHash,nonce)
    print("El bloque generado es")
    print(Bl.__repr__)
    return Bl


def trad(message):
    vec = message.split(" ")
    if(vec[0]=="print"):
        for c in Chain.cuentas:
            print(c.nombre)
    
    elif(vec[0]=="transfer"):
        fromAdd = Chain.find(my_username)
        toAdd = Chain.find(vec[1])
        val = int(vec[2])
        Chain.createTransaction(fromAdd,toAdd,tipoTrans.TRANSFERENCIA, val)

    elif(vec[0]=="printTrans"):
        for t in Chain.pendingTransactions:
                t.printTrans()
    
    elif(vec[0] =="mine"):
        copia = Chain.pendingTransactions
        Chain.minePendingTransactions(Chain.find(my_username))
        message = "newBlock "+ Chain.getLatestBlock().toString()
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)


        message = "transfer "+ my_username + " "+ str(Chain.miningReward)
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)

    elif(vec[0]=="printBlocks"):
        Chain.print()
        



HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234
my_username = input("Username: ")

c1 = Cuenta(my_username)
Chain.agregarCuenta(c1)

# Create a socket
# socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((IP, PORT))

# Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
client_socket.setblocking(False)

# Prepare username and header and send them
# We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)
message = "newAccount "+ my_username
message = message.encode('utf-8')
message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(message_header + message)


while True:

    # Wait for user to input a message
    message = input(f'{my_username} > ')

    # If message is not empty - send it
    if message:

        # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
        trad(message)
        message = message.encode('utf-8')
        
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)

    try:
        # Now we want to loop over received messages (there might be more than one) and print them
        while True:
            # Receive our "header" containing username length, it's size is defined and constant
            username_header = client_socket.recv(HEADER_LENGTH)
            # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()
            # Convert header to int value
            username_length = int(username_header.decode('utf-8').strip())
            # Receive and decode username
            username = client_socket.recv(username_length).decode('utf-8')
            # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')
            op = typeMessage(username,message)


            # Print message
            if(op):
                message = "newAccount "+ my_username
                message = message.encode('utf-8')
                message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                client_socket.send(message_header + message)
            
            if(message != "print" and ignore(message)):
                print(f'{username} > {message}')

    except IOError as e:
        # This is normal on non blocking connections - when there are no incoming data error is going to be raised
        # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
        # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
        # If we got different error code - something happened
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()

        # We just did not receive anything
        continue

    except Exception as e:
        # Any other exception - something happened, exit
        print('Reading error: {}'.format(str(e)))
        sys.exit()