from dataclasses import dataclass
from typing import Optional

@dataclass
class Resultado:
    """Patrón Result para encapsular respuestas de operaciones."""
    exito: bool
    mensaje: str
    datos: Optional[dict] = None


class Materia:
    """Representa el componente base de la asignatura."""

    def __init__(self, codigo: str, nombre: str, creditos: int):
        if not codigo or not nombre:
            raise ValueError("[Error] Código y nombre son obligatorios.")
        if creditos <= 0:
            raise ValueError("[Error] Los créditos deben ser mayores a cero.")
        
        self.__codigo = codigo
        self.__nombre = nombre
        self.__creditos = creditos

    @property
    def codigo(self) -> str:
        return self.__codigo

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def creditos(self) -> int:
        return self.__creditos

    def __repr__(self) -> str:
        return f"Materia({self.__codigo}, {self.__nombre}, {self.__creditos}cr)"


class Estudiante:
    """Entidad que contiene los datos del estudiante."""

    def __init__(
        self, identificacion: str, nombre: str, limite_creditos: int = 16
    ):
        if not identificacion or not nombre:
            raise ValueError("[Error] Identificación y nombre son obligatorios.")
        if limite_creditos <= 0:
            raise ValueError("[Error] El límite de créditos debe ser positivo.")
        
        self.__identificacion = identificacion
        self.__nombre = nombre
        self.__limite_creditos = limite_creditos

    @property
    def identificacion(self) -> str:
        return self.__identificacion

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def limite_creditos(self) -> int:
        return self.__limite_creditos

    def __repr__(self) -> str:
        return f"Estudiante({self.__identificacion}, {self.__nombre})"


class Inscripcion:
    """Gestiona la relación de composición entre Estudiante y Materias (SRP)."""

    def __init__(self, estudiante: Estudiante):
        if not isinstance(estudiante, Estudiante):
            raise TypeError("[Error] El parámetro debe ser una instancia de Estudiante.")
        
        self.__estudiante = estudiante
        self.__materias: list[Materia] = []

    @property
    def estudiante(self) -> Estudiante:
        return self.__estudiante

    @property
    def materias(self) -> list[Materia]:
        """Retorna una copia para evitar mutaciones externas."""
        return self.__materias.copy()

    def obtener_creditos_totales(self) -> int:
        """Calcula el total de créditos inscritos."""
        return sum(m.creditos for m in self.__materias)

    def obtener_creditos_disponibles(self) -> int:
        """Calcula créditos aún disponibles."""
        return self.__estudiante.limite_creditos - self.obtener_creditos_totales()

    def inscribir_materia(self, materia: Materia) -> Resultado:
        """Intenta inscribir una materia con validaciones."""
        # Validación de tipo
        if not isinstance(materia, Materia):
            return Resultado(False, "[Error] El parámetro debe ser una instancia de Materia.")

        # Validación de duplicados
        if any(m.codigo == materia.codigo for m in self.__materias):
            return Resultado(False, f"[Error] La materia '{materia.nombre}' ya está inscrita.")

        # Validación de tope máximo de créditos
        if self.obtener_creditos_totales() + materia.creditos > self.__estudiante.limite_creditos:
            return Resultado(
                False,
                f"[Error] No se puede inscribir '{materia.nombre}'. Excede el límite de {self.__estudiante.limite_creditos} créditos."
            )

        self.__materias.append(materia)
        return Resultado(
            True,
            f"[Éxito] Inscrita: {materia.nombre} ({materia.creditos} cr). Total: {self.obtener_creditos_totales()} cr.",
            {"creditos_totales": self.obtener_creditos_totales(), "creditos_disponibles": self.obtener_creditos_disponibles()}
        )

    def cancelar_materia(self, codigo_materia: str) -> Resultado:
        """Cancela la inscripción de una materia."""
        materia_encontrada = next(
            (m for m in self.__materias if m.codigo == codigo_materia), None
        )

        if materia_encontrada:
            self.__materias.remove(materia_encontrada)
            return Resultado(
                True,
                f"[Cancelación] Se canceló '{materia_encontrada.nombre}'. Créditos actualizados: {self.obtener_creditos_totales()} cr.",
                {"creditos_totales": self.obtener_creditos_totales(), "creditos_disponibles": self.obtener_creditos_disponibles()}
            )

        return Resultado(False, f"[Error] No se encontró la materia con código '{codigo_materia}' en la inscripción.")

    def obtener_resumen(self) -> dict:
        """Retorna un resumen completo de la inscripción."""
        return {
            "estudiante": {
                "id": self.__estudiante.identificacion,
                "nombre": self.__estudiante.nombre,
                "limite_creditos": self.__estudiante.limite_creditos,
            },
            "materias": [
                {"codigo": m.codigo, "nombre": m.nombre, "creditos": m.creditos}
                for m in self.__materias
            ],
            "estadistica": {
                "total_materias": len(self.__materias),
                "creditos_inscritos": self.obtener_creditos_totales(),
                "creditos_disponibles": self.obtener_creditos_disponibles(),
            }
        }


# --- PRUEBAS DE EJECUCIÓN ---
if __name__ == "__main__":
    print("--- PRUEBAS NIVEL PROFESIONAL (MEJORADO) ---\n")

    try:
        # Instanciación
        est = Estudiante("10102030", "Laura Gómez", limite_creditos=10)
        registro = Inscripcion(est)

        m1 = Materia("POO1", "Programación Orientada a Objetos 1", 4)
        m2 = Materia("BD01", "Bases de Datos", 4)
        m3 = Materia("MAT1", "Cálculo Diferencial", 4)

        # Inscripciones con patrón Result
        resultado = registro.inscribir_materia(m1)
        print(resultado.mensaje)

        resultado = registro.inscribir_materia(m2)
        print(resultado.mensaje)

        resultado = registro.inscribir_materia(m3)  # Fallará
        print(resultado.mensaje)

        # Cancelación segura
        print()
        resultado = registro.cancelar_materia("POO1")
        print(resultado.mensaje)

        resultado = registro.inscribir_materia(m3)  # Ahora sí debe permitirlo
        print(resultado.mensaje)

        # Resumen final
        print("\n--- RESUMEN FINAL ---")
        import json
        print(json.dumps(registro.obtener_resumen(), indent=2, ensure_ascii=False))

    except (ValueError, TypeError) as e:
        print(f"✗ Error: {e}")
        