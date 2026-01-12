# Este programa calcula el área de una figura.

# El usuario ingresa qué figura quiere calcular
figura = input("¿Qué figura quieres calcular (rectangulo/circulo)?: ").lower()

# Se usa una variable booleana para saber si es rectángulo
es_rectangulo = figura == "rectangulo"

# Se inicializa el área en 0.0
area = 0.0

if es_rectangulo:
    # Se solicita la base y la altura del rectángulo
    base = float(input("Ingresa la base del rectángulo: "))
    altura = float(input("Ingresa la altura del rectángulo: "))
    
    # Se calcula el área multiplicando base por altura
    area = base * altura
    
    # Muestra el resultado
    print(f"El área del rectángulo es: {area}")
else:
    # Si no es rectángulo se asume que es un círculo
    radio = float(input("Ingresa el radio del círculo: "))
    
    # Se usa un valor aproximado de pi
    pi = 3.1416
    
    # Se calculo el área del círculo
    area = pi * radio * radio
    
    # Muestra el resultado
    print(f"El área del círculo es: {area}")
