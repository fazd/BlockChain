from BlockChain import BlockChain
from Block import Block  
from Validations import isChainValid
from Cuenta import Cuenta
from tipoTrans import tipoTrans
import threading


Chain = BlockChain(2)

c1 = Cuenta("Fabio1")
c2 = Cuenta("Fabio2")
c3 = Cuenta("Fabio3")
c4 = Cuenta("Fabio4")

Chain.agregarCuenta(c1)
Chain.agregarCuenta(c2)
Chain.agregarCuenta(c3)
Chain.agregarCuenta(c4)
Chain.agregarCuenta(c1)

Chain.createTransaction(None,c1,tipoTrans.CONSIGNAR, 20)
Chain.createTransaction(None,c2,tipoTrans.CONSIGNAR, 20)
Chain.createTransaction(None,c3,tipoTrans.CONSIGNAR, 20)
Chain.createTransaction(None,c4,tipoTrans.CONSIGNAR, 20)
Chain.createTransaction(c1,c4, tipoTrans.TRANSFERENCIA,30)

Chain.minePendingTransactions(c1)
Chain.minePendingTransactions(c2)

print(Chain.getLatestBlock().toString()) 

for c in Chain.cuentas:
    print(c.nombre)