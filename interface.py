from abc import ABC, abstractmethod

class Icrud(ABC):
    @abstractmethod
    def create(self, data):
       pass
    @abstractmethod
    def read(self, id):
       pass
    @abstractmethod
    def update(self, id, data):
        pass

    @abstractmethod
    def delete(self, id):
        pass



class Empleado(Icrud):
    def __init__(self, nombre, puesto):
        self.nombre = nombre
        self.puesto = puesto

    def create(self, data):
        print(f"Creando empleado: {data}")

    def read(self, id):
        print(f"Leyendo empleado con ID: {id}")

    def update(self, id, data):
        print(f"Actualizando empleado con ID: {id} a {data}")

    def delete(self, id):
        print(f"Eliminando empleado con ID: {id}")

class Cliente(Icrud):
    def __init__(self, nombre, correo):
        self.nombre = nombre
        self.correo = correo

    def create(self, data):
        print(f"Creando cliente: {data}")

    def read(self, id):
        print(f"Leyendo cliente con ID: {id}")

    def update(self, id, data):
        print(f"Actualizando cliente con ID: {id} a {data}")

    def delete(self, id):
        print(f"Eliminando cliente con ID: {id}")
emp = Empleado("Juan", "Desarrollador")
cli = Cliente("Ana", "dv@gmail.com")