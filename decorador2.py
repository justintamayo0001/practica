

class Circulo:
    PI = 3.14159                          # atributo de clase

    def __init__(self, radio):
        self.radio = radio

    # ---------- MÉTODO NORMAL ----------
    # Recibe self (la instancia). Usa datos de esta instancia.
    def area(self):
        return Circulo.PI * self.radio ** 2

    # ---------- @property ----------
    # Se accede como atributo, se calcula dinámicamente
    @property
    def diametro(self):
        return self.radio * 2

    # ---------- @classmethod ----------
    # Recibe cls (la clase, no la instancia). Útil para fábricas
    # de objetos alternativas.
    @classmethod
    def desde_diametro(cls, diametro):
        """Crea un Circulo a partir del diámetro."""
        return cls(diametro / 2)          # cls = Circulo

    # ---------- @staticmethod ----------
    # No recibe ni self ni cls. Es una función suelta dentro de la clase,
    # agrupada allí por conveniencia (mismo namespace).
    @staticmethod
    def es_radio_valido(r):
        return r > 0


# --- Uso ---
c1 = Circulo(5)
print(c1.area())                          # normal
print(c1.diametro)                        # property (sin ())

c2 = Circulo.desde_diametro(20)           # classmethod - fábrica
print(c2.radio)                           # 10

print(Circulo.es_radio_valido(5))         # staticmethod - sin instancia
print(Circulo.es_radio_valido(-1))