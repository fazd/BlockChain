
class Cuenta:

    def __init__(self, nombre):
        self.nombre = nombre
        self.monto = 10
    
    def retiro(self,ret):
        if(self.monto < ret):
            return False
        else:
            self.monto = self.monto-ret
            return True

    def consignacion(self,cons):
        self.monto = self.monto + cons

    def __repr__(self):
        return str(self.__dict__)