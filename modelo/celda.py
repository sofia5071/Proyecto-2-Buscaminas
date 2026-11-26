class Celda:
    def __init__(self, tiene_mina):
        self.tiene_mina = tiene_mina
        self.tiene_bandera = False
        self.esta_descubierta = False
        self.minas_adyacentes = 0
