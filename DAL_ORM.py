
import email
from multiprocessing import connection
from multiprocessing.connection import Client
from operator import truediv
from re import I
from select import select
from sqlite3 import Cursor
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
    numero = AutoField(primary_key=True)
    nombre = TextField()
    direccion = TextField()
    telefono = IntegerField()
    email = TextField(unique=True)

class Tarjeta(BaseModel):
    numero = AutoField(primary_key=True)
    banco = TextField()
    tipo = TextField()

class Cuenta(BaseModel):
    numero = AutoField(primary_key=True)
    numero_cliente= ForeignKeyField(Cliente)
    numero_tarjeta= ForeignKeyField(Tarjeta)
    
class Pago(BaseModel):
    numero = AutoField(primary_key=True)
    estado = TextField()
    numero_tarjeta= ForeignKeyField(Tarjeta)


class Pedido(BaseModel):
    numero = AutoField(primary_key=True)
    estado = TextField()
    numero_cliente = ForeignKeyField(Cliente)

class Pedido_compuesto(BaseModel):
    numero_pedido_hijo = AutoField()
    numero_pedido= ForeignKeyField(Pedido)    
    primary_key= CompositeKey(numero_pedido,numero_pedido_hijo)

    

class Pedido_simple(BaseModel):
    numero_pedido = AutoField(primary_key=True)
    numero_pago = IntegerField()
    numero_pedido=ForeignKeyField(Pedido) 
    numero_cuenta= ForeignKeyField(Cuenta)

    

class Producto(BaseModel):
    numero = AutoField(primary_key=True)
    stock = IntegerField()
    tipo = TextField()
    
class Contiene_prod(BaseModel):
    cantidad= IntegerField()
    numero_producto= ForeignKeyField(Producto)
    numero_pedido_simple= ForeignKeyField(Pedido_simple)
    primary_key= CompositeKey(numero_producto,numero_pedido_simple)

    
def menu():
    ans=True
    while ans:
        print("1. Realizar el alta, baja y modificación de clientes")
        print("2. Ingresar pedidos simples y compuesto")
        print("3. Ingresar articulos en el stock")
        print("4. Listar")
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
            crear_pedido()
        elif option == "3":
            ingresar_articulos()     
        elif option == "4":
            ans3=True
            while ans3:
                print("1. Listar pedidos segun su estado")
                print("2. Listar productos en stock")
                print("3. Listar clientes")
                print("4. Listar pedidos del cliente")
                print("5. Regresar ")
                option3 = input("Seleccione una de las opciones")
                if option3 == "1":
                    listar_pedidos_segun_estado()
                elif option3 == "2":
                    listar_productos_en_stock()
                elif option3 == "3":
                    listar_clientes()
                elif option3 == "4":
                    pedidos_de_cliente()
                elif option3 == "5":
                    ans3=False
                else:
                    print("Opcion invalida")
                    return       
        elif option=="5":
            exit()
        else: 
            print("Opcion invalida")
            menu()


def create_cliente():
    nombre = input("Ingrese nombre")
    direccion = input("Ingrese direccion")
    telefono = input("Ingrese telefono")
    email = input("Ingrese email")
    
    if  Cliente.select(Cliente.email).where(Cliente.email == email).exists():
        print ("Cliente ya registrado")
        return
    else: 
        new_cliente = Cliente.create(nombre = nombre, direccion = direccion, telefono = telefono,email = email)
        numero_cliente=new_cliente
        print(numero_cliente)
        new_cliente.save() 
        print("Cliente registrado correctamente")


    respuesta=True
    while respuesta:
        print ("Desea asociar una trajeta?")
        respuesta=input("si/no")   
        if respuesta=="si":
            banco=input("ingrese nombre del banco")
            tipo=input("ingrese tipo de trajeta (credito/debito)")
            #Falta controlar que solo se puede crear la tarjeta si es que no existe para ese banco y para ese tipo credito/debito

            new_tarjeta=Tarjeta(banco=banco,tipo=tipo)
            new_tarjeta.save()

            numero_tarjeta=new_tarjeta

            new_cuenta=Cuenta.create(numero_cliente=numero_cliente,numero_tarjeta=numero_tarjeta)
            new_cuenta.save()
            print("Cuenta registrada correctamente")
            
        else:
            respuesta=False
            


def delete_cliente():
    numero = input("Ingrese numero del cliente que quiere eliminar")
    if Cliente.select().where(Cliente.numero == numero).exists():
        cliente_delete = Cliente.get(Cliente.numero == numero)
        cliente_delete.delete_instance()
        print("Cliente eliminado correctamente")
        return
    else:
        print ("Cliente no existe")
        return
        
def update_cliente():
    ans= True
    while ans:
        email = input("Ingrese email del cliente que quiere modificar")
        if Cliente.select(Cliente.email).where(Cliente.email==email).exists():
            print ("1. Nombre" )
            print ("2. Direccion")
            print ("3. Telefono" )
            print ("4. Email")
            print ("5. Volver al menu")
            dato_update = input ("Ingrese que tipo de dato desea cambiar")
            valor_update = input("Ingrese que valor quiere colocar en su lugar")
            if (dato_update=="1"):
                query = Cliente.update(nombre = valor_update)
                query.execute()
                print("Modificacion realizada con exito")
            elif (dato_update=="2"):
                query = Cliente.update(direccion = valor_update)
                query.execute()
                print("Modificacion realizada con exito")
            elif (dato_update=="3"):
                query = Cliente.update(telefono = valor_update)
                query.execute()
                print("Modificacion realizada con exito")
            elif (dato_update=="4"):
                query = Cliente.update(email = valor_update)
                query.execute()
                print("Modificacion realizada con exito")
            elif (dato_update=="5"): 
                menu()
            else:
                print("Seleccione una de las opciones correctamente")
                create_cliente()
        else: 
            print("Numero ingresado incorrecto")
            update_cliente()



def crear_pedido():
    print("ingrese el tipo de pedido a realizar")
    print("1. Pedido simple")
    print("2. Pedido compuesto")
    print("3. Salir")
    pedido_a_realizar=input("")

    if pedido_a_realizar=="1":
        email_cliente = input("Ingrese email") 
        numero_cliente=Cliente.select(Cliente.numero).where(Cliente.email==email_cliente)
        numero_cuenta=Cuenta.select(Cuenta.numero).where(Cuenta.numero_cliente==numero_cliente)

        new_pedido = Pedido.create(numero_cliente=numero_cliente,estado="en proceso")
        new_pedido.save()
        numero_pedido=new_pedido
        
        
        mas_productos=True
        cantidad_productos_en_la_compra=0

        while (mas_productos):
            numero_producto=input("ingresar id producto")
            cantidad_a_comprar=int(input("ingresar cantidad que se desea comprar"))
            cantidad_productos_en_la_compra=cantidad_productos_en_la_compra + cantidad_a_comprar
            cantidad_de_producto= Producto.get(Producto.numero == numero_producto).stock

            

            if cantidad_productos_en_la_compra>20 or (cantidad_de_producto-cantidad_a_comprar)<0:
                print("No es posible realizar pedido")
                query = Pedido.update(estado="rechazado")
                query.execute()
                return
            else:
                estado1="realizado"
                numero_pago=registrar_pago(estado1,numero_cuenta)
                new_pedido_simple = Pedido_simple.create(numero_pedido = numero_pedido,numero_cuenta=numero_cuenta,numero_pago=numero_pago)  
                new_pedido_simple.save()

                stock_nuevo= cantidad_de_producto-cantidad_a_comprar
                query = Producto.update(stock = stock_nuevo)
                query.execute()
                
                for pedido in Pedido:
                    if Pedido.numero == numero_pedido:
                        query1 = Pedido.update(estado ="realizado")#como se que estoy cambiando el estado del pedido que quiero
                        query1.execute()
                        
                respuesta=input( "Desea seguir agregando items? (si/no)")
                if respuesta=="no":
                    mas_productos=False
                    
    if pedido_a_realizar=="2":

        email_cliente = input("Ingrese email") 
        numero_cliente=Cliente.select(Cliente.numero).where(Cliente.email==email_cliente)
        numero_cuenta=Cuenta.select(Cuenta.numero).where(Cuenta.numero_cliente==numero_cliente)

        new_pedido1 = Pedido.create(numero_cliente=numero_cliente,estado="en proceso")
        new_pedido1.save()
        numero_pedido1=new_pedido1

        mas_pedidos=True
        while(mas_pedidos):
            new_pedido_compuesto=Pedido_compuesto.create(numero_pedido=numero_pedido1)
            new_pedido_compuesto.save()

            print("Que tipo de pedido se desea realizar")
            print("1-Simple")
            print("2-Compuesto")
            pedido_a_realizar=input("")
            if pedido_a_realizar=="1":
                simple_dentro_de_compuesto(numero_pedido1,numero_cuenta)
            elif pedido_a_realizar=="2":
                new_pedido_compuesto=Pedido_compuesto.create(numero_pedido=numero_pedido1)
                new_pedido_compuesto.save()
            else:
                print("Opcion invalida")
                return     
    if pedido_a_realizar=="3":
        return
    else:
        print("Opcion invalida")
        return

def simple_dentro_de_compuesto(numero_pedido,numero_cuenta):
    cantidad_productos_en_la_compra=0
    mas_productos=True
    while (mas_productos):
        numero_producto=input("ingresar id producto")
        cantidad_a_comprar=int(input("ingresar cantidad que se desea comprar"))
        cantidad_productos_en_la_compra=cantidad_productos_en_la_compra + cantidad_a_comprar
        cantidad_de_producto= Producto.get(Producto.numero == numero_producto).stock
        if cantidad_productos_en_la_compra>20 or (cantidad_de_producto-cantidad_a_comprar)<0:
            print("No es posible realizar pedido")
            query = Pedido.update(estado="rechazado")
            query.execute()
            return
        else:
            estado1="realizado"
            numero_pago=registrar_pago(estado1,numero_cuenta)
            new_pedido_simple = Pedido_simple.create(numero_pedido = numero_pedido,numero_cuenta=numero_cuenta,numero_pago=numero_pago)  
            new_pedido_simple.save()

            stock_nuevo= cantidad_de_producto-cantidad_a_comprar
            query = Producto.update(stock = stock_nuevo)
            query.execute()            
            for pedido in Pedido:
                if Pedido.numero == numero_pedido:
                    query1 = Pedido.update(estado ="realizado")
                    query1.execute()
                        
            respuesta=input( "Desea seguir agregando items? (si/no)")
            if respuesta=="no":
                mas_productos=False
   

def registrar_pago(estado,numero_cuenta):
    numero_tarjeta= Cuenta.get(Cuenta.numero==numero_cuenta).numero_tarjeta

    print(numero_tarjeta)
    
    new_pago= Pago.create(estado=estado,numero_tarjeta=numero_tarjeta)
    print(new_pago)
    new_pago.save()
    
    numero_pago=new_pago
    return numero_pago



def ingresar_articulos():
    stock=input("Ingrese stock del producto")
    tipo=input("ingrese tipo de producto")
    
    new_producto = Producto.create(stock=stock,tipo=tipo)
    new_producto.save()
    print("Producto ingresado correctamente")
    return

def listar_pedidos_segun_estado():
    #Los pedidos en un estado dado
    query = Pedido.select(Pedido.numero, Pedido.estado).order_by(Pedido.numero)
    for pedido in query:
        print(pedido.numero, pedido.estado)


def listar_productos_en_stock():
    #los productos en stock con su disponibilidad
    for producto in Producto.select(Producto.numero,Producto.stock):
        print(producto.numero,producto.stock)

def listar_clientes():
    #Los clientes mostrando sus atributos
        for cliente in Cliente.select(Cliente.numero,Cliente.nombre,Cliente.telefono,Cliente.email,Cliente.direccion):
            print(cliente.numero,cliente.nombre, cliente.telefono,cliente.email,cliente.direccion)


def pedidos_de_cliente():
    #Los pedidos de un cliente
    pg = psycopg2.connect(dbname="pedidos" , user="labuser" , password="labuser",host="192.168.56.101", port=5432)

    sql='''SELECT c.email, p.numero FROM Cliente AS c JOIN Pedido AS p
                            ON (c.numero = p.numero_cliente_id)'''

    cur = pg.cursor()

    cur.execute(sql)
    
    pedidos = cur.fetchall()

    print(pedidos)
    
    cur.close()



if __name__ == "__main__":
    pg_db.connect()
    #pg_db.drop_tables([Cliente,Tarjeta,Pago,Pedido,Pedido_compuesto,Pedido_simple,Producto,Contiene_prod,Cuenta])
    pg_db.create_tables([Cliente,Tarjeta,Pago,Pedido,Pedido_compuesto,Pedido_simple,Producto,Contiene_prod,Cuenta])
    menu()