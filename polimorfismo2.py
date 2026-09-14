# Sin ABC: nada garantiza que las subclases implementen area()
class Figura:
    pass

class Circulo(Figura):
    def area(self):
        return 3.14 * self.radio ** 2

class Rectangulo(Figura):
    # ¡ups! olvidó implementar area()
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura


r = Rectangulo(5, 3)
r.area()          # AttributeError en tiempo de EJECUCIÓN
                  # Un bug que se descubre tarde