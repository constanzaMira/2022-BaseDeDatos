import email
from multiprocessing.connection import Client
from venv import create
from peewee import *
from playhouse.postgres_ext import PostgresqlExtDatabase
from playhouse.db_url import connect
import psycopg2

# Connect to a Postgres database.
pg_db = PostgresqlDatabase('pedidos', user='labuser', password='labuser',host='192.168.56.101', port=5432, autoconnect=True)

#db = PostgresqlExtDatabase('pedidos', user='postgres', register_hstore=True)

#psql_db = PostgresqlDatabase('pedidos', user='postgres')

#db1 = connect("postgresql://postgres:my_password@localhost:5432/pedidos")
#db1.init("pedidos", host='localhost', user='postgres')

class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = pg_db
        
class Cliente(BaseModel):
    numero = IntegerField(primary_key=True)
    nombre = TextField()
    direccion = TextField()
    telefono = IntegerField()
    email = TextField()

class Tarjeta(BaseModel):
    numero = IntegerField(primary_key=True)
    banco = TextField()
    tipo = TextField()

class Cuenta(BaseModel):
    numero = IntegerField(primary_key=True)
    numero_cliente = IntegerField()
    numero_tarjeta = IntegerField()
    cliente= ForeignKeyField(Cliente,to_field="numero" )
    tarjeta= ForeignKeyField(Tarjeta,to_field="numero")
    
class Pago(BaseModel):
    numero = IntegerField(primary_key=True)
    estado = IntegerField()
    numero_tarjeta = IntegerField()
    tarjeta= ForeignKeyField(Tarjeta, to_field="numero")

class Pedido(BaseModel):
    numero = IntegerField(primary_key=True)
    numero_cliente = IntegerField()
    estado = TextField()


class Pedido_compuesto(BaseModel):
    numero_pedido = IntegerField()
    numero_pedido_hijo = IntegerField()
    primary_key= CompositeKey(numero_pedido,numero_pedido_hijo)
    pedido= ForeignKeyField(Pedido, to_field="numero")
    

class Pedido_simple(BaseModel):
    numero_pedido = IntegerField(primary_key=True)
    numero_cuenta = IntegerField()
    numero_pago = IntegerField()
    pedido=ForeignKeyField(Pedido, to_field="numero")
    cuenta= ForeignKeyField(Cuenta, to_field="numero")
    
class Pedido(BaseModel):
    numero = IntegerField(primary_key=True)
    numero_cliente = IntegerField()
    estado = TextField()
    cliente= ForeignKeyField(Cliente, to_field="numero")
    
    
class Contiene_prod(BaseModel):
    numero_pedido_simple = IntegerField()
    numero_pedido = IntegerField()
    pedido= ForeignKeyField(Pedido,to_field="numero")
    pedido_simple= ForeignKeyField(Pedido_simple,to_field="numero_pedido")
    primary_key= CompositeKey(numero_pedido,numero_pedido_simple)
    
class Producto(BaseModel):
    numero = IntegerField(primary_key=True)
    stock = IntegerField()
    tipo = TextField()
    

if __name__ == "__main__":
        pg_db.connect()

        #crear cliente
        cliente1= Cliente.create(numero="23786",nombre="constanza",direccion="francisco aguilar", telefono="098411324", email="cmira@correo.um.edu.uy")
    #   cliente1.save()

    #   dar de baja cliente
    #   cliente = Cliente.get(Cliente.numero == "23786")
    #   cliente.delete_instance()

    #   modificacion de cliente
    #   query=cliente1.update(nombre="lucia")
    #   query.execute()

    #   psql_db.create_tables(cliente , contiene_prod , cuenta , pago , pedido_completo , pedido_simple , pedido , producto , tarjeta)