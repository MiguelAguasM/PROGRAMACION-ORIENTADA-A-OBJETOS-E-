# Tarea: Implementación de Constructor y Destructor en Python.
# Sistema de Gestion de Vehiculos, ingresa un vehiculo nuevo y luego lo elimina.

class Carro:

    def __init__(self, modelo,):
        # Aquí defino el constructor.
        # Se activa cuando ingreso el modelo del vehiculo
        self.modelo_carro = modelo
        print(f"\nEl vehiculo '{self.modelo_carro}' ha sido creado en el sistema.")

    def mostrar_detalle(self):
        # Este método solo sirve para confirmar que el objeto tiene el nombre guardado.
        print(f"Confirmación: El vehiculo registrado es un {self.modelo_carro}.")

    def __del__(self):
        # Aquí defino el destructor.
        # Se activa cuando el objeto ya no se usa o se cierra el programa
        print(f"El vehiculo '{self.modelo_carro}' ha sido eliminado correctamente.")

def inicio_sistema():
    print("\nSISTEMA DE GESTIÓN DE VEHÍCULOS\n")
    
    # Aquí pido al usuario que ingrese el modelo del vehiculo
    nombre_usuario = input("Por favor ingresa el modelo del vehiculo que deseas registrar: ")
    
    # Este codigo dispara el __init__
    mi_carro = Carro(nombre_usuario)
    
    # Uso el objeto para mostrar el dato
    mi_carro.mostrar_detalle()
    
    print("\nEl proceso ha terminado. El sistema liberará la memoria ahora:")
    # Al terminar la función la variable mi_carro se borra y se activa el __del__

if __name__ == "__main__":
    inicio_sistema()
    print("\nPrograma finalizado.")
