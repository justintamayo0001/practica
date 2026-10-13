from models_academico import Estudiante, Docente, Materia, Matricula
from views import CrudBase


class EstudianteController(CrudBase):
    MODELO = Estudiante
    ARCHIVO = "data/estudiantes.json"
    NOMBRE = "estudiante"
    CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "carnet")

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            faltantes = [c for c in self.MODELO.OBLIGATORIOS
                         if not str(datos.get(c, "")).strip()]
            if faltantes:
                return f"Faltan campos obligatorios: {', '.join(faltantes)}"
        if "carnet" in datos and str(datos["carnet"]).strip():
            carnet = str(datos["carnet"]).strip().upper()
            usados = {r["carnet"].upper() for r in self.registros()
                      if r["id"] != id_actual}
            if carnet in usados:
                return f"El carnet {carnet} ya está registrado"
        return None


class DocenteController(CrudBase):
    MODELO = Docente
    ARCHIVO = "data/docentes.json"
    NOMBRE = "docente"
    CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "especialidad")

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            faltantes = [c for c in self.MODELO.OBLIGATORIOS
                         if not str(datos.get(c, "")).strip()]
            if faltantes:
                return f"Faltan campos obligatorios: {', '.join(faltantes)}"
        if "email" in datos:
            email = str(datos["email"]).strip().lower()
            usados = {r["email"].lower() for r in self.registros()
                      if r["id"] != id_actual}
            if email in usados:
                return "Ese email ya está registrado"
        return None


class MateriaController(CrudBase):
    MODELO = Materia
    ARCHIVO = "data/materias.json"
    NOMBRE = "materia"
    CAMPOS_BUSCABLES = ("nombre", "codigo")

    def __init__(self, docentes=None):
        super().__init__()
        self.docentes = docentes or DocenteController()

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            faltantes = [c for c in self.MODELO.OBLIGATORIOS
                         if not str(datos.get(c, "")).strip()]
            if faltantes:
                return f"Faltan campos obligatorios: {', '.join(faltantes)}"
        if "codigo" in datos and str(datos["codigo"]).strip():
            codigo = str(datos["codigo"]).strip().upper()
            usados = {r["codigo"].upper() for r in self.registros()
                      if r["id"] != id_actual}
            if codigo in usados:
                return f"Ya existe una materia con código {codigo}"
        if "docente_id" in datos and str(datos.get("docente_id", "")).strip() not in ("", "0", "None"):
            try:
                docente_id = int(datos["docente_id"])
            except (TypeError, ValueError):
                return "docente_id inválido"
            if not self.docentes.existe(docente_id):
                return f"No existe un docente con id {docente_id}"
        return None

    def asignar_docente(self, materia_id, docente_id):
        if not self.existe(materia_id):
            return False, f"No existe materia con id {materia_id}"
        if not self.docentes.existe(docente_id):
            return False, f"No existe docente con id {docente_id}"
        return self.actualizar(materia_id, {"docente_id": docente_id})

    def materias_de_docente(self, docente_id):
        return [m for m in self.listar() if m.docente_id == docente_id]


class MatriculaController(CrudBase):
    MODELO = Matricula
    ARCHIVO = "data/matriculas.json"
    NOMBRE = "matrícula"
    CAMPOS_BUSCABLES = ("periodo",)

    def __init__(self, estudiantes=None, materias=None):
        super().__init__()
        self.estudiantes = estudiantes or EstudianteController()
        self.materias = materias or MateriaController()

    def validar(self, datos, id_actual=None):
        try:
            estudiante_id = int(datos.get("estudiante_id", 0))
        except (TypeError, ValueError):
            return "El estudiante_id debe ser un número"
        if not self.estudiantes.existe(estudiante_id):
            return f"No existe un estudiante con id {estudiante_id}"
        try:
            materia_id = int(datos.get("materia_id", 0))
        except (TypeError, ValueError):
            return "El materia_id debe ser un número"
        if not self.materias.existe(materia_id):
            return f"No existe una materia con id {materia_id}"
        periodo = str(datos.get("periodo", "")).strip() or "2026-1"
        for registro in self.registros():
            if (registro["id"] != id_actual and
                registro["estudiante_id"] == estudiante_id and
                registro["materia_id"] == materia_id and
                registro.get("periodo", "") == periodo):
                return "El estudiante ya está matriculado en esa materia y periodo"
        return None

    def agregar_nota(self, matricula_id, tipo, valor, peso=1):
        matricula = self.obtener(matricula_id)
        if matricula is None:
            return False, f"No existe la matrícula {matricula_id}"
        try:
            matricula.agregar_nota(tipo, valor, peso)
        except ValueError as excepcion:
            return False, str(excepcion)
        registros = self.registros()
        for indice, registro in enumerate(registros):
            if registro["id"] == matricula_id:
                registros[indice] = matricula.a_diccionario()
                break
        self._gestor.guardar(registros)
        return True, f"Nota agregada. Promedio actual: {matricula.promedio}"

    def boletin(self, estudiante_id):
        estudiante = self.estudiantes.obtener(estudiante_id)
        if estudiante is None:
            return None
        matriculas = [m for m in self.listar() if m.estudiante_id == estudiante_id]
        if not matriculas:
            return f"El estudiante {estudiante.nombre_completo} no tiene matrículas."
        lineas = [
            f"BOLETÍN DE {estudiante.nombre_completo.upper()}",
            f"Carnet: {estudiante.carnet}",
            "-" * 50,
        ]
        suma_promedios = 0
        cantidad = 0
        for mat in matriculas:
            materia = self.materias.obtener(mat.materia_id)
            nombre_materia = materia.nombre if materia else f"Materia {mat.materia_id}"
            lineas.append(f"  {nombre_materia} ({mat.periodo})")
            lineas.append(f"    Promedio: {mat.promedio}  ·  Estado: {mat.estado}")
            for nota in mat.notas:
                lineas.append(f"      - {nota}")
            lineas.append("")
            if mat.notas:
                suma_promedios += mat.promedio
                cantidad += 1
        lineas.append("-" * 50)
        if cantidad:
            promedio_general = round(suma_promedios / cantidad, 2)
            lineas.append(f"  PROMEDIO GENERAL: {promedio_general}")
        else:
            lineas.append("  Sin notas registradas")
        return "\n".join(lineas)
