from tkinter import *
from tkinter.messagebox import *
import sqlite3
from tkinter import ttk
import re

def base_viajes():
    con = sqlite3.connect('baseviajes.db')
    return con

def crear_tabla(con):
    cursor = con.cursor()
    sql = """CREATE TABLE IF NOT EXISTS viajes
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             nombre varchar(20) NOT NULL,
             apellido varchar(20) NOT NULL,
             pasaje varchar(20),
             horario varchar(5))
    """
    cursor.execute(sql)
    con.commit()
crear_tabla(base_viajes())

def alta(nombre, apellido, pasaje, horario, tree):

    patron_nombre = r"^[A-Za-záéíóúÁÉÍÓÚñÑ ]{1,20}$"
    patron_apellido = r"^[A-Za-záéíóúÁÉÍÓÚñÑ ]{1,20}$"
    patron_pasaje = r"^[A-Z0-9]{1,20}$"
    patron_horario = r"^[0-9:]{1,5}$"
    if not re.match(patron_nombre, nombre.get()):
        showerror("Error", "Nombre inválido")
        return
    if not re.match(patron_apellido, apellido.get()):
        showerror("Error", "Apellido inválido")
        return
    if not re.match(patron_pasaje, pasaje.get()):
        showerror("Error", "Pasaje inválido")
        return
    if not re.match(patron_horario, horario.get()):
        showerror("Error", "Horario inválido")
        return

    con = base_viajes()
    cursor = con.cursor()
    cursor.execute(
        "INSERT INTO viajes (nombre, apellido, pasaje, horario) VALUES (?, ?, ?, ?)",
        (nombre.get(), apellido.get(), pasaje.get(), horario.get())
    )
    con.commit()
    con.close()
    actualizar_treeview(tree)

def actualizar_treeview(mitreview):
    records = mitreview.get_children()
    for element in records:
        mitreview.delete(element)
    sql = "SELECT * FROM viajes ORDER BY id ASC"
    con = base_viajes()
    cursor = con.cursor()
    datos = cursor.execute(sql)
    resultado = datos.fetchall()
    for fila in resultado:
        mitreview.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3], fila[4]))

root = Tk()
root.title("Administrar Viajes")

titulo = Label(root, text="Ingrese sus datos", bg="DarkOrchid3", fg="thistle1", height=1, width=60)
titulo.grid(row=0, column=0, columnspan=4, padx=1, pady=1, sticky=W+E)

Label(root, text="Nombre").grid(row=1, column=0, sticky=W)
Label(root, text="Apellido").grid(row=2, column=0, sticky=W)
Label(root, text="Pasaje").grid(row=3, column=0, sticky=W)
Label(root, text="Horario").grid(row=4, column=0, sticky=W)


a_val, b_val, c_val, d_val = StringVar(), StringVar(), StringVar(), StringVar()
w_ancho = 20

entrada1 = Entry(root, textvariable=a_val, width=w_ancho)
entrada1.grid(row=1, column=1)
entrada2 = Entry(root, textvariable=b_val, width=w_ancho)
entrada2.grid(row=2, column=1)
entrada3 = Entry(root, textvariable=c_val, width=w_ancho)
entrada3.grid(row=3, column=1)
entrada4 = Entry(root, textvariable=d_val, width=w_ancho)
entrada4.grid(row=4, column=1)

tree = ttk.Treeview(root)
tree["columns"] = ("col1", "col2", "col3", "col4")
tree.column("#0", width=90, minwidth=50, anchor=W)
tree.column("col1", width=200, minwidth=80)
tree.column("col2", width=200, minwidth=80)
tree.column("col3", width=200, minwidth=80)
tree.column("col4", width=200, minwidth=80)
tree.heading("#0", text="ID")
tree.heading("col1", text="Nombre")
tree.heading("col2", text="Apellido")
tree.heading("col3", text="Pasaje")
tree.heading("col4", text="Horario")
tree.grid(row=10, column=0, columnspan=4)

boton_alta = Button(root, text="Nuevo Viaje", command=lambda: alta(a_val, b_val, c_val, d_val, tree))
boton_alta.grid(row=6, column=1)

actualizar_treeview(tree)

root.mainloop()


