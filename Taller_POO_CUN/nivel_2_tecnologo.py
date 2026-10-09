from abc import ABC, abstractmethod
from typing import List

class Vehiculo(ABC):
    """Clase abstracta base para vehículos."""
    
    # Constantes
    TARIFA_BASE_AUTOMOVIL = 11500.0
    TARIFA_BASE_MOTO = 6200.0
    TARIFA_BASE_CAMION = 18000.0
    TARIFA_EJE_ADICIONAL_CAMION = 7000.0

    def __init__(self, placa: str):
        if not placa or not isinstance(placa, str):
            raise ValueError("[Error] La placa debe ser una cadena no vacía")
        self.__placa = placa

    @property
    def placa(self) -> str:
        return self.__placa

    @abstractmethod
    def calcular_peaje(self) -> float:
        """Método abstracto a ser implementado por subclases."""
        pass


class Automovil(Vehiculo):
    """Vehículo de 4 ruedas."""

    def calcular_peaje(self) -> float:
        return self.TARIFA_BASE_AUTOMOVIL


class Moto(Vehiculo):
    """Vehículo de 2 ruedas."""

    def calcular_peaje(self) -> float:
        return self.TARIFA_BASE_MOTO


class Camion(Vehiculo):
    """Vehículo de carga con múltiples ejes."""

    def __init__(self, placa: str, ejes: int):
        super().__init__(placa)
        if not isinstance(ejes, int) or ejes < 2:
            raise ValueError("[Error] Un camión debe tener al menos 2 ejes.")
        self.__ejes = ejes

    @property
    def ejes(self) -> int:
        return self.__ejes

    def calcular_peaje(self) -> float:
        ejes_adicionales = self.__ejes - 2
        return (self.TARIFA_BASE_CAMION + 
                (ejes_adicionales * self.TARIFA_EJE_ADICIONAL_CAMION))


# --- PRUEBAS DE EJECUCIÓN Y POLIMORFISMO ---
if __name__ == "__main__":
    print("--- PRUEBAS NIVEL TECNÓLOGO (MEJORADO) ---\n")

    try:
        # Lista polimórfica de vehículos
        estacion_peaje: List[Vehiculo] = [
            Automovil("CUN-123"),
            Moto("MTO-999"),
            Camion("CAM-456", ejes=4),  # 2 ejes base + 2 adicionales
            Camion("CAM-789", ejes=2),
        ]

        recaudo_total = 0.0

        for vehiculo in estacion_peaje:
            valor = vehiculo.calcular_peaje()
            recaudo_total += valor
            print(
                f"Placa: {vehiculo.placa:12} | Tipo: {type(vehiculo).__name__:10} | "
                f"Peaje: ${valor:>10,.2f}"
            )

        print(f"\n{'─' * 60}")
        print(f"Recaudo Total Estación: ${recaudo_total:,.2f}")
        print(f"{'─' * 60}")

        # Prueba de error
        print("\nIntentando crear vehículo inválido...")
        invalid = Camion("INVALID", ejes=1)  # ← Lanzará excepción

    except ValueError as e:
        print(f"✗ {e}")
    except Exception as e:
        print(f"✗ Error inesperado: {e}")
        