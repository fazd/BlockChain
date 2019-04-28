from tipoTrans import tipoTrans

class Transaction:

    def __init__(self, cuentaSal, cuentaEntr, tipoTrans, monto):
        self.cuentaSal = cuentaSal
        self.cuentaEntr = cuentaEntr
        self.tipoTrans =tipoTrans 
        self.monto = monto

    def execute(self):
        if(self.tipoTrans == tipoTrans.CONSIGNAR):
            return self.addMonto()
        elif(self.tipoTrans == tipoTrans.TRANSFERENCIA):
            return self.transferencia()

    def addMonto(self):
        self.cuentaEntr.monto = self.cuentaEntr.monto + self.monto
        print("Transacción realizada exitosamente")
        return True
    
    def  transferencia(self):        
        if(self.cuentaSal.monto >= self.monto):
            self.cuentaSal.monto = self.cuentaSal.monto - self.monto
            self.cuentaEntr.monto = self.cuentaEntr.monto + self.monto
            print("Transaccion realizada exitosamente")
            return True
        else:
            print("Transaccion invalida, no hay fondos suficientes")
            return False