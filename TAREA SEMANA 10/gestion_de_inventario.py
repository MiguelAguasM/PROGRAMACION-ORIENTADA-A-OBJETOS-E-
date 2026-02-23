"""
SISTEMA DE GESTIÓN DE INVENTARIO MEJORADO: TAREA SEMANA 10 - Alumno: Miguel Aguas

Este programa es un sistema de inventario el cual permite:
El almacenamiento de Inventarios en Archivos:
Se modificó la clase Inventario añadir, actualizar, o eliminar productos, estas modificaciones se reflejen en el archivo inventario.txt

La recuperación de Inventarios desde Archivos:
Al iniciar el programa, carga automáticamente los productos existentes en inventario.txt para reconstruir el inventario.

Manejo de Excepciones:
Se implementó el manejo de excepciones para capturar y tratar adecuadamente posibles errores durante la manipulación de archivos, como FileNotFoundError y PermissionError.
El programa maneja casos en los que el archivo de inventario no existe, y lo crea si es necesario.

Modificaciones a la Interfaz de Usuario en la Consola:
Se actualizó la interfaz de usuario para notificar al usuario sobre el éxito o fallo de operaciones de archivo (por ejemplo, notificar al usuario cuando un producto se añade exitosamente al archivo de inventario).
"""

import os

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

    def a_linea_texto(self):
        # Implementé este método para facilitar la escritura del producto en el archivo de texto
        return f"{self._id_producto},{self._nombre},{self._cantidad},{self._precio}\n"


class Inventario:
    def __init__(self, archivo="inventario.txt"):
        # Inicialicé el inventario con un nombre de archivo para la persistencia
        self.productos = []
        self.archivo = archivo
        # Llamé a la función de carga automática al instanciar la clase
        self.cargar_desde_archivo()

    def guardar_en_archivo(self):
        # Implementé este método para volcar toda la lista de productos al archivo de texto
        try:
            with open(self.archivo, "w") as f:
                for producto in self.productos:
                    f.write(producto.a_linea_texto())
            print(f"Cambios guardados exitosamente en {self.archivo}.")
        except PermissionError:
            # Agregué captura de error por falta de permisos de escritura
            print(f"Error: No tiene permisos para escribir en el archivo {self.archivo}.")
        except Exception as e:
            # Manejé cualquier otra excepción inesperada durante la escritura
            print(f"Ocurrió un error inesperado al guardar: {e}")

    def cargar_desde_archivo(self):
        # Implementé la carga automática de productos desde el archivo al iniciar
        if not os.path.exists(self.archivo):
            # Si el archivo no existe, lo creé vacío y notifiqué al usuario
            try:
                with open(self.archivo, "w") as f:
                    pass
                print(f"Archivo {self.archivo} no existía, fue creado.")
            except Exception as e:
                print(f"No se pudo crear el archivo inicial: {e}")
            return

        try:
            with open(self.archivo, "r") as f:
                for linea in f:
                    # Limpié y separé los datos de cada línea
                    datos = linea.strip().split(",")
                    if len(datos) == 4:
                        id_p, nombre, cantidad, precio = datos
                        # Reconstruí el objeto Producto y lo agregué a la lista
                        self.productos.append(Producto(id_p, nombre, int(cantidad), float(precio)))
            print(f"\nCargué correctamente {len(self.productos)} productos desde {self.archivo}.")
        except FileNotFoundError:
            # Aunque verifiqué existencia con os.path, manejé FileNotFoundError por seguridad
            print(f"El archivo {self.archivo} no pudo ser encontrado.")
        except ValueError:
            # Manejé excepciones para casos de datos corruptos o mal formateados en el archivo
            print(f"Error: El archivo {self.archivo} contiene datos corruptos o con formato inválido.")
        except Exception as e:
            print(f"Error inesperado al cargar el archivo: {e}")

    def añadir_producto(self, producto):
        # Verifica si el ID ya existe para que no se repitan los datos
        if any(p.get_id() == producto.get_id() for p in self.productos):
            print(f"Error: Ya existe un producto con el ID {producto.get_id()}.")
            return False
        self.productos.append(producto)
        # Agregué la llamada para guardar los cambios en el archivo tras añadir
        self.guardar_en_archivo()
        print("Producto añadido exitosamente.")
        return True

    def eliminar_producto_por_id(self, id_producto):
        # Busca el índice del producto para eliminarlo de la lista
        for i, producto in enumerate(self.productos):
            if producto.get_id() == id_producto:
                del self.productos[i]
                # Agregué la llamada para actualizar el archivo tras eliminar
                self.guardar_en_archivo()
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
                # Agregué la llamada para reflejar la actualización en el archivo
                self.guardar_en_archivo()
                print(f"Producto con ID {id_producto} actualizado.")
                return True
        print(f"Error: No se encontró el producto con ID {id_producto}.")
        return False

    def buscar_por_nombre(self, nombre):
        # Búsqueda que ignora mayúsculas y minúsculas
        resultados = [p for p in self.productos if nombre.lower() in p.get_nombre().lower()]
        if resultados:
            print(f"\nResultados de búsqueda para '{nombre}':\n")
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
    print("\nSISTEMA DE GESTIÓN DE INVENTARIO MEJORADO\n")
    print("1. Añadir nuevo producto")
    print("2. Eliminar producto por ID")
    print("3. Actualizar cantidad o precio")
    print("4. Buscar producto por nombre")
    print("5. Mostrar todos los productos")
    print("6. Salir\n")

def ejecutar():
    # Lógica principal de ejecución del programa
    # Instancié el inventario; ahora cargará automáticamente el archivo
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
