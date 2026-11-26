import random
from enum import Enum
from celda import Celda
from itertools import product

class EstadoJuego(Enum):
    JUGANDO = "jugando"
    GANADO = "ganado"
    PERDIDO = "perdido"


class Tablero:
    def __init__(self, filas, columnas, minas):
        self.filas = filas
        self.columnas = columnas
        self.minas = minas
        self.estado = EstadoJuego.JUGANDO
        self.cuadricula: list[list[Celda]] = [] 
        self.reiniciar(filas, columnas, minas)

    def reiniciar(self, filas, columnas, minas):
        self.filas = filas
        self.columnas = columnas
        self.minas = minas
        self.estado = EstadoJuego.JUGANDO
        self.cuadricula = [[Celda(False) for _ in range(self.columnas)] for _ in range(self.filas)]
        
        coordenadas_minas = random.sample(list(product(range(self.filas), range(self.columnas))), self.minas)

        for f, c in coordenadas_minas:
            self.cuadricula[f][c].tiene_mina = True

        for f in range(self.filas):
            for c in range(self.columnas):
                if not self.cuadricula[f][c].tiene_mina:
                        self.contar_minas_adyacentes(f, c) 
        

    def contar_minas_adyacentes(self, fila, columna):
        for df in range(fila-1, fila+2):
            for dc in range(columna-1, columna+2):
                if ((df==fila and dc==columna) or not self.dentro_tablero(df, dc)): 
                    continue
                if self.cuadricula[df][dc].tiene_mina: 
                    self.cuadricula[fila][columna].minas_adyacentes += 1


    def dentro_tablero(self, fila, columna):
        return 0 <= fila < self.filas and 0 <= columna < self.columnas
    
    def descubrir_celda(self, fila, columna):
        if self.estado != EstadoJuego.JUGANDO:
            return self.estado

        celda = self.cuadricula[fila][columna]

        if celda.esta_descubierta or celda.tiene_bandera:
            return self.estado

        celda.esta_descubierta = True

        if celda.tiene_mina:
            self.estado = EstadoJuego.PERDIDO
            self.revelar_minas()
            return self.estado

        if (celda.minas_adyacentes == 0):
            stack = [(fila,columna)]

            while len(stack)>0:
                f, c = stack[-1]
                stack.pop()
                
                for df in range(f-1, f+2):
                    for dc in range(c-1, c+2):
                        if ((df==f and dc==c) or not self.dentro_tablero(df, dc)): 
                            continue
                        siguiente = self.cuadricula[df][dc]
                        if not siguiente.esta_descubierta and not siguiente.tiene_mina and not siguiente.tiene_bandera:
                            siguiente.esta_descubierta = True
                            if siguiente.minas_adyacentes == 0:
                                stack.append((df, dc))
        
        if self.todas_celdas_seguras_descubiertas():
            self.estado = EstadoJuego.GANADO

        return self.estado

    def alternar_bandera(self, fila, columna):
        if (self.estado != EstadoJuego.JUGANDO):
            return
        celda = self.cuadricula[fila][columna]
        if not celda.esta_descubierta:
            celda.tiene_bandera = not celda.tiene_bandera
                                
    def todas_celdas_seguras_descubiertas(self):
        for fila in self.cuadricula:
            for celda in fila:
                if not celda.tiene_mina and not celda.esta_descubierta:
                    return False
        return True

    def revelar_minas(self):
        for fila in self.cuadricula:
            for celda in fila:
                if celda.tiene_mina:
                    celda.esta_descubierta = True            
        