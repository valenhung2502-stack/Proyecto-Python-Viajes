from tkinter import *
import sqlite3
from tkinter import ttk 


#################################################### Modelo ######################################################

def conexion():
    con = sqlite3.connect('baseviajes.db')
    return con

def crear_tabla(con):
    
    cursor = con.cursor()
    sql = "CREATE TABLE viajes(dni integer PRIMARY KEY, nombre text, origen text, destino text, fecha text)"
    cursor.execute(sql)
    con.commit()


try:
    con = conexion()
    crear_tabla(con)
except:
    print("Hay un error")
   


def alta(dni, nombre, origen, destino, fecha, tree):
 
    print(dni, nombre, origen, destino, fecha)
    con=conexion()
    cursor=con.cursor()
    data=(dni, nombre, origen, destino, fecha)
    sql="INSERT INTO viajes(dni, nombre, origen, destino, fecha) VALUES(?, ?, ?, ?, ?)"
    cursor.execute(sql, data)
    con.commit()
    print("Estoy en alta todo ok")
    actualizar_treeview(tree)



def baja(tree):
    valor = tree.selection()
    print(valor)   #('I005',)
    item = tree.item(valor)
    print(item)    #{'text': 5, 'image': '', 'values': ['daSDasd', '13.0', '2.0'], 'open': 0, 'tags': ''}
    print(item['text'])
    mi_id = item['text']

    con=conexion()
    cursor=con.cursor()
    #mi_id = int(mi_id)
    data = (mi_id,)
    sql = "DELETE FROM viajes WHERE dni = ?;"
    cursor.execute(sql, data)
    con.commit()
    tree.delete(valor)
    
    

def actualizar_treeview(mitreview):
    records = mitreview.get_children()
    for element in records:
        mitreview.delete(element)

    sql = "SELECT * FROM viajes ORDER BY dni ASC"
    con=conexion()
    cursor=con.cursor()
    datos=cursor.execute(sql)

    resultado = datos.fetchall()
    for fila in resultado:
        print(fila)
        mitreview.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3], fila[4]))



################################################## Pantalla ###########################################################

root = Tk()
root.title("Viajes")
        
titulo = Label(root, text="Ingrese los datos para solicitar un pasaje", bg="DarkOrchid3", fg="thistle1", height=1, width=60)
titulo.grid(row=0, column=0, columnspan=4, padx=1, pady=1, sticky=W+E)

dni = Label(root, text="DNI")
dni.grid(row=1, column=0, sticky=W)
nombre=Label(root, text="Nombre")
nombre.grid(row=2, column=0, sticky=W)
origen=Label(root, text="Origen")
origen.grid(row=3, column=0, sticky=W)
destino=Label(root, text="Destino")
destino.grid(row=4, column=0, sticky=W)
fecha=Label(root, text="Fecha")
fecha.grid(row=5, column=0, sticky=W)


#Variables definidas para tomar valores de campos de entrada
a_val, b_val, c_val, d_val, e_val = IntVar(), StringVar(), StringVar(), StringVar(), StringVar()
w_ancho = 30

entrada1 = Entry(root, textvariable = a_val, width = w_ancho) 
entrada1.grid(row = 1, column = 1)
entrada2 = Entry(root, textvariable = b_val, width = w_ancho) 
entrada2.grid(row = 2, column = 1)
entrada3 = Entry(root, textvariable = c_val, width = w_ancho) 
entrada3.grid(row = 3, column = 1)
entrada4 = Entry(root, textvariable = d_val, width = w_ancho) 
entrada4.grid(row = 4, column = 1)
entrada4 = Entry(root, textvariable = e_val, width = w_ancho) 
entrada4.grid(row = 5, column = 1)


################################# Treeview ##########################################

tree = ttk.Treeview(root)
tree["columns"]=("col2", "col3", "col4","col5")
tree.column("#0", width=90, minwidth=50, anchor=W)
tree.column("col2", width=200, minwidth=80)
tree.column("col3", width=200, minwidth=80)
tree.column("col4", width=200, minwidth=80)
tree.column("col5", width=200, minwidth=80)

tree.heading("#0", text="DNI")
tree.heading("col2", text="Nombre")
tree.heading("col3", text="Origen")
tree.heading("col4", text="Destino")
tree.heading("col5", text="Fecha")
tree.grid(row=10, column=0, columnspan=4)


################################# Botones ############################################


boton_alta=Button(root, text="Alta", command=lambda:alta(a_val.get(), b_val.get(), c_val.get(), d_val.get(), e_val.get(), tree))
boton_alta.grid(row=1, column=2)


boton_baja=Button(root, text="Baja", command=lambda:baja(tree))
boton_baja.grid(row=3, column=2)

#boton_modificar=Button(root, text="Modificar", command=lambda:modificar(b_val.get(), c_val.get(), d_val.get(), e_val.get(), tree))
#boton_modificar.grid(row=5, column=2)



root.mainloop()