from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views_academico import (
    EstudianteController, DocenteController, MateriaController, MatriculaController
)
from main import MenuCRUD


class MenuMatriculas(MenuCRUD):
    def __init__(self, controlador):
        super().__init__(controlador, "MATRÍCULAS")
        self._opciones = {
            "1": ("Registrar matrícula", self.crear),
            "2": ("Ver todos", self.listar),
            "3": ("Buscar", self.buscar),
            "4": ("Ver por id", self.ver_por_id),
            "5": ("Actualizar", self.actualizar),
            "6": ("Eliminar", self.eliminar),
            "7": ("Agregar nota", self.agregar_nota),
            "8": ("Ver boletín", self.ver_boletin),
            "0": ("Volver", self.volver),
        }
    def crear(self):
        imprimir_titulo("REGISTRAR MATRÍCULA")
        estudiante_id = self.pedir_entero("Id del estudiante: ")
        if estudiante_id is None:
            imprimir_error("El id debe ser un número")
            return self.pausa()
        materia_id = self.pedir_entero("Id de la materia: ")
        if materia_id is None:
            imprimir_error("El id debe ser un número")
            return self.pausa()
        periodo = input("Fecha (dd-mm-aaaa, Enter = hoy): ").strip()
        self.mostrar_resultado(
            *self._controlador.crear({
                "estudiante_id": estudiante_id,
                "materia_id": materia_id,
                "periodo": periodo
            })
        )
        self.pausa()

    def agregar_nota(self):
        imprimir_titulo("AGREGAR NOTA")
        matricula_id = self.pedir_entero("Id de la matrícula: ")
        if matricula_id is None:
            imprimir_error("Id inválido")
            return self.pausa()
        tipo = input("Tipo (deber / lección / examen): ").strip()
        try:
            valor = float(input("Valor (0-20): "))
        except ValueError:
            imprimir_error("Valor inválido")
            return self.pausa()
        peso_txt = input("Peso (Enter = 1): ").strip()
        peso = float(peso_txt) if peso_txt else 1
        self.mostrar_resultado(
            *self._controlador.agregar_nota(matricula_id, tipo, valor, peso)
        )
        self.pausa()

    def ver_boletin(self):
        imprimir_titulo("BOLETÍN")
        estudiante_id = self.pedir_entero("Id del estudiante: ")
        texto = self._controlador.boletin(estudiante_id) if estudiante_id else None
        if texto is None:
            imprimir_error("No existe ese estudiante")
        else:
            print(texto)
        self.pausa()


class MenuPrincipalAcademico:
    def __init__(self):
        estudiantes = EstudianteController()
        docentes = DocenteController()
        materias = MateriaController(docentes)
        matriculas = MatriculaController(estudiantes, materias)
        self._activo = True
        self._menus = {
            "1": MenuCRUD(estudiantes, "ESTUDIANTES"),
            "2": MenuCRUD(docentes, "DOCENTES"),
            "3": MenuCRUD(materias, "MATERIAS"),
            "4": MenuMatriculas(matriculas),
        }

    def ejecutar(self):
        while self._activo:
            imprimir_titulo("SISTEMA ACADÉMICO")
            print("  1. Estudiantes")
            print("  2. Docentes")
            print("  3. Materias")
            print("  4. Matrículas")
            print("  0. Salir\n")
            tecla = input("Opción: ").strip()
            if tecla == "0":
                imprimir_info("¡Hasta luego! 👋")
                self._activo = False
            elif tecla in self._menus:
                self._menus[tecla].ejecutar()
            else:
                imprimir_error("Opción no válida")
                MenuCRUD.pausa()


if __name__ == "__main__":
    try:
        MenuPrincipalAcademico().ejecutar()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")
