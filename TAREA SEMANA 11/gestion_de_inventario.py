"""
SISTEMA DE GESTIÓN DE INVENTARIO TIENDA UEA: TAREA SEMANA 11 - Alumno: Miguel Aguas
Uso de Diccionarios (Requisito 2):

USO DE DICCIONARIOS:
Se cambió self.productos = [] (lista) por self.productos = {} (diccionario).
Ahora el ID del producto es la clave lo que permite que la eliminación y actualización de productos sean rápidas.
Se optimizó añadir_producto para verificar la existencia del ID del producto en el diccionario.

Integración de más Colecciones:
Tuplas: He implementado el uso de tuplas en el método  cargar_desde_archivo para desempaquetar 
los datos del archivo inventario.txt de forma segura antes de crear los productos.
Conjuntos (sets): He añadido self.nombres_registrados = set(). Esta colección permite un seguimiento 
rápido de los nombres de los productos para futuras validaciones.
Listas: Para el método buscar_por_nombre.

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
        # Se utiliza un DICCIONARIO para almacenar los productos.
        # La clave es el ID del producto, lo que permite búsquedas rápidas.
        self.productos = {}
        self.archivo = archivo
        # Se utiliza un CONJUNTO para mantener un registro rápido de nombres únicos.
        self.nombres_registrados = set()
        self.cargar_desde_archivo()

    def guardar_en_archivo(self):
        try:
            with open(self.archivo, "w") as f:
                # Iteracion sobre los valores del diccionario
                for producto in self.productos.values():
                    f.write(producto.a_linea_texto())
            print(f"Cambios guardados exitosamente en {self.archivo}.")
        except PermissionError:
            print(f"Error: No tiene permisos para escribir en el archivo {self.archivo}.")
        except Exception as e:
            print(f"Ocurrió un error inesperado al guardar: {e}")

    def cargar_desde_archivo(self):
        if not os.path.exists(self.archivo):
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
                    datos = linea.strip().split(",")
                    if len(datos) == 4:
                        # Uso de TUPLAS para el desempaquetado de datos
                        datos_tupla = tuple(datos)
                        id_p, nombre, cantidad, precio = datos_tupla
                        
                        nuevo_p = Producto(id_p, nombre, int(cantidad), float(precio))
                        # Almacenamiento en el DICCIONARIO usando ID como clave
                        self.productos[id_p] = nuevo_p
                        self.nombres_registrados.add(nombre.lower())
            
            print(f"\nCargué correctamente {len(self.productos)} productos desde {self.archivo}.")
        except FileNotFoundError:
            print(f"El archivo {self.archivo} no pudo ser encontrado.")
        except ValueError:
            print(f"Error: El archivo {self.archivo} contiene datos corruptos.")
        except Exception as e:
            print(f"Error inesperado al cargar el archivo: {e}")

    def añadir_producto(self, producto):
        # Búsqueda optimizada: Verificamos si la clave existe en el DICCIONARIO
        if producto.get_id() in self.productos:
            print(f"Error: Ya existe un producto con el ID {producto.get_id()}.")
            return False
        
        # Inserción directa en el diccionario
        self.productos[producto.get_id()] = producto
        self.nombres_registrados.add(producto.get_nombre().lower())
        self.guardar_en_archivo()
        print("Producto añadido exitosamente.")
        return True

    def eliminar_producto_por_id(self, id_producto):
        # Eliminación optimizada usando la clave del DICCIONARIO
        if id_producto in self.productos:
            producto = self.productos.pop(id_producto)
            self.nombres_registrados.discard(producto.get_nombre().lower())
            self.guardar_en_archivo()
            print(f"Producto con ID {id_producto} eliminado.")
            return True
        print(f"Error: No se encontró el producto con ID {id_producto}.")
        return False

    def actualizar_producto(self, id_producto, cantidad=None, precio=None):
        # Acceso directo al producto por su ID en el DICCIONARIO
        if id_producto in self.productos:
            producto = self.productos[id_producto]
            if cantidad is not None:
                producto.set_cantidad(cantidad)
            if precio is not None:
                producto.set_precio(precio)
            self.guardar_en_archivo()
            print(f"Producto con ID {id_producto} actualizado.")
            return True
        print(f"Error: No se encontró el producto con ID {id_producto}.")
        return False

    def buscar_por_nombre(self, nombre):
        # Para búsqueda parcial se sigue iterando sobre los valores del diccionario
        resultados = [p for p in self.productos.values() if nombre.lower() in p.get_nombre().lower()]
        if resultados:
            print(f"\nResultados de búsqueda para '{nombre}':\n")
            for p in resultados:
                print(p)
        else:
            print(f"No se encontraron productos que coincidan con '{nombre}'.")

    def mostrar_inventario(self):
        if not self.productos:
            print("\nEl inventario está vacío.")
        else:
            print("\nInventario Total de la Tienda UEA:\n")
            # Iteración sobre los valores del diccionario
            for producto in self.productos.values():
                print(producto)


def mostrar_menu():
    # Menú que se muestra en la consola
    print("\nSISTEMA DE GESTIÓN DE INVENTARIO - TIENDA UEA\n")
    print("1. Añadir nuevo producto")
    print("2. Eliminar producto por ID")
    print("3. Actualizar cantidad o precio de un producto")
    print("4. Buscar y mostrar productos por nombre")
    print("5. Mostrar todos los productos del inventario")
    print("6. Salir\n")

def ejecutar():
    # Lógica principal de ejecución del programa
    # El inventario se carga automáticamente al iniciar el programa
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
