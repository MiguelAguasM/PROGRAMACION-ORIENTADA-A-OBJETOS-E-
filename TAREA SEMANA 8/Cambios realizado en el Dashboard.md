Estimado profesor, he actualizado el archivo Dashboard.py 
con las 2 nuevas funcionalidades y tambien agregue comentarios descriptivos.

1.- Funcionalidad incrementada: 

limpiar_pantalla()

Utiliza os.system para limpiar la consola.
Es compatible con Windows (cls) como con Mac o Linux (clear), ya que soy usuario de una Macbook M4.
Se invoca al inicio de cada menú para que la navegación sea más limpia.

2.- Funcionalidad incrementada: 

buscar_script()

Usa os.walk para buscar todos los archivos .py en cualquier carpeta o subcarpeta.

Permite al usuario encontrar un ejercicio específico escribiendo una palabra clave (como "herencia" o "clase").
Tiene la lógica para ver el código y ejecutar el script encontrado directamente desde el resultado de la búsqueda.

3.- Funcionalidad incrementada en: 

mostrar_menu()

Se añadió la opción 's' al menú principal, la cual sirve para buscar scripts.
