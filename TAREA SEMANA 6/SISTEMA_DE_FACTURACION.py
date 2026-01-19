# Programa de facturacion sencilla usando clases, herencia, encapsulación y polimorfismo.

# DEFINICIÓN DE CLASE Y ENCAPSULACIÓN
class Articulo:
    """
    Clase base que representa un artículo genérico.
    Utiliza encapsulación para proteger el atributo de precio.
    """
    def __init__(self, nombre, precio):
        self.nombre = nombre
        # Encapsulación, el guion bajo indica que es un atributo "protegido"
        self._precio = precio

    # Método para obtener el precio
    def get_precio(self):
        return self._precio

    # Método base que será sobrescrito (Polimorfismo)
    def mostrar_info(self):
        return f"Articulo: {self.nombre} | Precio: ${self._precio}"

# HERENCIA
class ProductoFactura(Articulo):
    """
    Clase derivada que hereda de Articulo.
    Añade la cantidad y métodos específicos para la factura.
    """
    def __init__(self, nombre, precio, cantidad):
        # Se llama al constructor de la clase padre (Articulo)
        super().__init__(nombre, precio)
        self.cantidad = cantidad

    # Método propio de esta clase para calcular el subtotal
    def calcular_subtotal(self):
        # Se accede al atributo protegido _precio de la clase padre
        return self._precio * self.cantidad

    # POLIMORFISMO
    # Se sobre el método mostrar_info 
    def mostrar_info(self):
        subtotal = self.calcular_subtotal()
        return f"Producto: {self.nombre} | Precio Unit: ${self._precio} | Cantidad: {self.cantidad} | Subtotal: ${subtotal}"

def main():
    print("\nSISTEMA DE FACTURACIÓN\n")
    
    lista_compras = []
    
    # Bucle para ingresar productos
    while True:
        try:
            nombre = input("Ingrese el nombre del producto o salir para facturar: ")
            if nombre.lower() == 'salir':
                break
            
            precio = float(input(f"Ingrese precio de {nombre}: "))
            cantidad = int(input(f"Ingrese cantidad de {nombre}: "))
            
            # Creación de Objeto (Instancia de la clase derivada)
            nuevo_producto = ProductoFactura(nombre, precio, cantidad)
            lista_compras.append(nuevo_producto)
            print("\n  Producto agregado correctamente.\n")
            
        except ValueError:
            print(" Error: Ingrese números válidos para el precio y cantidad.\n")

    # Muestra la factura final
    print("\n       DETALLE DE LA FACTURA\n")
    
    total_general = 0
    
    if not lista_compras:
        print("No se agregaron productos.")
    else:
        # Uso de Polimorfismo al iterar
        for prod in lista_compras:
            print(prod.mostrar_info())
            total_general += prod.calcular_subtotal()
            
        print(f"\nTOTAL A PAGAR: ${total_general:.2f}\n")

if __name__ == "__main__":
    main()
