class Producto:

    def __init__(self, codigo: str, nombre: str, precio: float, stock: int):
        self.__codigo = codigo
        self.__nombre = ""
        self.__precio = 0.0
        self.__stock = 0

        # Validaciones mediante setters
        self.set_nombre(nombre)
        self.set_precio(precio)
        self.set_stock(stock)

    # Getters
    def get_codigo(self) -> str:
        return self.__codigo

    def get_nombre(self) -> str:
        return self.__nombre

    def get_precio(self) -> float:
        return self.__precio

    def get_stock(self) -> int:
        return self.__stock

    # Setters con validaciones
    def set_nombre(self, nuevo_nombre: str):
        if not nuevo_nombre or not isinstance(nuevo_nombre, str):
            raise ValueError("[Error] El nombre debe ser una cadena no vacía")
        self.__nombre = nuevo_nombre

    def set_precio(self, nuevo_precio: float):
        if nuevo_precio < 0:
            raise ValueError(f"[Error] El precio no puede ser negativo: ${nuevo_precio}")
        self.__precio = nuevo_precio

    def set_stock(self, nuevo_stock: int):
        if nuevo_stock < 0:
            raise ValueError(f"[Error] El stock no puede ser negativo: {nuevo_stock}")
        self.__stock = nuevo_stock

    # Lógica de negocio
    def vender(self, cantidad: int) -> float:
        if cantidad <= 0:
            raise ValueError("[Error] La cantidad a vender debe ser mayor a cero.")

        if cantidad > self.__stock:
            raise ValueError(
                f"[Error] Stock insuficiente. Disponible: {self.__stock}, Solicitado: {cantidad}"
            )

        self.__stock -= cantidad
        monto_venta = cantidad * self.__precio
        print(
            f"[Éxito] Venta realizada: {cantidad} x {self.get_nombre()}. Stock restante: {self.__stock}"
        )
        return monto_venta
    