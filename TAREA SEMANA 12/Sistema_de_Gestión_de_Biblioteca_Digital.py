#Tarea semana 12:
#Sistema para gestionar una biblioteca digital. El sistema permite administrar los libros 
#disponibles, las categorías de libros, los usuarios registrados y el historial de préstamos.

import os

class Libro:
    """Representa un libro en la biblioteca."""
    def __init__(self, titulo, autor, categoria, isbn):
        # Utilizamos una tupla para título y autor ya que son inmutables
        self.info = (titulo, autor)
        self.categoria = categoria
        self.isbn = isbn

    @property
    def titulo(self):
        return self.info[0]

    @property
    def autor(self):
        return self.info[1]

    def __str__(self):
        return f"Libro: {self.titulo} | Autor: {self.autor} | Categoría: {self.categoria} | ISBN: {self.isbn}"

    def a_linea_texto(self):
        """Convierte el libro a una línea de texto para el archivo."""
        return f"{self.titulo},{self.autor},{self.categoria},{self.isbn}\n"

    @staticmethod
    def desde_linea_texto(linea):
        """Crea un objeto Libro desde una línea de texto del archivo."""
        datos = linea.strip().split(',')
        if len(datos) == 4:
            return Libro(datos[0], datos[1], datos[2], datos[3])
        return None


class Usuario:
    """Representa a un usuario de la biblioteca."""
    def __init__(self, nombre, user_id):
        self.nombre = nombre
        self.user_id = user_id
        # Lista para gestionar los libros actualmente prestados
        self.libros_prestados = []

    def __str__(self):
        resumen_libros = ", ".join([l.titulo for l in self.libros_prestados]) if self.libros_prestados else "Ninguno"
        return f"Usuario: {self.nombre} (ID: {self.user_id}) | Prestados: {resumen_libros}"
    
    def a_linea_texto(self):
        """Convierte el usuario a una línea de texto."""
        return f"{self.nombre},{self.user_id}\n"


class Biblioteca:
    """Gestiona la colección de libros, usuarios y préstamos."""
    def __init__(self, archivo_libros="libros.txt", archivo_usuarios="usuarios.txt", archivo_prestamos="prestamos.txt"):
        self.archivo_libros = archivo_libros
        self.archivo_usuarios = archivo_usuarios
        self.archivo_prestamos = archivo_prestamos
        
        # Diccionario maestro con TODOS los libros del sistema {isbn: objeto Libro}
        self.catalogo_completo = {}
        # Diccionario de libros que están en estantería (disponibles)
        self.libros_disponibles = {}
        # Diccionario de usuarios {user_id: objeto Usuario}
        self.usuarios = {}
        # Conjunto para asegurar IDs de usuario únicos
        self.usuarios_ids = set()
        
        # Cargar todos los datos al iniciar
        self.cargar_datos()

    def guardar_datos(self):
        """Guarda toda la información en los archivos correspondientes."""
        try:
            # 1. Guardar todos los libros (Catálogo maestro)
            with open(self.archivo_libros, 'w', encoding='utf-8') as f:
                for libro in self.catalogo_completo.values():
                    f.write(libro.a_linea_texto())
            
            # 2. Guardar todos los usuarios
            with open(self.archivo_usuarios, 'w', encoding='utf-8') as f:
                for usuario in self.usuarios.values():
                    f.write(usuario.a_linea_texto())
            
            # 3. Guardar el estado de los préstamos
            with open(self.archivo_prestamos, 'w', encoding='utf-8') as f:
                for user_id, usuario in self.usuarios.items():
                    for libro in usuario.libros_prestados:
                        f.write(f"{user_id},{libro.isbn}\n")
                        
        except Exception as e:
            print(f"Error al guardar datos: {e}")

    def cargar_datos(self):
        """Reconstruye el estado del sistema desde los archivos TXT."""
        # A. Cargar catálogo completo
        if os.path.exists(self.archivo_libros):
            try:
                with open(self.archivo_libros, 'r', encoding='utf-8') as f:
                    for linea in f:
                        if linea.strip():
                            libro = Libro.desde_linea_texto(linea)
                            if libro:
                                self.catalogo_completo[libro.isbn] = libro
                                # Inicialmente asumimos todos como disponibles
                                self.libros_disponibles[libro.isbn] = libro
            except Exception as e:
                print(f"Error al cargar libros: {e}")

        # B. Cargar usuarios
        if os.path.exists(self.archivo_usuarios):
            try:
                with open(self.archivo_usuarios, 'r', encoding='utf-8') as f:
                    for linea in f:
                        if not linea.strip(): continue
                        datos = [d.strip() for d in linea.split(',')]
                        # Filtramos elementos vacíos por si hay comas al final
                        datos = [d for d in datos if d]
                        if len(datos) >= 2:
                            nombre, user_id = datos[0], datos[1]
                            usuario = Usuario(nombre, user_id)
                            self.usuarios[user_id] = usuario
                            self.usuarios_ids.add(user_id)
            except Exception as e:
                print(f"Error al cargar usuarios: {e}")

        # C. Cargar préstamos
        if os.path.exists(self.archivo_prestamos):
            try:
                with open(self.archivo_prestamos, 'r', encoding='utf-8') as f:
                    for linea in f:
                        if not linea.strip(): continue
                        datos = [d.strip() for d in linea.split(',')]
                        if len(datos) >= 2:
                            u_id, l_isbn = datos[0], datos[1]
                            if u_id in self.usuarios and l_isbn in self.catalogo_completo:
                                libro = self.catalogo_completo[l_isbn]
                                self.usuarios[u_id].libros_prestados.append(libro)
                                if l_isbn in self.libros_disponibles:
                                    del self.libros_disponibles[l_isbn]
            except Exception as e:
                print(f"Error al cargar préstamos: {e}")

    def añadir_libro(self, libro):
        if libro.isbn not in self.catalogo_completo:
            self.catalogo_completo[libro.isbn] = libro
            self.libros_disponibles[libro.isbn] = libro
            self.guardar_datos()
            print(f"Sistema: Libro '{libro.titulo}' registrado en el catálogo maestro.")
        else:
            print(f"Error: El ISBN {libro.isbn} ya existe.")

    def quitar_libro(self, isbn):
        if isbn in self.catalogo_completo:
            # Verificar si está prestado antes de eliminar
            disponible = isbn in self.libros_disponibles
            if disponible:
                del self.catalogo_completo[isbn]
                del self.libros_disponibles[isbn]
                self.guardar_datos()
                print(f"Sistema: Libro eliminado del catálogo.")
            else:
                print(f"Error: No se puede eliminar un libro que está actualmente prestado.")
        else:
            print(f"Error: ISBN no encontrado.")

    def registrar_usuario(self, usuario):
        if usuario.user_id not in self.usuarios_ids:
            self.usuarios_ids.add(usuario.user_id)
            self.usuarios[usuario.user_id] = usuario
            self.guardar_datos()
            print(f"Sistema: Usuario '{usuario.nombre}' registrado con éxito.")
        else:
            print(f"Error: El ID {usuario.user_id} ya existe.")

    def dar_baja_usuario(self, user_id):
        if user_id in self.usuarios:
            usuario = self.usuarios[user_id]
            if not usuario.libros_prestados:
                self.usuarios_ids.remove(user_id)
                del self.usuarios[user_id]
                self.guardar_datos()
                print(f"Sistema: Usuario '{usuario.nombre}' eliminado.")
            else:
                print(f"Error: No se puede dar de baja a un usuario con préstamos pendientes.")
        else:
            print(f"Error: Usuario no encontrado.")

    def prestar_libro(self, isbn, user_id):
        if isbn in self.libros_disponibles and user_id in self.usuarios:
            libro = self.libros_disponibles.pop(isbn)
            self.usuarios[user_id].libros_prestados.append(libro)
            self.guardar_datos() # Esto actualizará prestamos.txt
            print(f"Sistema: Libro '{libro.titulo}' prestado exitosamente.")
        else:
            print(f"Error: ISBN no disponible o ID de usuario no registrado.")

    def devolver_libro(self, isbn, user_id):
        if user_id in self.usuarios:
            usuario = self.usuarios[user_id]
            for i, libro in enumerate(usuario.libros_prestados):
                if libro.isbn == isbn:
                    libro_devuelto = usuario.libros_prestados.pop(i)
                    self.libros_disponibles[isbn] = libro_devuelto
                    self.guardar_datos() # Esto actualizará prestamos.txt
                    print(f"Sistema: '{libro_devuelto.titulo}' devuelto con éxito.")
                    return
            print(f"Error: El usuario no tiene ese libro.")
        else:
            print(f"Error: Usuario no encontrado.")

    def buscar_libro(self, criterio, valor):
        valor = valor.lower()
        # Buscamos en el catálogo maestro para ver todos los libros, 
        # o solo en disponibles si prefieres. Aquí buscaremos en TODOS.
        resultados = []
        libros_a_buscar = self.catalogo_completo.values()
        
        if criterio == "1":
            resultados = [l for l in libros_a_buscar if valor in l.titulo.lower()]
        elif criterio == "2":
            resultados = [l for l in libros_a_buscar if valor in l.autor.lower()]
        elif criterio == "3":
            resultados = [l for l in libros_a_buscar if valor in l.categoria.lower()]
        
        if resultados:
            print("\nResultados del Catálogo:")
            for libro in resultados:
                estatus = "[DISPONIBLE]" if libro.isbn in self.libros_disponibles else "[PRESTADO]"
                print(f"{estatus} {libro}")
        else:
            print("No se encontraron coincidencias en el catálogo.")

    def listar_libros_prestados(self, user_id):
        if user_id in self.usuarios:
            usuario = self.usuarios[user_id]
            print(f"\nLibros de {usuario.nombre}:")
            if usuario.libros_prestados:
                for libro in usuario.libros_prestados:
                    print(libro)
            else:
                print("Ninguno.")
        else:
            print("Error: Usuario no encontrado.")

def menu():
    biblioteca = Biblioteca()
    
    while True:
        print("\nSISTEMA DE GESTIÓN DE BIBLIOTECA DIGITAL\n")
        print("1. Añadir Libro al Catálogo")
        print("2. Quitar Libro del Catálogo")
        print("3. Registrar Usuario")
        print("4. Dar de Baja Usuario")
        print("5. Prestar Libro")
        print("6. Devolver Libro")
        print("7. Buscar Libro (Catálogo)")
        print("8. Ver Libros de un Usuario")
        print("9. Salir")
        
        opcion = input("\nSeleccione una opción: ")
        
        try:
            if opcion == "1":
                lib = Libro(input("Título: "), input("Autor: "), input("Categoría: "), input("ISBN: "))
                biblioteca.añadir_libro(lib)
            elif opcion == "2":
                biblioteca.quitar_libro(input("ISBN del libro a eliminar: "))
            elif opcion == "3":
                usr = Usuario(input("Nombre: "), input("ID único: "))
                biblioteca.registrar_usuario(usr)
            elif opcion == "4":
                biblioteca.dar_baja_usuario(input("ID del usuario: "))
            elif opcion == "5":
                biblioteca.prestar_libro(input("ISBN: "), input("ID Usuario: "))
            elif opcion == "6":
                biblioteca.devolver_libro(input("ISBN: "), input("ID Usuario: "))
            elif opcion == "7":
                print("\nBuscar por: 1. Título | 2. Autor | 3. Categoría")
                biblioteca.buscar_libro(input("Criterio: "), input("Texto: "))
            elif opcion == "8":
                biblioteca.listar_libros_prestados(input("ID Usuario: "))
            elif opcion == "9":
                print("Saliendo y guardando datos...")
                break
            else:
                print("Opción no válida.")
        except KeyboardInterrupt:
            print("\nAcción cancelada. Volviendo al menú.")
        except Exception as e:
            print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    menu()
