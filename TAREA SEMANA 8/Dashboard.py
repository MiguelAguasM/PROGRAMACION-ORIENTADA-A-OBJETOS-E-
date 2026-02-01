import os
import subprocess

def limpiar_pantalla():
    """
    Nueva función implementada para limpiar la terminal según el sistema operativo.
    'cls' es para Windows y 'clear' para Mac o Linux, porque en mi soy usuario de una Macbook M4.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_codigo(ruta_script):
    # Asegúrate de que la ruta al script es absoluta
    ruta_script_absoluta = os.path.abspath(ruta_script)
    try:
        with open(ruta_script_absoluta, 'r') as archivo:
            codigo = archivo.read()
            print(f"\n--- Código de {ruta_script} ---\n")
            print(codigo)
            return codigo
    except FileNotFoundError:
        print("El archivo no se encontró.")
        return None
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
        return None

def ejecutar_codigo(ruta_script):
    try:
        if os.name == 'nt':  # Windows
            subprocess.Popen(['cmd', '/k', 'python', ruta_script])
        else:  # Unix-based systems
            subprocess.Popen(['xterm', '-hold', '-e', 'python3', ruta_script])
    except Exception as e:
        print(f"Ocurrió un error al ejecutar el código: {e}")

def buscar_script():
    """
    Permite al usuario buscar archivos .py en todas las carpetas del proyecto.
    Esta es una funcionalidad avanzada pero sencilla para agilizar el acceso a los ejercicios.
    """
    limpiar_pantalla()
    print("\nBuscador de Scripts")
    palabra_clave = input("Ingresa parte del nombre del archivo que buscas: ").strip().lower()
    
    if not palabra_clave:
        return

    encontrados = []
    # os.walk recorre el directorio actual
    for raiz, dirs, archivos in os.walk("."):
        for archivo in archivos:
            if palabra_clave in archivo.lower() and archivo.endswith(".py") and archivo != "Dashboard.py":
                encontrados.append(os.path.join(raiz, archivo))

    if not encontrados:
        print(f"\nNo se encontraron resultados para: '{palabra_clave}'")
    else:
        print(f"\nSe encontraron {len(encontrados)} scripts:")
        for i, ruta in enumerate(encontrados, 1):
            print(f"{i} - {ruta}")
        
        try:
            eleccion = int(input("\nSelecciona el número del script para verlo / ejecutarlo (0 para cancelar): "))
            if 1 <= eleccion <= len(encontrados):
                ruta_script = encontrados[eleccion - 1]
                codigo = mostrar_codigo(ruta_script)
                if codigo:
                    ejecutar = input("\n¿Deseas ejecutar este script? (1: Sí, 0: No): ")
                    if ejecutar == '1':
                        ejecutar_codigo(ruta_script)
        except ValueError:
            print("Entrada inválida. Debe ser un número.")
    
    input("\nPresiona Enter para volver al menú principal.")


def mostrar_menu():
    # Define la ruta base donde se encuentra el dashboard.py
    ruta_base = os.path.dirname(__file__)

    unidades = {
        '1': 'Unidad 1',
        '2': 'Unidad 2'
    }

    while True:
        limpiar_pantalla() # Se limpia la pantalla al inicio de cada ciclo
        print("\nMenu Principal - Dashboard")
        # Imprime las opciones del menú principal
        for key in unidades:
            print(f"{key} - {unidades[key]}")
        print("s - Buscar script") # Nueva opción de búsqueda
        print("0 - Salir")

        eleccion_unidad = input("Elige una unidad, 's' para buscar o '0' para salir: ")
        if eleccion_unidad == '0':
            print("Saliendo del programa.")
            break
        elif eleccion_unidad in unidades:
            mostrar_sub_menu(os.path.join(ruta_base, unidades[eleccion_unidad]))
        elif eleccion_unidad.lower() == 's': # Lógica para activar el buscador
            buscar_script()
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")
            input("Presiona Enter para continuar...")

def mostrar_sub_menu(ruta_unidad):
    sub_carpetas = [f.name for f in os.scandir(ruta_unidad) if f.is_dir()]

    while True:
        limpiar_pantalla() # Mantenemos la interfaz limpia
        print("\nSubmenú - Selecciona una subcarpeta")
        # Imprime las subcarpetas
        for i, carpeta in enumerate(sub_carpetas, start=1):
            print(f"{i} - {carpeta}")
        print("0 - Regresar al menú principal")

        eleccion_carpeta = input("Elige una subcarpeta o '0' para regresar: ")
        if eleccion_carpeta == '0':
            break
        else:
            try:
                eleccion_carpeta = int(eleccion_carpeta) - 1
                if 0 <= eleccion_carpeta < len(sub_carpetas):
                    mostrar_scripts(os.path.join(ruta_unidad, sub_carpetas[eleccion_carpeta]))
                else:
                    print("Opción no válida. Por favor, intenta de nuevo.")
            except ValueError:
                print("Opción no válida. Por favor, intenta de nuevo.")

def mostrar_scripts(ruta_sub_carpeta):
    scripts = [f.name for f in os.scandir(ruta_sub_carpeta) if f.is_file() and f.name.endswith('.py')]

    while True:
        limpiar_pantalla() # se mantiene la interfaz limpia
        print("\nScripts - Selecciona un script para ver y ejecutar")
        # Imprime los scripts
        for i, script in enumerate(scripts, start=1):
            print(f"{i} - {script}")
        print("0 - Regresar al submenú anterior")
        print("9 - Regresar al menú principal")

        eleccion_script = input("Elige un script, '0' para regresar o '9' para ir al menú principal: ")
        if eleccion_script == '0':
            break
        elif eleccion_script == '9':
            return  # Regresar al menú principal
        else:
            try:
                eleccion_script = int(eleccion_script) - 1
                if 0 <= eleccion_script < len(scripts):
                    ruta_script = os.path.join(ruta_sub_carpeta, scripts[eleccion_script])
                    codigo = mostrar_codigo(ruta_script)
                    if codigo:
                        ejecutar = input("¿Desea ejecutar el script? (1: Sí, 0: No): ")
                        if ejecutar == '1':
                            ejecutar_codigo(ruta_script)
                        elif ejecutar == '0':
                            print("No se ejecutó el script.")
                        else:
                            print("Opción no válida. Regresando al menú de scripts.")
                        input("\nPresiona Enter para volver al menú de scripts.")
                else:
                    print("Opción no válida. Por favor, intenta de nuevo.")
            except ValueError:
                print("Opción no válida. Por favor, intenta de nuevo.")

# Ejecutar el dashboard
if __name__ == "__main__":
    mostrar_menu()