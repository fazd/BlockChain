import numpy as np
from Crypto.Hash import SHA256

class Block:
    def __init__(self, timestamp, Transactions, prevHash = ""):
        self.timestamp = timestamp
        self.Transactions = Transactions
        self.prevHash = prevHash
        self.nonce = 0
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



    def print(self):
        print("TimeStamp: ", self.timestamp)
        print("Transactions: ", self.Transactions)
        print("Prev Hash: ",self.prevHash)
        print("Hash: ", self.hash)