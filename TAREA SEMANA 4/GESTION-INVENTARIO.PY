#PROGRAMA DE GESTION DE INVENTARIO - ESTUDIANTE: MIGUEL ANGEL AGUAS

class Producto:
    """Clase para el producto del inventario, tambien tiene los datos básicos del producto."""

    def __init__(self, codigo, nombre, precio, cantidad):
        self.codigo = codigo #atributos del producto
        self.nombre = nombre #atributos del producto
        self.precio = precio #atributos del producto
        self.cantidad = cantidad #atributos del producto

    def mostrar_info(self):
        """Muestra en pantalla la información completa del producto."""
        print(f"Código: {self.codigo} | Nombre: {self.nombre} | Precio: ${self.precio} | Cantidad: {self.cantidad}")

class Inventario:
    """Clase que gestiona el inventario de productos"""
    def __init__(self):
        self.productos = []

    def agregar_producto(self, producto):
        """Agrega un objeto de tipo Producto a la lista del inventario"""
        self.productos.append(producto)
        print("\nProducto agregado.")

    def mostrar_productos(self):
        """Recorre la lista de productos y muestra la información de cada uno, si no existen productos agregados muestra un mensaje indicando que el inventario está vacío."""
        if not self.productos:
            print("No hay productos ingresados.")
        else:
            print("\nLISTA DE PRODUCTOS:\n")
            for producto in self.productos:
                producto.mostrar_info()

def menu():
    """Función que muestra el menú principal del programa de gestion de inventario."""
    print("\nMENÚ DE INVENTARIO:\n")
    print("1. Agregar producto")
    print("2. Mostrar productos")
    print("3. Salir")

#Se crea un objeto de la clase Inventario para gestionar los productos.
inventario = Inventario()

#Ciclo principal del programa que se ejecuta hasta que el usuario escoja la opción de salir
while True:
    menu()
    opcion = input("\nSeleccione una opción:")

    if opcion == "1":
        #Pide los datos del producto al usuario
        codigo = input("\nIngrese el código del producto: ")
        nombre = input("Ingrese el nombre del producto: ")
        precio = float(input("Ingrese el precio del producto: "))
        cantidad = int(input("Ingrese la cantidad del producto: "))

        #Crea un objeto Producto y se agrega al inventario
        nuevo_producto = Producto(codigo, nombre, precio, cantidad)
        inventario.agregar_producto(nuevo_producto)

    elif opcion == "2":
        #Muestra todos los productos ingresados en el inventario
        inventario.mostrar_productos()

    elif opcion == "3":
        #Finaliza o cierra el programa
        print("Cerrando el programa.")
        break

    else:
        #Se muestra cuando el usuario digita opciones incorrectas
        print("Opción no válida, por favor intente nuevamente.")