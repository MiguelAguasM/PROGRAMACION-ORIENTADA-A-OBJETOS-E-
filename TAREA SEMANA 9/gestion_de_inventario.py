"""
SISTEMA DE GESTIÓN DE INVENTARIO:

Este programa es un sistema básico de inventario.

"""

class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        # Inicialización de atributos con el prefijo _ para indicar que son "protegidos"
        self._id_producto = id_producto
        self._nombre = nombre
        self._cantidad = cantidad
        self._precio = precio

    # Getters: Permiten obtener el valor de los atributos de forma segura
    def get_id(self):
        return self._id_producto

    def get_nombre(self):
        return self._nombre

    def get_cantidad(self):
        return self._cantidad

    def get_precio(self):
        return self._precio

    # Setters: Permiten modificar los atributos
    def set_id(self, id_producto):
        self._id_producto = id_producto

    def set_nombre(self, nombre):
        self._nombre = nombre

    def set_cantidad(self, cantidad):
        self._cantidad = cantidad

    def set_precio(self, precio):
        self._precio = precio

    def __str__(self):
        # Representación en cadena del objeto para facilitar su visualización
        return f"ID: {self._id_producto} | Nombre: {self._nombre} | Cantidad: {self._cantidad} | Precio: ${self._precio:.2f}"


class Inventario:
    def __init__(self):
        self.productos = []

    def añadir_producto(self, producto):
        # Verifica si el ID ya existe para que no se repitan los datos
        if any(p.get_id() == producto.get_id() for p in self.productos):
            print(f"Error: Ya existe un producto con el ID {producto.get_id()}.")
            return False
        self.productos.append(producto)
        print("Producto añadido exitosamente.")
        return True

    def eliminar_producto_por_id(self, id_producto):
        # Busca el índice del producto para eliminarlo de la lista
        for i, producto in enumerate(self.productos):
            if producto.get_id() == id_producto:
                del self.productos[i]
                print(f"Producto con ID {id_producto} eliminado.")
                return True
        print(f"Error: No se encontró el producto con ID {id_producto}.")
        return False

    def actualizar_producto(self, id_producto, cantidad=None, precio=None):
        # Permite actualizar el producto, cantidad, precio o ambos
        for producto in self.productos:
            if producto.get_id() == id_producto:
                if cantidad is not None:
                    producto.set_cantidad(cantidad)
                if precio is not None:
                    producto.set_precio(precio)
                print(f"Producto con ID {id_producto} actualizado.")
                return True
        print(f"Error: No se encontró el producto con ID {id_producto}.")
        return False

    def buscar_por_nombre(self, nombre):
        # Búsqueda que ignora mayúsculas y minúsculas
        resultados = [p for p in self.productos if nombre.lower() in p.get_nombre().lower()]
        if resultados:
            print(f"\nResultados de búsqueda para '{nombre}':")
            for p in resultados:
                print(p)
        else:
            print(f"No se encontraron productos que coincidan con '{nombre}'.")

    def mostrar_inventario(self):
        # Lista todos los productos o informa si el inventario está vacío
        if not self.productos:
            print("\nEl inventario está vacío.")
        else:
            print("\nInventario Completo:\n")
            for producto in self.productos:
                print(producto)


def mostrar_menu():
    # Presentación simple del menú por consola
    print("\nSISTEMA DE GESTIÓN DE INVENTARIO\n")
    print("1. Añadir nuevo producto")
    print("2. Eliminar producto por ID")
    print("3. Actualizar cantidad o precio")
    print("4. Buscar producto por nombre")
    print("5. Mostrar todos los productos")
    print("6. Salir\n")

def ejecutar():
    # Lógica principal de ejecución del programa
    inventario = Inventario()
    
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            try:
                # Captura y validación de datos para nuevo producto
                id_p = input("Ingrese ID del producto: ")
                nombre = input("Ingrese nombre del producto: ")
                cantidad = int(input("Ingrese cantidad: "))
                precio = float(input("Ingrese precio: "))
                nuevo_p = Producto(id_p, nombre, cantidad, precio)
                inventario.añadir_producto(nuevo_p)
            except ValueError:
                # Maneja errores cuando se ingresan letras en campos numéricos
                print("Error: Cantidad debe ser entero y Precio debe ser numérico.")

        elif opcion == "2":
            id_p = input("Ingrese el ID del producto a eliminar: ")
            inventario.eliminar_producto_por_id(id_p)

        elif opcion == "3":
            # Permite al usuario presionar ENTER para omitir un campo
            id_p = input("Ingrese el ID del producto a actualizar: ")
            print("Deje en blanco si no desea cambiar el valor.")
            cantidad_str = input("Nueva cantidad: ")
            precio_str = input("Nuevo precio: ")
            
            try:
                cantidad = int(cantidad_str) if cantidad_str.strip() else None
                precio = float(precio_str) if precio_str.strip() else None
                inventario.actualizar_producto(id_p, cantidad, precio)
            except ValueError:
                print("Error: Los valores de actualización deben ser numéricos.")

        elif opcion == "4":
            nombre = input("Ingrese el nombre o parte del nombre a buscar: ")
            inventario.buscar_por_nombre(nombre)

        elif opcion == "5":
            inventario.mostrar_inventario()

        elif opcion == "6":
            print("\nSaliendo del sistema...\n")
            break
        else:
            print("\nOpción no válida, intente de nuevo.")


if __name__ == "__main__":
    # Inicia la aplicación
    ejecutar()
