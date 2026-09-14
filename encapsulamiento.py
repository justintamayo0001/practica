class Cuenta:
    def __init__(self, titular, saldo_inicial=0):
        self.titular = titular            # público
        self._saldo = saldo_inicial       # protegido por convención

    @property
    def saldo(self):
        """Getter: se usa como si fuera un atributo, no como método."""
        return self._saldo

    @saldo.setter
    def saldo(self, valor):
        """Setter con validación."""
        if valor < 0:
            raise ValueError("El saldo no puede ser negativo")
        self._saldo = valor

    def depositar(self, monto):
        if monto <= 0:
            raise ValueError("Monto debe ser positivo")
        self._saldo += monto

    def retirar(self, monto):
        if monto > self._saldo:
            raise ValueError("Saldo insuficiente")
        self._saldo -= monto


# --- Uso ---
tit1 = Cuenta("Ana", 100)
print(tit1.saldo)              # 100 — se accede SIN paréntesis (property)
tit1.depositar(50)             # 150
tit1.retirar(30)               # 120
tit1.saldo = 500               # setter — validado
tit2 = Cuenta("Daniel") 
print(tit2.saldo)           # 0 — saldo inicial
tit2.saldo = 300
print(tit2.saldo)           # 300
numeros=[2, 2, 3, 4, 5]
cuentas = [tit1,tit2]
for tit in cuentas:
    print(tit.titular," ",tit.saldo)           # 100, 0 — se accede SIN paréntesis (property)