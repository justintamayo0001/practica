class Figura:
    def area(self):
        raise NotImplementedError("Cada figura debe implementar area()")


class Circulo(Figura):
    def __init__(self, radio):
        self.radio = radio

    def area(self):
        return 3.14159 * self.radio ** 2


class Rectangulo(Figura):
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura

    def area(self):
        return self.base * self.altura


# Polimorfismo: mismo bucle, distinto cálculo
""" c1 = Circulo(5)
r1 = Rectangulo(4, 3)
c2 = Circulo(2)
figuras = [c1, r1, c2] """
figuras = [Circulo(5), Rectangulo(4, 3), Circulo(2)]
total = 0
for f in figuras:
    total += f.area()      # cada figura sabe cómo calcularse

print(f"Área total: {total:.2f}")