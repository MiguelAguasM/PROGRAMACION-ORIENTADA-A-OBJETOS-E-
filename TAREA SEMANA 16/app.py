"""
Esta aplicacion permite gestionar una lista de tareas,permitiendo al usuario añadir 
nuevas tareas, marcarlas como completadas y eliminarlas. 
La aplicación responde a los eventos del usuario, como clics del ratón y 
pulsaciones del teclado.
"""

import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Tareas")
        self.root.geometry("450x550")
        self.root.configure(bg="#f0f2f5")

        # Fuentes
        self.title_font = ("Segoe UI", 18, "bold")
        self.base_font = ("Segoe UI", 11)

        # Estilos
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=self.base_font, padding=6)
        self.style.configure("Add.TButton", background="#4CAF50", foreground="white")
        self.style.map("Add.TButton", background=[("active", "#45a049")])
        self.style.configure("Delete.TButton", background="#f44336", foreground="white")
        self.style.map("Delete.TButton", background=[("active", "#da190b")])
        self.style.configure("Complete.TButton", background="#2196F3", foreground="white")
        self.style.map("Complete.TButton", background=[("active", "#0b7dda")])
        self.style.configure("Edit.TButton", background="#FF9800", foreground="white")
        self.style.map("Edit.TButton", background=[("active", "#F57C00")])
        
        # Título
        self.label_titulo = tk.Label(
            root, text="Lista de Tareas Pendientes", 
            font=self.title_font, bg="#f0f2f5", fg="#1c1e21", pady=20
        )
        self.label_titulo.pack()

        # Entrada y botón de añadir
        frame_input = tk.Frame(root, bg="#f0f2f5")
        frame_input.pack(pady=10, padx=20, fill="x")

        self.entry_tarea = ttk.Entry(frame_input, font=self.base_font)
        self.entry_tarea.pack(side="left", fill="x", expand=True, padx=(0, 10))
        # Captura tecla Enter para añadir tarea
        self.entry_tarea.bind("<Return>", lambda event: self.add_task())

        self.btn_add = ttk.Button(
            frame_input, text="Añadir Tarea", 
            style="Add.TButton", command=self.add_task
        )
        self.btn_add.pack(side="right")

        # Lista de tareas Listbox con Scrollbar
        frame_list = tk.Frame(root, bg="#f0f2f5")
        frame_list.pack(pady=10, padx=20, fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(frame_list)
        self.scrollbar.pack(side="right", fill="y")

        self.listbox_tareas = tk.Listbox(
            frame_list, font=self.base_font, 
            bg="white", fg="#4b4f56",
            selectbackground="#e7f3ff", selectforeground="#1877f2",
            height=12, bd=0, highlightthickness=1,
            highlightbackground="#dddfe2", relief="flat",
            yscrollcommand=self.scrollbar.set
        )
        self.listbox_tareas.pack(side="left", fill="both", expand=True)
        self.scrollbar.config(command=self.listbox_tareas.yview)

        # Opcional: Doble clic para marcar como completada
        self.listbox_tareas.bind("<Double-Button-1>", lambda event: self.mark_completed())
        # Captura tecla Enter en la lista para editar la tarea seleccionada
        self.listbox_tareas.bind("<Return>", lambda event: self.edit_task())
        
        # Atajos de teclado solicitados
        # Tecla C para marcar como completada
        self.root.bind("<KeyPress-c>", self.handle_shortcuts)
        self.root.bind("<KeyPress-C>", self.handle_shortcuts)
        # Tecla Delete o D o d para eliminar (compatible con Windows y Mac)
        self.root.bind("<Delete>", self.handle_shortcuts)     # Suprimir para Windows
        self.root.bind("<BackSpace>", self.handle_shortcuts)  # En Mac 'Delete'
        self.root.bind("<KeyPress-d>", self.handle_shortcuts)
        self.root.bind("<KeyPress-D>", self.handle_shortcuts)
        # Tecla Escape para cerrar la aplicación
        self.root.bind("<Escape>", lambda event: self.root.destroy())

        # Frame para botones de acción
        frame_botones = tk.Frame(root, bg="#f0f2f5")
        frame_botones.pack(pady=20, padx=20, fill="x")

        self.btn_complete = ttk.Button(
            frame_botones, text="Marcar como Completada", 
            style="Complete.TButton", command=self.mark_completed
        )
        self.btn_complete.pack(side="left", fill="x", expand=True, padx=(0, 2))

        self.btn_edit = ttk.Button(
            frame_botones, text="Editar Tarea", 
            style="Edit.TButton", command=self.edit_task
        )
        self.btn_edit.pack(side="left", fill="x", expand=True, padx=2)

        self.btn_delete = ttk.Button(
            frame_botones, text="Eliminar Tarea", 
            style="Delete.TButton", command=self.delete_task
        )
        self.btn_delete.pack(side="left", fill="x", expand=True, padx=(2, 0))

        # Muestra los atajos en la aplicacion
        self.label_shortcuts = tk.Label(
            root, 
            text="Atajos de teclado: C para Marcar como Tarea Completada - D/Del/Suprimir para Eliminar\nEnter sobre la tarea para Editar - Esc para Salir de la Aplicación",
            font=("Segoe UI", 9), bg="#f0f2f5", fg="#64748b", justify="center"
        )
        self.label_shortcuts.pack(side="bottom", pady=(0, 15))

        # Información del estudiante y asignatura
        self.label_dev = tk.Label(
            root, text="Desarrollado por Miguel Aguas - Asignatura POO",
            font=("Segoe UI", 8, "italic"), bg="#f0f2f5", fg="#94a3b8"
        )
        self.label_dev.pack(side="bottom", pady=(0, 5))

        # Estado de edición e inicialización
        self.filename = "tareas.json"
        self.editing_index = None
        
        # Cargar tareas guardadas al iniciar
        self.load_tasks_from_file()

    # Lógica de la Aplicación

    def add_task(self):

        # Añade una nueva tarea o guarda los cambios de una existente.
        tarea = self.entry_tarea.get().strip()
        if tarea:
            if self.editing_index is not None:
                # En la edición de la tarea reemplaza en la posición que estaba la tarea
                self.listbox_tareas.delete(self.editing_index)
                self.listbox_tareas.insert(self.editing_index, tarea)
                
                # Resetea el estado de edición
                self.editing_index = None
                self.btn_add.config(text="Añadir Tarea")
            else:
                # Añade la tarea al final de la lista
                self.listbox_tareas.insert(tk.END, tarea)
            
            self.entry_tarea.delete(0, tk.END)
            self.save_tasks_to_file()
        else:
            messagebox.showwarning("Campo Vacío", "Por favor, escribe una tarea antes de añadirla.")

    def edit_task(self):
        """
        Carga la tarea seleccionada en el modo de edición sin borrarla.
        Al presionar Enter en el Entry o entrada, se actualiza en su misma posición.
        """
        try:
            self.editing_index = self.listbox_tareas.curselection()[0]
            tarea_actual = self.listbox_tareas.get(self.editing_index)
            
            # Limpia el estado previo si lo tuviera
            tarea_limpia = tarea_actual.replace(" (Completada)", "")
            
            # Carga la tarea en el Entry
            self.entry_tarea.delete(0, tk.END)
            self.entry_tarea.insert(0, tarea_limpia)
            self.entry_tarea.focus_set()

            # Cambia el texto del botón para indicar que se esta editando la tarea
            self.btn_add.config(text="Guardar Cambios")
        except IndexError:
            messagebox.showwarning("Sin selección", "Por favor, selecciona una tarea para editarla.")

    def mark_completed(self):
        """
        feedback visual para las tareas:
        -Se agreaga el textual '(Completada)' para las tareas completadas.
        -Se cambia el color de fuente y fondo para diferenciarla visualmente para las tareas completadas.
        """
        try:
            # Obtiene el índice de la tarea seleccionada por el cursor
            index = self.listbox_tareas.curselection()[0]
            tarea_actual = self.listbox_tareas.get(index)
            
            if " (Completada)" not in tarea_actual:
                nueva_tarea = f"{tarea_actual} (Completada)"
                # Reemplaza el elemento para actualizar el texto
                self.listbox_tareas.delete(index)
                self.listbox_tareas.insert(index, nueva_tarea)
                
                # Modifica el estilo visual (Feedback Visual)
                # Texto en gris y fondo ligeramente diferente para diferenciarla
                self.listbox_tareas.itemconfig(index, fg="#94a3b8", bg="#f9fafb")
                
                self.listbox_tareas.select_clear(0, tk.END)
                self.save_tasks_to_file()
        except IndexError:
            # Si no hay nada seleccionado, se lanza un aviso preventivo
            messagebox.showwarning("Sin selección", "Por favor, selecciona una tarea para marcarla como completada.")

    def handle_shortcuts(self, event):

        # Si el foco está en la entrada de texto, se ignoran los atajos de completar/eliminar
        # para permitir que el usuario escriba normalmente.
        if event.widget == self.entry_tarea:
            return

        key = event.keysym.lower()
        
        if key == 'c':
            self.mark_completed()
        elif key in ['d', 'delete', 'backspace']:
            self.delete_task()

    def delete_task(self):

        # Elimina la tarea seleccionada del componente Listbox.
        try:
            index = self.listbox_tareas.curselection()[0]
            self.listbox_tareas.delete(index)
            self.save_tasks_to_file()
        except IndexError:
            messagebox.showwarning("Sin selección", "Por favor, selecciona una tarea para eliminarla.")

    def save_tasks_to_file(self):
        """
        Guarda todas las tareas actuales en un archivo JSON.
        """
        tareas = []
        for i in range(self.listbox_tareas.size()):
            item_text = self.listbox_tareas.get(i)
            is_completed = " (Completada)" in item_text
            tarea_limpia = item_text.replace(" (Completada)", "")
            tareas.append({
                "texto": tarea_limpia,
                "completada": is_completed
            })
        
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(tareas, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error al guardar: {e}")

    def load_tasks_from_file(self):
        """
        Carga las tareas guardadas desde el archivo JSON al iniciar la aplicación.
        """
        if not os.path.exists(self.filename):
            return

        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                tareas = json.load(f)
                
            for tarea in tareas:
                texto_display = tarea["texto"]
                if tarea["completada"]:
                    texto_display += " (Completada)"
                
                self.listbox_tareas.insert(tk.END, texto_display)
                
                # Aplica el feedback visual si la tarea está completada
                if tarea["completada"]:
                    nuevo_index = self.listbox_tareas.size() - 1
                    self.listbox_tareas.itemconfig(nuevo_index, fg="#94a3b8", bg="#f9fafb")
        except Exception as e:
            print(f"Error al cargar: {e}")

if __name__ == "__main__":
    # Inicializa el entorno Tkinter
    root = tk.Tk()
    app = TodoApp(root)
    # Ejecuta el bucle principal de eventos
    root.mainloop()
