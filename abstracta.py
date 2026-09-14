from abc import ABC, abstractmethod

class Figura(ABC):                     # hereda de ABC → es abstracta
    @abstractmethod
    def area(self):
        """Cada figura debe implementar su cálculo de área."""
        pass

    @abstractmethod
    def perimetro(self):
        pass

    def describir(self):                # método concreto (opcional)
        return f"{type(self).__name__}: área={self.area()}, perímetro={self.perimetro()}"

    def mostrar(self):                 # método concreto (opcional)
        print("soy la clase Figura abstracta")

class Circulo(Figura):
    def __init__(self, radio):
        self.radio = radio

    def area(self):
        return 3.14159 * self.radio ** 2

    def perimetro(self):
        return 2 * 3.14159 * self.radio


class Rectangulo(Figura):
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura

    def area(self):
        return self.base * self.altura
    # ¡Olvidó perimetro()!


# --- Uso ---
c = Circulo(5)                          # OK
print(c.describir())

#r = Rectangulo(5, 3)
# TypeError: Can't instantiate abstract class Rectangulo
#            with abstract method perimetro
# Python NO deja crear la instancia hasta que se implementen TODOS
# los métodos abstractos. Bug detectado en tiempo de instanciación.

#f = Figura()                          # TypeError también:
                                        # no puedes instanciar la clase abstracta directamente