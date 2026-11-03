"""Práctica de la introducción a Python.

Cada función tiene su firma, una docstring con lo que debe hacer y `raise NotImplementedError`.
Reemplace esa línea por la implementación y ejecute, desde la raíz del proyecto:

    uv run pytest introduccion -v          # todas
    uv run pytest introduccion -k saludo   # solo las de un ejercicio

Los ejercicios siguen el orden de la presentación "Python para quien ya programa".
"""

from __future__ import annotations

import functools  # noqa: F401  (lo necesita el ejercicio 12)
import math  # noqa: F401  (lo necesita el ejercicio 8)
from collections.abc import Callable, Iterator
from dataclasses import dataclass


# 1. Un programa es un archivo ----------------------------------------------------------
def saludo(nombre: str, formal: bool = False) -> str:
    """Saludo para `nombre`, sin los espacios que traiga a los lados.

    saludo("Ana") → "Hola, Ana"        saludo("Ana", formal=True) → "Buenos días, Ana."
    Pista: f-strings y el método strip.
    """
    nombre = nombre.strip()
    return f"Buenos días, {nombre}." if formal else f"Hola, {nombre}"


def main() -> None:
    """Imprime saludo("mundo"). Al final del archivo ya está el bloque
    `if __name__ == "__main__":` que la llama: pruebe `uv run python introduccion/intro.py`.
    """
    print(saludo("mundo"))

    try:
        product1 = Producto("Portatil", 100000.15)
        print(f"Producto 1: {product1.nombre} - {product1.precio_con_iva}")
        # product2 = Producto("Teclado", -500000)
    except ValueError as e:
        print(f"Error: {e!r}")

    @en_mayusculas
    def presentar(nombre: str, cargo: str = "analista") -> str:
        """Presenta a una persona."""
        return f"{nombre}, {cargo}"

    print(presentar("luis", cargo="gerente"))


# 2. Bloques y condiciones --------------------------------------------------------------
def clasificar_temperatura(t: float) -> str:
    """Clasifica la temperatura de un modelo de IA.

    Menor que 0.3 → "precisa"; de 0.3 a 1 (incluido) → "equilibrada"; mayor que 1 → "creativa".
    Si es negativa o mayor que 2: ValueError.
    """
    if t < 0 or t > 2:
        raise ValueError(f"Temperatura incorrecta: {t}")
    if t < 0.3:
        return "precisa"
    elif t >= 0.3 and t <= 1:
        return "equilibrada"
    return "creativa"


# 3. Recorrer y contar ------------------------------------------------------------------
def contar_vocales(texto: str) -> dict[str, int]:
    """Cuántas veces aparece cada vocal (a, e, i, o, u), sin importar mayúsculas.

    Siempre devuelve las cinco claves, aunque alguna valga 0. El texto viene sin tildes.
    contar_vocales("Hola Mundo") → {"a": 1, "e": 0, "i": 0, "o": 2, "u": 1}
    """
    contador_vocales = {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0}
    for letra in texto.lower():
        if letra in contador_vocales:
            contador_vocales[letra] += 1
    return contador_vocales


# 4. Funciones que devuelven varios valores ---------------------------------------------
def resumen(numeros: list[float]) -> tuple[float, float, float]:
    """(mínimo, máximo, promedio) de la lista. Lista vacía: ValueError.

    resumen([4, 1, 7]) → (1, 7, 4.0)
    """
    if not numeros:
        raise ValueError("Lista de números vacia")
    return min(numeros), max(numeros), sum(numeros) / len(numeros)


# 5. Al llamar, se pasa el objeto -------------------------------------------------------
def agregar_etiqueta(etiquetas: list[str] | None, nueva: str) -> list[str]:
    """Una lista con las etiquetas y `nueva` al final, si no estaba ya.

    No modifica la lista que recibe: devuelve otra. Con None, empieza de una lista vacía.
    agregar_etiqueta(["rrhh"], "legal") → ["rrhh", "legal"]
    """
    # base = [] if etiquetas is None else etiquetas.copy()
    # base = [] if etiquetas is None else list(etiquetas)
    # base = [] if etiquetas is None else etiquetas[:]

    # base = [] if etiquetas is None else list(etiquetas)
    # if nueva not in base:
    #     base.append(nueva)
    # return base
    if etiquetas is None:
        etiquetas = []
    lista_etiquetas = [etiqueta for etiqueta in etiquetas]
    if nueva not in lista_etiquetas:
        lista_etiquetas.append(nueva)
    return lista_etiquetas


# 6. Comprensiones ----------------------------------------------------------------------
def largos(palabras: list[str]) -> dict[str, int]:
    """Diccionario palabra → largo, sin las palabras vacías o de solo espacios.

    Con una comprensión de diccionario. largos(["sol", "", "luna"]) → {"sol": 3, "luna": 4}
    """
    diccionario = {palabra: len(palabra) for palabra in palabras if palabra.strip()}
    return diccionario


# 7. Errores ----------------------------------------------------------------------------
def a_entero(texto: str, defecto: int = 0) -> int:
    """El entero que representa el texto, o `defecto` si no es un entero válido.

    a_entero(" 7 ") → 7     a_entero("4.2") → 0     a_entero("x", defecto=-1) → -1
    Pista: try / except ValueError.
    """
    try:
        texto = texto.strip()
        valor = int(texto)
        return valor
    except ValueError:
        return defecto


# 8. Módulos de la biblioteca estándar --------------------------------------------------
def hipotenusa(a: float, b: float) -> float:
    """La hipotenusa de un triángulo rectángulo, redondeada a 2 decimales.

    Use math.sqrt (el import ya está arriba). hipotenusa(1, 1) → 1.41
    """
    return round(math.sqrt(a**2 + b**2), 2)


# 9. Clases -----------------------------------------------------------------------------
class Contador:
    """Contador que solo sube.

    Contador() empieza en 0; Contador(10), en 10. `valor` se lee como atributo (una property)
    y no se puede asignar. incrementar(paso=1) suma; con paso <= 0, ValueError. reiniciar()
    vuelve a 0. repr(c) → "Contador(6)".
    """

    def __init__(self, inicio: int = 0) -> None:
        self._contador = inicio

    @property
    def valor(self) -> int:
        return self._contador

    def incrementar(self, paso: int = 1) -> None:
        if paso <= 0:
            raise ValueError("EL número del paso no puede ser menor o igual a 0")
        self._contador += paso

    def reiniciar(self) -> None:
        self._contador = 0

    def __repr__(self) -> str:
        return f"Contador({self._contador})"


# 10. dataclass -------------------------------------------------------------------------
@dataclass(frozen=True)
class Producto:
    """Producto inmutable. Precio negativo: ValueError al crearlo.

    `precio_con_iva` es una property: el precio por 1.19, redondeado a 2 decimales.
    """

    nombre: str
    precio: float
    etiquetas: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.precio < 0:
            raise ValueError("El precio no puede ser negativo.")

    @property
    def precio_con_iva(self) -> float:
        return round(self.precio * 1.19, 2)


# 11. Generadores -----------------------------------------------------------------------
def lineas_numeradas(texto: str) -> Iterator[str]:
    """Genera "1: texto", "2: texto"… por cada línea no vacía, sin espacios a los lados.

    Las líneas vacías no se cuentan. Debe ser un generador (yield), no devolver una lista.
    list(lineas_numeradas("a\\n\\n b ")) → ["1: a", "2: b"]
    """
    contador = 0
    for linea in texto.splitlines():
        linea = linea.strip()
        if linea:
            contador += 1
            yield f"{contador}: {linea}"


# 12. Decoradores -----------------------------------------------------------------------
def en_mayusculas(funcion: Callable[..., str]) -> Callable[..., str]:
    """Decorador: la función decorada devuelve su resultado en mayúsculas.

    Debe aceptar cualquier argumento (*args, **kwargs) y conservar el nombre y la docstring
    de la original con functools.wraps (el import ya está arriba).
    """

    @functools.wraps(funcion)
    def envoltura(*args, **kwargs):
        valor = funcion(*args, **kwargs)
        return valor.upper()

    envoltura.valor = ""
    return envoltura


if __name__ == "__main__":
    main()
