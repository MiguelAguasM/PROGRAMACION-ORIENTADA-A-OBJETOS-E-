import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class AppGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.title("Ingreso de Estudiantes de la UEA - Tarea Semana 13")
        self.geometry("650x500")  # Aumentamos el ancho para la tabla
        self.config(padx=20, pady=20)

        # Componentes de la interfaz
        self.crear_componentes()

    def crear_componentes(self):
        # Contenedor para los campos de entrada
        self.frame_inputs = tk.Frame(self)
        self.frame_inputs.pack(pady=10)

        # Campo: Nombre
        tk.Label(self.frame_inputs, text="Nombre:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="e", pady=2)
        self.txt_nombre = tk.Entry(self.frame_inputs, width=40)
        self.txt_nombre.grid(row=0, column=1, pady=2, padx=5)

        # Campo: Cédula
        tk.Label(self.frame_inputs, text="Cédula:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="e", pady=2)
        self.txt_cedula = tk.Entry(self.frame_inputs, width=40)
        self.txt_cedula.grid(row=1, column=1, pady=2, padx=5)

        # Campo: Carrera
        tk.Label(self.frame_inputs, text="Carrera:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="e", pady=2)
        self.txt_carrera = tk.Entry(self.frame_inputs, width=40)
        self.txt_carrera.grid(row=2, column=1, pady=2, padx=5)

        # Botón Agregar
        self.btn_agregar = tk.Button(self, text="Agregar Estudiante", command=self.agregar_dato, width=20, bg="#4CAF50", fg="black")
        self.btn_agregar.pack(pady=10)

        # Título de la sección de visualización
        self.lbl_lista = tk.Label(self, text="Registro de Estudiantes:", font=("Arial", 12, "bold"))
        self.lbl_lista.pack(pady=(15, 5))

        # Contenedor para la Tabla (Treeview) y Scrollbar
        self.frame_tabla = tk.Frame(self)
        self.frame_tabla.pack(fill=tk.BOTH, expand=True)

        # Configuración de la Tabla
        columnas = ("nombre", "cedula", "carrera")
        self.tree = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings")
        
        # Definir encabezados
        self.tree.heading("nombre", text="Nombre Completo")
        self.tree.heading("cedula", text="Cédula / ID")
        self.tree.heading("carrera", text="Carrera Universitaria")

        # Ajustar ancho de columnas
        self.tree.column("nombre", width=200)
        self.tree.column("cedula", width=120)
        self.tree.column("carrera", width=200)

        # Scrollbar para la tabla
        self.scrollbar = tk.Scrollbar(self.frame_tabla, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Botón Eliminar
        self.btn_limpiar = tk.Button(self, text="Limpiar", command=self.limpiar_datos, width=30, bg="#f44336", fg="black")
        self.btn_limpiar.pack(pady=20)

    def agregar_dato(self):
        """Obtiene el texto de los campos y los agrega a la tabla si no están vacíos."""
        nombre = self.txt_nombre.get().strip()
        cedula = self.txt_cedula.get().strip()
        carrera = self.txt_carrera.get().strip()
        
        if nombre and cedula and carrera:
            # Insertar en el Treeview
            self.tree.insert("", tk.END, values=(nombre, cedula, carrera))
            
            # Limpiar los campos de entrada
            self.txt_nombre.delete(0, tk.END)
            self.txt_cedula.delete(0, tk.END)
            self.txt_carrera.delete(0, tk.END)
            self.txt_nombre.focus()
        else:
            messagebox.showwarning("Campos incompletos", "Por favor, complete todos los campos (Nombre, Cédula y Carrera).")

    def limpiar_datos(self):
        """Elimina la fila seleccionada de la tabla."""
        seleccion = self.tree.selection() # Obtiene el item seleccionado
        
        if seleccion:
            if messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar al estudiante seleccionado?"):
                for item in seleccion:
                    self.tree.delete(item)
        else:
            messagebox.showwarning("Sin selección", "Por favor, seleccione un estudiante de la tabla para eliminar.")

if __name__ == "__main__":
    app = AppGUI()
    app.mainloop()
