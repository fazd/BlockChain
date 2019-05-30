import numpy as np
from Crypto.Hash import SHA256

class Block:
    def __init__(self, timestamp, Transactions, prevHash = "", nonce=0):
        self.timestamp = timestamp
        self.Transactions = Transactions
        self.prevHash = prevHash
        self.nonce = nonce
        self.hash = self.calcHash()
    

    def calcHash(self):
        aux = str.encode( str(self.prevHash) + str(self.timestamp) + 
        str(self.Transactions)+ str(self.nonce))
        h = SHA256.new()
        h.update(aux)
        return h.hexdigest()

    def mineBlock(self, dif):
        while(self.hash[0:dif] != ''.join(["0"]*dif)):
            self.nonce+=1
            self.hash = self.calcHash()     

        print("Block Mined")       


    def __repr__(self):
        return str(self.__dict__)



    def print(self):
        print("TimeStamp: ", self.timestamp)
        print("Transactions: ", self.Transactions)
        print("Prev Hash: ",self.prevHash)
        print("Hash: ", self.hash)

    def toString(self):
        return str(self.timestamp) + ";"+ self.prevHash+ ";"+self.hash+";"+ str(self.nonce)
        