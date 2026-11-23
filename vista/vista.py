import tkinter as tk
from tkinter import ttk

class VistaBuscaminas:
    def __init__(self, root):
        self.root = root
        self.root.title("Buscaminas - Proyecto MVC")
        self.root.configure(bg="#f0f0f0")
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.botones = []
        self.callback_izquierdo = None
        self.callback_derecho = None
        self.callback_nuevo = None

        # --- Controles superiores ---
        self.frame_top = tk.Frame(root, bg="#f0f0f0")
        self.frame_top.pack(pady=10)

        self.btn_nuevo = ttk.Button(self.frame_top, text="Nuevo Juego", command=self._on_nuevo)
        self.btn_nuevo.pack(side=tk.LEFT, padx=10)

        # Arreglamos el ancho del temporizador para que no se corte el texto
        self.label_tiempo = tk.Label(self.frame_top, text="Tiempo: 000", font=("Consolas", 14, "bold"), 
                                     bg="black", fg="red", width=12)
        self.label_tiempo.pack(side=tk.LEFT, padx=20)

        # --- Frame para el tablero ---
        self.frame_tablero = tk.Frame(root, bg="#a0a0a0", bd=3, relief="sunken")
        self.frame_tablero.pack(padx=15, pady=10)

    def set_callbacks(self, on_izquierdo, on_derecho, on_nuevo):
        self.callback_izquierdo = on_izquierdo
        self.callback_derecho = on_derecho
        self.callback_nuevo = on_nuevo

    def _on_nuevo(self):
        if self.callback_nuevo:
            self.callback_nuevo()

    def construir_tablero(self, filas, columnas):
        for widget in self.frame_tablero.winfo_children():
            widget.destroy()
        self.botones = []

        for f in range(filas):
            fila_botones = []
            for c in range(columnas):
                # highlightthickness=0 quita el borde feo de selección
                # bd=1 y relief="solid" hace que se vean como cuadritos unidos
                btn = tk.Button(self.frame_tablero, text="", width=2, height=1, 
                                font=("Arial", 12, "bold"), bg="#d0d0d0", relief="solid", bd=1,
                                highlightthickness=0)
                
                btn.bind("<Button-1>", lambda e, f=f, c=c: self._clic_izq(f, c))
                btn.bind("<Button-3>", lambda e, f=f, c=c: self._clic_der(f, c))
                
                # padx=1 y pady=1 separa un micro-pixel para que se vean las líneas
                btn.grid(row=f, column=c, padx=1, pady=1)
                fila_botones.append(btn)
            self.botones.append(fila_botones)

    def _clic_izq(self, f, c):
        if self.callback_izquierdo:
            self.callback_izquierdo(f, c)

    def _clic_der(self, f, c):
        if self.callback_derecho:
            self.callback_derecho(f, c)

    def actualizar_celda(self, f, c, estado_visual):
        btn = self.botones[f][c]
        
        if estado_visual == "cubierta":
            btn.config(text="", bg="#d0d0d0", state="normal", relief="solid")
        
        elif estado_visual == "bandera":
            # F de Bandera, roja
            btn.config(text="F", fg="#FF0000", bg="#d0d0d0", state="normal", relief="solid")
        
        elif estado_visual == "mina":
            # Ahora es una X negra grande en fondo rojo claro
            btn.config(text="X", bg="#ff8888", state="disabled", relief="flat",
                       disabledforeground="#000000")
        
        elif estado_visual == "vacia":
            # Fondo blanco para casillas destapadas
            btn.config(text="", bg="#ffffff", state="disabled", relief="flat")
        
        elif isinstance(estado_visual, int): # Es un número
            btn.config(text=str(estado_visual), bg="#ffffff", state="disabled", relief="flat",
                       disabledforeground=self._color_numero(estado_visual))

    def _color_numero(self, n):
        colores = {1: "#0000FF", 2: "#008000", 3: "#FF0000", 4: "#000080", 
                   5: "#800000", 6: "#008080", 7: "#000000", 8: "#808080"}
        return colores.get(n, "black")

    def actualizar_temporizador(self, segundos):
        self.label_tiempo.config(text=f"Tiempo: {segundos:03d}")

    def bloquear_tablero(self):
        for fila in self.botones:
            for btn in fila:
                btn.config(state="disabled")

# ==========================================
# BLOQUE DE PRUEBA
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    vista = VistaBuscaminas(root)
    vista.construir_tablero(9, 9)
    
    # Llenamos una zona para probar cómo se ve el juego real
    vista.actualizar_celda(0, 0, 1)
    vista.actualizar_celda(0, 1, 2)
    vista.actualizar_celda(0, 2, 3)
    vista.actualizar_celda(0, 3, "vacia")
    vista.actualizar_celda(0, 4, "vacia")
    
    vista.actualizar_celda(1, 0, "bandera")
    vista.actualizar_celda(5, 5, "mina")
    
    vista.actualizar_temporizador(42)
    
    root.mainloop()
