from abc import ABC, abstractmethod
from shared.json_manager import GestorJSON


class CrudBase(ABC):
    MODELO = None
    ARCHIVO = None
    NOMBRE = "registro"
    CAMPOS_BUSCABLES = ()

    def __init__(self):
        if self.MODELO is None or self.ARCHIVO is None:
            raise ValueError("El controlador debe definir MODELO y ARCHIVO")
        self._gestor = GestorJSON(self.ARCHIVO)

    @abstractmethod
    def validar(self, datos, id_actual=None):
        pass

    def preparar(self, datos):
        return {campo: datos.get(campo, "") for campo in self.MODELO.CAMPOS}

    def registros(self):
        return self._gestor.leer()

    def siguiente_id(self):
        ids = [registro["id"] for registro in self.registros()]
        return max(ids) + 1 if ids else 1

    def listar(self):
        return [self.MODELO.desde_diccionario(r) for r in self.registros()]

    def obtener(self, id_registro):
        for objeto in self.listar():
            if objeto.id == id_registro:
                return objeto
        return None

    def existe(self, id_registro):
        return any(r["id"] == id_registro for r in self.registros())

    def buscar(self, termino):
        termino = str(termino).strip().lower()
        if not termino:
            return []
        encontrados = []
        for registro in self.registros():
            for campo in self.CAMPOS_BUSCABLES:
                if termino in str(registro.get(campo, "")).lower():
                    encontrados.append(self.MODELO.desde_diccionario(registro))
                    break
        return encontrados

    def crear(self, datos):
        error = self.validar(datos)
        if error:
            return False, error
        try:
            objeto = self.MODELO(self.siguiente_id(), **self.preparar(datos))
        except ValueError as excepcion:
            return False, str(excepcion)
        registros = self.registros()
        registros.append(objeto.a_diccionario())
        if not self._gestor.guardar(registros):
            return False, "No se pudo escribir el archivo"
        return True, f"{self.NOMBRE.capitalize()} creado: {objeto.etiqueta()}"

    def actualizar(self, id_registro, cambios):
        desconocidos = set(cambios) - set(self.MODELO.CAMPOS)
        if desconocidos:
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"
        if not cambios:
            return False, "No se indicó ningún cambio"
        objeto = self.obtener(id_registro)
        if objeto is None:
            return False, f"No existe {self.NOMBRE} con id {id_registro}"
        error = self.validar(cambios, id_actual=id_registro)
        if error:
            return False, error
        try:
            for campo, valor in cambios.items():
                setattr(objeto, campo, valor)
        except ValueError as excepcion:
            return False, str(excepcion)
        registros = self.registros()
        for indice, registro in enumerate(registros):
            if registro["id"] == id_registro:
                registros[indice] = objeto.a_diccionario()
                break
        self._gestor.guardar(registros)
        return True, f"{self.NOMBRE.capitalize()} {id_registro} actualizado"

    def eliminar(self, id_registro):
        registros = self.registros()
        quedan = [r for r in registros if r["id"] != id_registro]
        if len(quedan) == len(registros):
            return False, f"No existe {self.NOMBRE} con id {id_registro}"
        self._gestor.guardar(quedan)
        return True, f"{self.NOMBRE.capitalize()} {id_registro} eliminado"
