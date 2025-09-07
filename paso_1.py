lista_reservas = [] #arreglo vacío para que se muestre como lista la carga de los datos en salida


#definimos las funciones para a carga de reservas..
def consultar_disponibilidad(destino, fecha): 
    for reserva in lista_reservas: #iteración de cada elemento dentro del arreglo lista_reservas
        if reserva["destino"] == destino and reserva["fecha"] == fecha: #comparación de destino guardado en ese reserva, con destino solicitado
                                                                        #uso de and para que ambas comparaciones sean verdaderas
            return False #Si encontró al menos una reserva 
                          #con mismo destino y misma fecha, entonces no hay disponibilidad y 
                          # la función termina en ese instante (no sigue revisando)
    return True #si no encontro fechas que coincidan entonces hay disponibilidad para reservar


#definiendo diccionario de reserva...
def reservar_viaje(cliente, destino, fecha, salida):
    if consultar_disponibilidad(destino, fecha):
        reserva = {
            "cliente": cliente, #definiendo keys
            "destino": destino,
            "fecha": fecha,
            "salida": salida
        }
        lista_reservas.append(reserva) #va agregando elemento en lista
        return "Reserva confirmada"
    else:
        return "No hay disponibilidad en esa fecha"
    
def carga_de_viaje():
    
    cliente = str(input("Ingrese nombre de usuario: ")).strip()
    dni = str(input("Ingrese Dni del cliente: ")).strip()
    fecha = int(input("ingrese entrada de fecha de su viaje : "))  
    salida = int(input("Ingrese salida de fecha de su viaje "))
    
    return cliente, dni, fecha, salida


#carga de lista clientes...
lista_clientes = []

def registrar_cliente(nombre, dni, correo):
    cliente = {"nombre": nombre, "dni": dni, "correo": correo}
    lista_clientes.append(cliente)
    return "Cliente registrado con éxito"
    
#muestra en salida
def mostrar_clientes():
    return lista_clientes

lista_destinos = [
    {"codigo": 1, "nombre": "Buenos Aires", "precio": 500},
    {"codigo": 2, "nombre": "Córdoba", "precio": 400},
    {"codigo": 3, "nombre": "Mendoza", "precio": 600}
]

#muestra en salida
def mostrar_destinos():
    return lista_destinos

def consultar_precio(codigo_destino):
    for destino in lista_destinos:
        if destino["codigo"] == codigo_destino:
            return destino["precio"]
    return None

#seccion donde validamos....
def pedir_texto(mensaje):
    while True:
        texto = input(mensaje).strp() #elimina espacios al ingresar valor
        if texto:
            return texto
        else:
            print("Error: El campo no puede quedar vacío.")
            
def principal():
    for i in range(2):#caraga de dos reservas como ejemplo
        print("--Reserva de su viaje--")
        cliente, dni, destino, fecha, salida = carga_de_viaje()
        mensaje =  reservar_viaje(cliente,destino,fecha,salida)
        print(mensaje)
        
        print("--Lista de reservas confirmadas--")
        for r in lista_reservas:
            print(r)
    
#ejecutar programa   
principal()
