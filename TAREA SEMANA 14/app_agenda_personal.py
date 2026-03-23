import tkinter as tk
from tkinter import ttk, messagebox
import datetime

class AgendaApp:
    """
    Clase principal para la Aplicación de Agenda Personal.
    Utiliza componentes de Tkinter.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda Personal")
        self.root.geometry("600x500")

        # Variables para los campos de entrada
        hoy = datetime.date.today()
        self.dia_var = tk.StringVar(value=str(hoy.day))
        self.mes_var = tk.StringVar(value=str(hoy.month))
        self.anio_var = tk.StringVar(value=str(hoy.year))
        
        ahora = datetime.datetime.now()
        self.hora_var = tk.StringVar(value=ahora.strftime("%H:%M"))
        self.desc_var = tk.StringVar()

        self._setup_ui()

    def _setup_ui(self):
        """Configura los contenedores y widgets de la interfaz estándar."""
        
        # Frame de Entrada de Datos
        input_frame = tk.Frame(self.root, padx=10, pady=10)
        title_label = tk.Label(self.root, text="Nuevo Evento o Tarea", font=('Helvetica', 12, 'bold'))
        title_label.pack(anchor="w", padx=10, pady=(5,0))
        input_frame.pack(fill="x", padx=10, pady=5)

        # Selección de Fecha (DatePicker Alternativo con Spinboxes)
        tk.Label(input_frame, text="Fecha (Día/Mes/Año):").grid(row=0, column=0, sticky="w")
        
        date_selection_frame = tk.Frame(input_frame)
        date_selection_frame.grid(row=0, column=1, columnspan=3, sticky="w", padx=5)

        # Spinboxes para permitir selección (DatePicker manual)
        self.spin_dia = tk.Spinbox(date_selection_frame, from_=1, to=31, width=3, textvariable=self.dia_var)
        self.spin_dia.pack(side="left", padx=2)
        
        self.spin_mes = tk.Spinbox(date_selection_frame, from_=1, to=12, width=3, textvariable=self.mes_var)
        self.spin_mes.pack(side="left", padx=2)
        
        self.spin_anio = tk.Spinbox(date_selection_frame, from_=2024, to=2030, width=5, textvariable=self.anio_var)
        self.spin_anio.pack(side="left", padx=2)
        
        # Campo: Hora
        tk.Label(input_frame, text="Hora (HH:MM):").grid(row=0, column=4, sticky="w", padx=(10, 0))
        self.entry_hora = tk.Entry(input_frame, textvariable=self.hora_var, width=8)
        self.entry_hora.grid(row=0, column=5, padx=5, pady=5)

        # Campo: Descripción
        tk.Label(input_frame, text="Descripción:").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_desc = tk.Entry(input_frame, textvariable=self.desc_var, width=40)
        self.entry_desc.grid(row=1, column=1, columnspan=5, sticky="we", padx=5, pady=5)

        # Frame de Visualización (TreeView)
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("fecha", "hora", "descripcion")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("hora", text="Hora")
        self.tree.heading("descripcion", text="Descripción")

        self.tree.column("fecha", anchor="center", width=100)
        self.tree.column("hora", anchor="center", width=80)
        self.tree.column("descripcion", anchor="w", width=350)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Frame de Botones de Acción
        button_frame = tk.Frame(self.root, pady=10)
        button_frame.pack(fill="x")

        # Botones con texto normal y sin colores externos llamativos
        btn_crear = tk.Button(button_frame, text="Agregar Evento", command=self.add_event, padx=10)
        btn_crear.pack(side="left", padx=(120, 10))

        btn_eliminar = tk.Button(button_frame, text="Eliminar Evento Seleccionado", command=self.delete_event, padx=10)
        btn_eliminar.pack(side="left", padx=10)

        btn_salir = tk.Button(button_frame, text="Salir", command=self.exit_app, padx=10)
        btn_salir.pack(side="left", padx=10)

    def add_event(self):
        """Valida y agrega un nuevo evento."""
        # Construir la fecha desde los Spinboxes
        dia = self.dia_var.get().zfill(2)
        mes = self.mes_var.get().zfill(2)
        anio = self.anio_var.get()
        fecha = f"{dia}/{mes}/{anio}"
        
        hora = self.hora_var.get().strip()
        desc = self.desc_var.get().strip()

        if not desc or not hora:
            messagebox.showwarning("Campos vacíos", "Por favor, complete la descripción y la hora.")
            return

        try:
            # Validaciones de formato
            datetime.datetime.strptime(fecha, "%d/%m/%Y")
            datetime.datetime.strptime(hora, "%H:%M")
        except ValueError:
            messagebox.showerror("Error", "La fecha y hora no son válidas.")
            return

        # Agregar a la tabla
        self.tree.insert("", "end", values=(fecha, hora, desc))
        
        # Limpiar descripción
        self.desc_var.set("")
        # Actualizar hora
        self.hora_var.set(datetime.datetime.now().strftime("%H:%M"))

    def delete_event(self):
        """Elimina el evento seleccionado."""
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showwarning("Aviso", "Seleccione un evento de la lista.")
            return

        if messagebox.askyesno("Confirmar", "¿Eliminar evento seleccionado?"):
            for item in selected_item:
                self.tree.delete(item)

    def exit_app(self):
        """Cierra el programa."""
        if messagebox.askokcancel("Salir", "¿Desea salir de la aplicación?"):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AgendaApp(root)
    root.mainloop()
