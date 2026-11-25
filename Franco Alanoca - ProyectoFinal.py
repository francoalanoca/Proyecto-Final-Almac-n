# ==================================================
# Franco Alanoca - Proyecto Final
# ==================================================
import dataset

#Conectamos con la base de datos
miBase = dataset.connect("sqlite:///inventario.db")

# Creamos la tabla con los campos solicitados.
# Evita crearla nuevamente si ya existe.
miBase.query("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        cantidad INTEGER NOT NULL,
        precio REAL NOT NULL,
        categoria TEXT
    )
""")

tabla = miBase["productos"]

# ==================================================
#FUNCIONES DE VALIDACION
#Logica para ingresar un numero entero
def ingresar_entero(mensaje):

    while True:

        #Validamos la veracidad del dato ingresado
        try:
            numero = int(input(mensaje))

            if numero >= 0:
                return numero
            else:
                print("Error: ingresá un número mayor o igual a cero.")

        except ValueError:
            print("Error: ingresá un número entero válido.")


#Logica para ingresar un numero real
def ingresar_real(mensaje):

    while True:

        #Validamos la veracidad del dato ingresado
        try:
            numero = float(input(mensaje))

            if numero >= 0:
                return numero
            else:
                print("Error: el precio no puede ser negativo.")

        except ValueError:
            print("Error: ingresá un precio válido.")


#Logica para ingresar texto
def ingresar_texto(mensaje):

    texto = input(mensaje).strip()

    #Validamos que no sea un campo vacio
    while texto == "":
        print("Error: el campo no puede estar vacío.")
        texto = input(mensaje).strip()

    return texto
# ==================================================



# OPCION 1 - REGISTRAR
def registrar_producto():

    print("\n--- REGISTRAR PRODUCTO ---")
    nombre = ingresar_texto("Nombre: ")
    descripcion = input("Descripción: ").strip()
    cantidad = ingresar_entero("Cantidad: ")
    precio = ingresar_real("Precio: ")
    categoria = input("Categoría: ").strip()

    #Agregamos los registros a la tabla
    tabla.insert({
        "nombre": nombre,
        "descripcion": descripcion,
        "cantidad": cantidad,
        "precio": precio,
        "categoria": categoria
    })

    print("Producto registrado correctamente.")



# OPCION 2 - MOSTRAR
def mostrar_productos():

    print("\n--- LISTADO DE PRODUCTOS ---")
    encontro = False

    #Buscamos y mostramos todos los productos registrados
    for producto in tabla.find(order_by="id"):
        print("\nID:", producto["id"])
        print("Nombre:", producto["nombre"])
        print("Descripción:", producto["descripcion"])
        print("Cantidad:", producto["cantidad"])
        print("Precio: $", producto["precio"])
        print("Categoría:", producto["categoria"])
        print("---------------------------")

        encontro = True

    #Si no hay ninguno
    if not encontro:
        print("No hay productos registrados.")



# OPCION 3 - BUSCAR POR ID
def buscar_producto():

    print("\n--- BUSCAR PRODUCTO ---")
    #Pedimos el id del producto
    id_producto = ingresar_entero("Ingresá el ID: ")
    #Buscamos el producto y asignamos en variable
    producto = tabla.find_one(id=id_producto)

    if producto:
        print("\nProducto encontrado:")
        print("ID:", producto["id"])
        print("Nombre:", producto["nombre"])
        print("Descripción:", producto["descripcion"])
        print("Cantidad:", producto["cantidad"])
        print("Precio: $", producto["precio"])
        print("Categoría:", producto["categoria"])

    else:
        print("No se encontró un producto con ese ID.")



# OPCION 4 - BUSCAR POR NOMBRE O CATEGORIA (OPCIONAL)
def buscar_por_nombre_categoria():

    print("\n--- BUSQUEDA POR NOMBRE O CATEGORIA ---")
    texto = ingresar_texto("Ingresá el nombre o categoría: ")

    #Buscamos coincidencias parciales en ambos campos.
    por_nombre = tabla.find(nombre={"ilike": "%" + texto + "%"})
    por_categoria = tabla.find(categoria={"ilike": "%" + texto + "%"})

    resultados = {}

    for producto in por_nombre:
        resultados[producto["id"]] = producto

    for producto in por_categoria:
        resultados[producto["id"]] = producto

    if len(resultados) == 0:
        print("No se encontraron coincidencias.")
    else:
        for producto in resultados.values():
            print("\nID:", producto["id"])
            print("Nombre:", producto["nombre"])
            print("Categoría:", producto["categoria"])
            print("Cantidad:", producto["cantidad"])
            print("Precio: $", producto["precio"])



# OPCION 5 - ACTUALIZAR
def actualizar_producto():

    print("\n--- ACTUALIZAR PRODUCTO ---")
    #Pedimos el id del producto
    id_producto = ingresar_entero("Ingresá el ID: ")
    #Buscamos el producto y asignamos en variable
    producto = tabla.find_one(id=id_producto)

    if producto:
        print("\nProducto actual:", producto["nombre"])
        print("Ingresá los nuevos datos.")

        nombre = ingresar_texto("Nombre: ")
        descripcion = input("Descripción: ").strip()
        cantidad = ingresar_entero("Cantidad: ")
        precio = ingresar_real("Precio: ")
        categoria = input("Categoría: ").strip()

        #Actualizamos los registros de la tabla
        tabla.update({
            "id": id_producto,
            "nombre": nombre,
            "descripcion": descripcion,
            "cantidad": cantidad,
            "precio": precio,
            "categoria": categoria
        }, keys=["id"])

        print("Producto actualizado correctamente.")

    else:
        print("No se encontró un producto con ese ID.")



# OPCION 6 - ELIMINAR
def eliminar_producto():

    print("\n--- ELIMINAR PRODUCTO ---")
    #Pedimos el id del producto
    id_producto = ingresar_entero("Ingresá el ID: ")
    #Buscamos el producto y asignamos en variable
    producto = tabla.find_one(id=id_producto)

    if producto:
        print("Producto:", producto["nombre"])

        confirmacion = input(
            "¿Desea eliminar este producto? (s/n): "
        ).strip().lower()

        if confirmacion == "s":
            tabla.delete(id=id_producto)
            print("Producto eliminado correctamente.")
        else:
            print("Eliminación cancelada.")

    else:
        print("No se encontró un producto con ese ID.")



# OPCION 7 - REPORTE DE STOCK
def reporte_stock():

    print("\n--- REPORTE DE STOCK ---")
    limite = ingresar_entero("Ingresá el límite de stock: ")
    #Buscamos la cabtidad de todos los productos registrados
    productos = tabla.find(cantidad={"lte": limite}, order_by="cantidad")
    encontro = False

    for producto in productos:
        print("\nID:", producto["id"])
        print("Nombre:", producto["nombre"])
        print("Cantidad disponible:", producto["cantidad"])
        print("Precio: $", producto["precio"])

        encontro = True

    if not encontro:
        print("No hay productos que cumplan con ese límite.")



# MENU PRINCIPAL
while True:

    #Interfaz del menu interactivo
    print("\n===================================")
    print("       SISTEMA DE INVENTARIO")
    print("===================================")
    print("1 - Registrar producto")
    print("2 - Mostrar productos")
    print("3 - Buscar producto por ID")
    print("4 - Buscar por nombre o categoría")
    print("5 - Actualizar producto")
    print("6 - Eliminar producto")
    print("7 - Reporte de stock")
    print("8 - Salir")
    print("===================================")

    opcion = input("Seleccioná una opción: ").strip()


    #Logica del interfaz
    match opcion:

        case "1":
            registrar_producto()

        case "2":
            mostrar_productos()

        case "3":
            buscar_producto()

        case "4":
            buscar_por_nombre_categoria()

        case "5":
            actualizar_producto()

        case "6":
            eliminar_producto()

        case "7":
            reporte_stock()

        case "8":
            print("Saliendo del sistema...")
            break

        case _:
            print("Opción incorrecta. Intentá nuevamente.")


#Cerramos la conexión con la base de datos.
miBase.close()

print("Programa finalizado.")
