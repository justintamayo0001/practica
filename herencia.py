class Persona:
    def __init__(self, nombre, cedula):
        self.nombre = nombre
        self.cedula = cedula

    def presentarse(self):
        return f"Soy {self.nombre}"


class Empleado(Persona):
    def __init__(self, nombre, cedula, salario):
        super().__init__(nombre, cedula)   # llama al __init__ del padre
        self.salario = salario

    # Polimorfismo: redefinimos el método presentarse() del padre
    def presentarse(self):
        # Extendemos, no reemplazamos
        #base = super().presentarse()
        return f"{self.nombre}, empleado con salario ${self.salario}"


e = Empleado("Ana", "0912161234", 1200)
print(e.presentarse())
# Soy Ana, empleado con salario $1200