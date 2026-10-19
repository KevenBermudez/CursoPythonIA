from dataclasses import dataclass


class Persona:
    def __init__(self, nombre: str, apellido: str, edad: int) -> None:
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad

    def __eq__(self, obj: object) -> bool:
        return isinstance(obj, Persona)

    @property
    def edad(self) -> int:
        return self.edad


class Empleado(Persona):
    def __init__(
        self, nombre: str, apellido: str, edad: int, puesto: str, cargo: str, salario: float
    ):
        super().__init__(nombre, apellido, edad)
        self.puesto = puesto
        self.cargo = cargo
        self.salario = salario


@dataclass(frozen=True)
class EmpleadoPersona:
    nombre: str
    puesto: str
    salario: float


# persona1 = Persona("Ronald", "Barrero", 35)
# empleado1 = Empleado("Keven", "Bermudez", 32, "Desarrollador", "Ingeniero", 3500000)

# persona1 == empleado1

# persona2 = EmpleadoPersona("Ruben", "Desarrollador", 4000000)
