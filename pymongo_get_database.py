from pymongo import MongoClient
from Pedidos import Pedido



def get_database():
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb://localhost:27017/pedidos"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)

   pedidos = client["pedidos"]
   return pedidos
 
   # Create the database for our example (we will use the same database throughout the tutorial

def menu():
   respuesta=True
   while respuesta:
      print("1. Insertar pedido")
      print("2. Consultar pedido")
      r=input("")
      if r=="1":
         numero = input("Ingrese numero pedido")
         numero_cliente =input("Ingrese numero cliente")
         estado = input("Ingrese estado del pedido")

         pedido = Pedido(numero=numero, numero_cliente=numero_cliente,estado=estado)
         id_registro = insertar_pedido(pedido)
      elif r=="2":
         consultar_pedido()
      else:
         return


def insertar_pedido (pedido):
   dbname = get_database()
   res = dbname["pedidos"].insert_one(pedido.toCollection())
   return res.inserted_id

def consultar_pedido():
   dbname = get_database()
   res = dbname["pedidos"].find()
   print("{:20} {:20} {:20}".format("Numero","Numero_Cliente","Estado"))
   for pedido in res:
      print("{:<20} {:<20} {:<20}".format(pedido["Numero"],pedido["Numero_Cliente"],pedido["Estado"]))

# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":   
  
   # Get the database
   menu()
