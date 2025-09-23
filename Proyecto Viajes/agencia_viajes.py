from tkinter import *
from tkinter.messagebox import *
import sqlite3
from tkinter import ttk
import re

def base_viajes():
    con = sqlite3.connect('viajes3.db')
    return con

def crear_tabla(con):
    cursor = con.cursor()
    sql = """CREATE TABLE IF NOT EXISTS viajes
             (dni varchar(10) PRIMARY KEY,
              nombre_apellido varchar(40) NOT NULL,
              origen varchar(20) NOT NULL,
              numero_pasaje varchar(20),
              horario varchar(5),
              destino varchar(20),
              fecha varchar(20))
    """
    cursor.execute(sql)
    con.commit()
crear_tabla(base_viajes())

def alta(dni, nombre_apellido, origen, numero_pasaje, horario, destino, fecha, tree):
    patron_dni = r"^[0-9]{1,10}$"
    patron_nombre_apellido = r"^[A-Za-záéíóúÁÉÍÓÚñÑ ]{1,40}$"
    patron_origen = r"^[A-Za-záéíóúÁÉÍÓÚñÑ ]{1,20}$"
    patron_numero_pasaje = r"^[A-Za-z0-9]{1,20}$"
    patron_horario = r"^[0-9:]{1,5}$"
    patron_destino = r"^[A-Za-záéíóúÁÉÍÓÚñÑ ]{1,20}$"
    patron_fecha = r"^[0-9/-]{1,20}$"

    if not re.match(patron_dni, dni.get()):
        showerror("Error", "DNI inválido")
        return
    if not re.match(patron_nombre_apellido, nombre_apellido.get()):
        showerror("Error", "Nombre y apellido inválido")
        return
    if not re.match(patron_origen, origen.get()):
        showerror("Error", "Origen inválido")
        return
    if not re.match(patron_numero_pasaje, numero_pasaje.get()):
        showerror("Error", "Número de pasaje inválido")
        return
    if not re.match(patron_horario, horario.get()):
        showerror("Error", "Horario inválido")
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
            "INSERT INTO viajes (dni, nombre_apellido, origen, numero_pasaje, horario, destino, fecha) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (dni.get(), nombre_apellido.get(), origen.get(), numero_pasaje.get(), horario.get(), destino.get(), fecha.get())
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
    dni_borrar = item['values'][0]
    con = base_viajes()
    cursor = con.cursor()
    cursor.execute("DELETE FROM viajes WHERE dni = ?", (dni_borrar,))
    con.commit()
    con.close()
    actualizar_treeview(tree)

def modificar_registro(tree, dni, nombre_apellido, origen, numero_pasaje, horario, destino, fecha):
    selected = tree.selection()
    if not selected:
        showerror("Error", "Seleccione un registro para modificar")
        return

    item_id = selected[0]
    item = tree.item(item_id)

    dni_modificar = item['values'][0]

    con = base_viajes()
    cursor = con.cursor()
    cursor.execute(
        "UPDATE viajes SET nombre_apellido=?, origen=?, numero_pasaje=?, horario=?, destino=?, fecha=? WHERE dni=?",
        (nombre_apellido.get(),
         origen.get(),
         numero_pasaje.get(),
         horario.get(),
         destino.get(),
         fecha.get(),
         dni_modificar)
    )

    if cursor.rowcount == 0:
        showerror("Error", "No se encontró el registro a modificar")
    else:
        con.commit()
        showinfo("Éxito", "Registro actualizado correctamente")

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
        mitreview.insert("", 0, values=fila)

root = Tk()
root.title("Administrar Viajes")

titulo = Label(root, text="Ingrese los datos del viaje", bg="DarkOrchid3", fg="thistle1", height=1, width=60)
titulo.grid(row=0, column=0, columnspan=4, padx=1, pady=1, sticky=W+E)

Label(root, text="DNI").grid(row=1, column=0, sticky=W)
Label(root, text="Nombre y apellido").grid(row=2, column=0, sticky=W)
Label(root, text="Origen").grid(row=3, column=0, sticky=W)
Label(root, text="Número de pasaje").grid(row=4, column=0, sticky=W)
Label(root, text="Horario").grid(row=1, column=2, sticky=W)
Label(root, text="Destino").grid(row=2, column=2, sticky=W)
Label(root, text="Fecha").grid(row=3, column=2, sticky=W)

e_val, a_val, b_val, c_val, d_val, f_val, g_val = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
w_ancho = 20

entrada_dni = Entry(root, textvariable=e_val, width=w_ancho)  # dni
entrada_dni.grid(row=1, column=1)
entrada_nombre = Entry(root, textvariable=a_val, width=w_ancho)  # nombre_apellido
entrada_nombre.grid(row=2, column=1)
entrada_origen = Entry(root, textvariable=b_val, width=w_ancho)  # origen
entrada_origen.grid(row=3, column=1)
entrada_pasaje = Entry(root, textvariable=c_val, width=w_ancho)  # numero_pasaje
entrada_pasaje.grid(row=4, column=1)
entrada_horario = Entry(root, textvariable=d_val, width=w_ancho)  # horario
entrada_horario.grid(row=1, column=3)
entrada_destino = Entry(root, textvariable=f_val, width=w_ancho)  # destino
entrada_destino.grid(row=2, column=3)
entrada_fecha = Entry(root, textvariable=g_val, width=w_ancho)  # fecha
entrada_fecha.grid(row=3, column=3)

tree = ttk.Treeview(root)
tree["columns"] = ("col1", "col2", "col3", "col4", "col5", "col6", "col7")
tree.column("#0", width=0, stretch=NO)
tree.column("col1", width=120, minwidth=80)
tree.column("col2", width=200, minwidth=80)
tree.column("col3", width=200, minwidth=80)
tree.column("col4", width=200, minwidth=80)
tree.column("col5", width=120, minwidth=80)
tree.column("col6", width=200, minwidth=80)
tree.column("col7", width=200, minwidth=80)
tree.heading("col1", text="DNI")
tree.heading("col2", text="Nombre y apellido")
tree.heading("col3", text="Origen")
tree.heading("col4", text="Número de pasaje")
tree.heading("col5", text="Horario")
tree.heading("col6", text="Destino")
tree.heading("col7", text="Fecha")
tree.grid(row=10, column=0, columnspan=4)

boton_alta = Button(root, text="Guardar", command=lambda: alta(e_val, a_val, b_val, c_val, d_val, f_val, g_val, tree))
boton_alta.grid(row=6, column=1)

boton_borrar = Button(root, text="Eliminar", command=lambda: borrar_registro(tree))
boton_borrar.grid(row=6, column=2)

boton_modificar = Button(
    root, text="Modificar",
    command=lambda: modificar_registro(tree, e_val, a_val, b_val, c_val, d_val, f_val, g_val)
)
boton_modificar.grid(row=6, column=3)

actualizar_treeview(tree)
root.mainloop()