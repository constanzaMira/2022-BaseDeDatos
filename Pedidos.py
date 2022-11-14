

class Pedido():
    def __init__(self, numero, numero_cliente, estado) :
        self.numero=numero
        self.numero_cliente=numero_cliente
        self.estado=estado
    
    def toCollection(self):
        return{
            "Numero":self.numero,
            "Numero_Cliente": self.numero_cliente,
            "Estado": self.estado,

        }

        
    #cerar atributos