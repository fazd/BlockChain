from Block import Block
from datetime import date
from Transaction import Transaction
from tipoTrans import tipoTrans

class BlockChain:
    def __init__(self, difficulty):
        self.chain = [ self.create_genesis()]
        self.difficulty = difficulty
        self.pendingTransactions = []
        self.miningReward = 100
        self.cuentas = []

    def agregarCuenta(self,cuenta):
        
        if(cuenta in self.cuentas):
            print("La cuenta no pudo ser agregada, ya hay alguien con ese usuario")
        else:
            self.cuentas.append(cuenta)
            print("La cuenta ha sido agregada exitosamente")

    def create_genesis(self ):
        return Block("fecha", "Genesis","0")
    

    def getLatestBlock(self):
        return self.chain[len(self.chain)-1]

    def minePendingTransactions (self,rewardAddress):
        newTrans = []
        for tr in self.pendingTransactions:
            res = tr.execute()
            if(res):
                newTrans.append(tr)

        block = Block(date.today(),newTrans,self.getLatestBlock().hash)
        block.mineBlock(self.difficulty)
        print("Block mined")
        self.chain.append(block)
        self.pendingTransactions = [Transaction(None, rewardAddress,tipoTrans.CONSIGNAR, self.miningReward)]
    
    def createTransaction(self, c1, c2,tipoTrans, amount):
        trans = Transaction(c1,c2,tipoTrans,amount)
        self.pendingTransactions.append(trans)
    

    def getBalanceOfAdress(self, adress):
        balance = 0
        for block in self.chain:
            for trans in block:
                if(trans.fromAdress == adress):
                    balance-=trans.amount
                elif(trans.toAdress == adress):
                    balance+= trans.amount
        
        return balance


    def printClients(self):
        for i in self.cuentas:
            print("nanme: ", i.nombre)
            print("Amount: ",i.monto)

    def print(self):
        for i in self.chain:
            print("Bloque: ")
            i.print()
            print("-----------------------------------------------")

    
    def solveConflict(self,Bloque1, Bloque2):
        if(Bloque1.nonce > Bloque2.nonce):
            return Bloque1
        else:
            return Bloque2
        