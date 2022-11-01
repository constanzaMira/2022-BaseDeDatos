import email
from multiprocessing.connection import Client
from operator import truediv
from re import I
from time import process_time_ns
from venv import create
from peewee import *
from playhouse.postgres_ext import PostgresqlExtDatabase
from playhouse.db_url import connect
import psycopg2

# Connect to a Postgres database.
pg_db = PostgresqlDatabase('pedidos', user='labuser', password='labuser',host='192.168.56.101', port=5432, autoconnect=True)

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
    numero = AutoField(primary_key=True)
    numero_cliente = IntegerField()
    estado = TextField()
    cliente= ForeignKeyField(Cliente, to_field="numero")

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
    

class Producto(BaseModel):
    numero = IntegerField(primary_key=True)
    stock = IntegerField()
    tipo = TextField()
    
class Contiene_prod(BaseModel):
    numero_pedido_simple = IntegerField()
    numero_producto = IntegerField()
    cantidad= IntegerField()
    producto= ForeignKeyField(Producto,to_field="numero")
    pedido_simple= ForeignKeyField(Pedido_simple,to_field="numero_pedido")
    primary_key= CompositeKey(numero_producto,numero_pedido_simple)

    
def menu():
    ans=True
    while ans:
        print("1. Realizar el alta, baja y modificación de clientes")
        print("2. Ingresar pedidos simples y compuesto")
        print("3. Ingresar articulos en el stock")
        print("4. Registrar el pago o no de los pedidos")
        print("5. Salir")
        option = input("Seleccione una de las opciones")

        if option == "1": 
            ans2=True
            while ans2:
                print("1. Alta clientes")
                print("2. Baja clientes")
                print("3. Modificacion clientes")
                print("4. Regresar al menu")
                print("5. Salir")
                option2 = input("Seleccione una de las opciones")
                if option2 == "1":
                    create_cliente()
                elif option2 == "2":
                    delete_cliente()
                elif option2 == "3":
                    update_cliente()
                elif option2 == "4":
                    ans2=False
                elif option2 == "5":
                    exit()
                else:
                    print("Seleccione una de las opciones correctamente")
                    #FIXme
                    return
                    
        elif option == "2":
            ans=True
            while ans:
                print("1. Realizar un pedido")
                print("2. Regresar al menu")
                print("3. Salir")
                option3 = input("Seleccione una de las opciones")
                if option3 == "1":
                    crear_pedido()
                elif option3 == "2":
                    menu()
                elif option3 == "3":
                    exit()
                else: 
                    print("Seleccione una de las opciones correctamente")
                    #FIXme
                    return            
        elif option == "3":
            ingresar_articulos()
            return
        elif option == "4":
            return
        elif option == "5":
            exit()
        else: 
            print("Seleccione una de las opciones correctamente")
            menu()


def create_cliente():
    numero = input("Ingrese numero")
    nombre = input("Ingrese nombre")
    direccion = input("Ingrese direccion")
    telefono = input("Ingrese telefono")
    email = input("Ingrese email")
    
    if not Cliente.select().where(Cliente.numero == numero).exists():
        new_cliente = Cliente.create(numero = numero,nombre = nombre, direccion = direccion, telefono = telefono,email = email)
        new_cliente.save()
        print("Cliente registrado correctamente")
        menu()
    else: 
        print ("Cliente ya registrado")
        create_cliente()

def delete_cliente():
    numero = input("Ingrese numero del cliente que quiere eliminar")
    if Cliente.select().where(Cliente.numero == numero).exists():
        cliente_delete = Cliente.get(Cliente.numero == numero)
        cliente_delete.delete_instance()
        print("Cliente eliminado correctamente")
        menu()
    else:
        print ("Cliente no existe")
        delete_cliente()
        
def update_cliente():
    ans= True
    while ans:
        numero = input("Ingrese numero del cliente que quiere modificar")
        if Cliente.select().where(Cliente.numero==numero).exists():
            print ("1. Numero" )
            print ("2. Nombre" )
            print ("3. Direccion")
            print ("4. Telefono" )
            print ("5. Email")
            print ("6. Volver al menu")
            print ("7. Salir")
            dato_update = input ("Ingrese que tipo de dato desea cambiar")
            valor_update = input("Ingrese que valor quiere colocar en su lugar")
            if (dato_update=="1"):
                query = Cliente.update(numero = valor_update)
                query.execute()
                print("Modificacion realizada con exito")
            elif (dato_update=="2"):
                query = Cliente.update(nombre = valor_update)
                query.execute()
                print("Modificacion realizada con exito")
            elif (dato_update=="3"):
                query = Cliente.update(direccion = valor_update)
                query.execute()
                print("Modificacion realizada con exito")
            elif (dato_update=="4"):
                query = Cliente.update(telefono = valor_update)
                query.execute()
                print("Modificacion realizada con exito")
            elif (dato_update=="5"):
                query = Cliente.update(email = valor_update)
                query.execute()
                print("Modificacion realizada con exito")
            elif (dato_update=="6"): 
                menu()
            elif (dato_update=="7"):
                exit()
            else:
                print("Seleccione una de las opciones correctamente")
                create_cliente()
        else: 
            print("Numero ingresado incorrecto")
            update_cliente()

def create_pedidos(numero_cliente , estado):
    new_pedido = Pedido.create(numero_cliente=numero_cliente,estado=estado)
    new_pedido.save()
    return new_pedido



def crear_pedido():
    print("ingrese el tipo de pedido a realizar")
    print("1. Pedido simple")
    print("2. Pedido compuesto")
    print("3. Salir")
 
    pedido_a_realizar=input("")
    if pedido_a_realizar=="1":
        numero_cliente = input("Ingrese numero de cliente")  
            
        new_pedido=create_pedidos(numero_cliente,"en proceso")
        print(new_pedido.get(Pedido.numero))

        numero_cuenta = input("ingrese numero de cuenta")

        mas_productos=True
        cantidad_productos_en_la_compra=0

        while (mas_productos):
            numero_producto=input("ingresar id producto")
            cantidad_a_comprar=input("ingresar cantidad que se desea comprar")
            cantidad_productos_en_la_compra=cantidad_productos_en_la_compra + cantidad_a_comprar
            cantidad_de_producto= Producto.select(Producto.stock).where(Producto.numero == numero_producto)
            if cantidad_productos_en_la_compra>20 or cantidad_a_comprar-cantidad_de_producto<0:
                print("No es posible realizar pedido")
                return
            else:

                new_pedido_simple = Pedido_simple.create(numero_pedido = numero_pedido,numero_cuenta=numero_cuenta,numero_pago=numero_pago)  
                new_pedido_simple.save()
                stock_nuevo= cantidad_de_producto-cantidad_a_comprar
                query = Producto.update(stock = stock_nuevo)
                query.execute()
                respuesta=input( "Desea seguir agregando items? (Si/No)")
                    
                if respuesta=="No":
                    mas_productos=False 
    if pedido_a_realizar=="2":
             
        numero_cuenta = input("ingrese numero de cuenta")
        numero_cliente = input("Ingrese numero de cliente")  
        
        estado="pendiente"
        new_pedido=Pedido.create(numero_cliente=numero_cliente,estado=estado)
        new_pedido.save()
    
    if pedido_a_realizar=="3":
        return
    else:
        print("Numero ingresado erroneo")
        return





               
   
def realizar_pago(numero_pago, estado):
    numero=input("Ingrese numero de tarjeta")
    new_pago= Pago.create(numero_pago,estado,numero)# numero de pago tiene que ser un autofiedl
    new_pago.save()



def ingresar_articulos():
    numero = input("Ingrese numero de producto")
    stock = input("Ingrese stock del producto")
    tipo=input("ingrese tipo de producto")
    if not Producto.select().where(Producto.numero == numero).exists():
        new_producto = Producto.create(numero = numero,stock=stock,tipo=tipo)
        new_producto.save()
        print("Producto ingresado correctamente")
        menu()
    else: 
        print ("Producto ya registrado")
        respuesta= input("Desea cambiar la cantidad de articulos en stock?(si/no)")
        if respuesta=="si":
            stock1 = input("Ingrese stock del producto")
            query = Producto.update(stock = stock1)
            query.execute()
            menu()
        else:
            menu()


def pedido_compuesto():
    return

if __name__ == "__main__":
    pg_db.connect()
    pg_db.create_tables()
    menu()