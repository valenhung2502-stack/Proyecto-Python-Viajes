from tkinter import *
from tkinter.messagebox import *
import sqlite3
from tkinter import ttk
import re

def base_viajes():
    con = sqlite3.connect('pasajes.db')
    return con

def crear_tabla(con):
    cursor = con.cursor()
    sql = """CREATE TABLE IF NOT EXISTS viajes
             (dni varchar(10) PRIMARY KEY,
             nombre varchar(20) NOT NULL,
             apellido varchar(20) NOT NULL,
             pasaje varchar(20),
             horario varchar(5),
             destino varchar(20),
             fecha varchar(20))
    """
    cursor.execute(sql)
    con.commit()
crear_tabla(base_viajes())

def alta(nombre, apellido, pasaje, horario, dni, destino, fecha, tree):

    patron_nombre = r"^[A-Za-záéíóúÁÉÍÓÚñÑ ]{1,20}$"
    patron_apellido = r"^[A-Za-záéíóúÁÉÍÓÚñÑ ]{1,20}$"
    patron_pasaje = r"^[A-Za-z0-9]{1,20}$"
    patron_horario = r"^[0-9:]{1,5}$"
    patron_dni = r"^[0-9 ]{1,10}$"
    patron_destino = r"^[A-Za-záéíóúÁÉÍÓÚñÑ ]{1,20}$"
    patron_fecha = r"^[0-9/-]{1,20}$"
   
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
    if not re.match(patron_dni, dni.get()):
        showerror("Error", "DNI inválido")
        return
    if not re.match(patron_destino, destino.get()):
        showerror("Error", "Destino inválido")
        return
    if not re.match(patron_fecha, fecha.get()):
        showerror("Error", "Fecha inválida")
        return

    con = base_viajes()
    cursor = con.cursor()
    try:
        cursor.execute(
            "INSERT INTO viajes (dni, nombre, apellido, pasaje, horario, destino, fecha) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (dni.get(), nombre.get(), apellido.get(), pasaje.get(), horario.get(), destino.get(), fecha.get())
        )
        con.commit()
    except sqlite3.IntegrityError:
        showerror("Error", "El DNI ya existe")
    con.close()
    actualizar_treeview(tree)

def borrar_registro(tree):
    selected = tree.selection()
    if not selected:
        showerror("Error", "Seleccione un registro para eliminar")
        return
    item = tree.item(selected)
    dni_borrar = item['text']
    con = base_viajes()
    cursor = con.cursor()
    cursor.execute("DELETE FROM viajes WHERE dni = ?", (dni_borrar,))
    con.commit()
    con.close()
    actualizar_treeview(tree)

def modificar_registro(tree, nombre, apellido, pasaje, horario, dni, destino, fecha):
    selected = tree.selection()
    if not selected:
        showerror("Error", "Seleccione un registro para modificar")
        return
    item = tree.item(selected)
    dni_modificar = item['text']
    con = base_viajes()
    cursor = con.cursor()
    cursor.execute(
        "UPDATE viajes SET nombre=?, apellido=?, pasaje=?, horario=?, destino=?, fecha=? WHERE dni=?",
        (nombre.get(), apellido.get(), pasaje.get(), horario.get(), destino.get(), fecha.get(), dni_modificar)
    )
    con.commit()
    con.close()
    actualizar_treeview(tree)


def actualizar_treeview(mitreview):
    records = mitreview.get_children()
    for element in records:
        mitreview.delete(element)
    sql = "SELECT * FROM viajes ORDER BY dni ASC"
    con = base_viajes()
    cursor = con.cursor()
    datos = cursor.execute(sql)
    resultado = datos.fetchall()
    for fila in resultado:
        mitreview.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3], fila[4], fila[5], fila[6]))

root = Tk()
root.title("Administrar Viajes")

titulo = Label(root, text="Ingrese los datos del viaje", bg="DarkOrchid3", fg="thistle1", height=1, width=60)
titulo.grid(row=0, column=0, columnspan=4, padx=1, pady=1, sticky=W+E)

Label(root, text="Nombre").grid(row=1, column=0, sticky=W)
Label(root, text="Apellido").grid(row=2, column=0, sticky=W)
Label(root, text="Pasaje").grid(row=3, column=0, sticky=W)
Label(root, text="Horario").grid(row=4, column=0, sticky=W)
Label(root, text="DNI").grid(row=5, column=0, sticky=W)
Label(root, text="Destino").grid(row=1, column=2, sticky=W)
Label(root, text="Fecha").grid(row=2, column=2, sticky=W)

a_val, b_val, c_val, d_val, e_val, f_val, g_val = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
w_ancho = 20

entrada1 = Entry(root, textvariable=a_val, width=w_ancho)
entrada1.grid(row=1, column=1)
entrada2 = Entry(root, textvariable=b_val, width=w_ancho)
entrada2.grid(row=2, column=1)
entrada3 = Entry(root, textvariable=c_val, width=w_ancho)
entrada3.grid(row=3, column=1)
entrada4 = Entry(root, textvariable=d_val, width=w_ancho)
entrada4.grid(row=4, column=1)
entrada5 = Entry(root, textvariable=e_val, width=w_ancho)
entrada5.grid(row=5, column=1)
entrada6 = Entry(root, textvariable=f_val, width=w_ancho)
entrada6.grid(row=1, column=3)
entrada7 = Entry(root, textvariable=g_val, width=w_ancho)
entrada7.grid(row=2, column=3)

tree = ttk.Treeview(root)
tree["columns"] = ("col1", "col2", "col3", "col4", "col5", "col6")
tree.column("#0", width=90, minwidth=50, anchor=W)
tree.column("col1", width=200, minwidth=80)
tree.column("col2", width=200, minwidth=80)
tree.column("col3", width=200, minwidth=80)
tree.column("col4", width=200, minwidth=80)
tree.column("col5", width=200, minwidth=80)
tree.column("col6", width=200, minwidth=80)
tree.heading("#0", text="DNI")
tree.heading("col1", text="Nombre")
tree.heading("col2", text="Apellido")
tree.heading("col3", text="Pasaje")
tree.heading("col4", text="Horario")
tree.heading("col5", text="Destino")
tree.heading("col6", text="Fecha")
tree.grid(row=10, column=0, columnspan=4)


boton_alta = Button(root, text="Guardar", command=lambda: alta(a_val, b_val, c_val, d_val, e_val, f_val, g_val, tree))
boton_alta.grid(row=6, column=1)

boton_borrar = Button(root, text="Eliminar", command=lambda: borrar_registro(tree))
boton_borrar.grid(row=6, column=2)

boton_modificar = Button(
    root, text="Modificar",
    command=lambda: modificar_registro(tree, a_val, b_val, c_val, d_val, e_val, f_val, g_val)
)
boton_modificar.grid(row=6, column=3)

actualizar_treeview(tree)
root.mainloop()