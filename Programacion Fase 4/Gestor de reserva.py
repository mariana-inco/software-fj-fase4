class GestorReservas:

    def __init__(self):
        self._reservas = []

    def agregar_reserva(self, reserva):
        self._reservas.append(reserva)

    def listar_reservas(self):
        return self._reservas

    def buscar_por_estado(self, estado):
        return [
            r for r in self._reservas
            if r.estado == estado
        ]