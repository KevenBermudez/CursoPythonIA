"""Sesión 1 — Prueba diagnóstica (45 min). Implemente cada función y ejecute:

    uv run pytest diagnostico -q

Mide: tipado, colecciones, comprensiones, funciones de orden superior, generadores,
manejo de errores, dataclasses y context managers. No requiere librerías externas.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass


# 1. Comprensiones -----------------------------------------------------------
def palabras_por_longitud(texto: str) -> dict[int, list[str]]:
    """Agrupa palabras únicas (minúsculas, sin puntuación) por longitud, ordenadas."""
    texto_minuscula = texto.lower().replace(",", "").replace(".", "").strip()
    lista_palabras = texto_minuscula.split()
    grupos = {}
    for palabra in lista_palabras:
        longitud_palabra = len(palabra)
        if longitud_palabra not in grupos:
            grupos[longitud_palabra] = []
        if palabra not in grupos[longitud_palabra]:
            grupos[longitud_palabra].append(palabra)
    grupos_ordenados = {longitud: sorted(grupos[longitud]) for longitud in sorted(grupos)}
    return grupos_ordenados


# 2. Colecciones -------------------------------------------------------------
def top_n(frecuencias: Iterable[str], n: int) -> list[tuple[str, int]]:
    """Los n elementos más frecuentes; empate → orden alfabético."""
    elementos_conteo = {}
    for frecuencia in frecuencias:
        if frecuencia not in elementos_conteo:
            elementos_conteo[frecuencia] = 1
        else:
            elementos_conteo[frecuencia] += 1
    elementos_ordenados = {
        elemento: elementos_conteo[elemento] for elemento in sorted(elementos_conteo)
    }
    lista_tuplas = list(elementos_ordenados.items())
    return lista_tuplas[:n]


# 3. Funciones de orden superior / closures ----------------------------------
def reintentar(veces: int) -> Callable[[Callable[..., object]], Callable[..., object]]:
    """Decorador: reintenta la función hasta `veces` si lanza excepción; luego la propaga."""
    raise NotImplementedError


# 4. Generadores -------------------------------------------------------------
def en_lotes[T](items: Iterable[T], tamano: int) -> Iterator[list[T]]:
    """Entrega listas de `tamano` elementos (la última puede ser menor). Perezoso."""
    raise NotImplementedError


# 5. Dataclasses + propiedades -----------------------------------------------
@dataclass
class Factura:
    subtotal: float
    iva: float = 0.19

    @property
    def total(self) -> float:
        raise NotImplementedError

    def __post_init__(self) -> None:
        """Debe lanzar ValueError si subtotal < 0 o iva fuera de [0, 1]."""
        raise NotImplementedError


# 6. Context managers --------------------------------------------------------
class Cronometro:
    """with Cronometro() as c: ...  → c.segundos tiene la duración del bloque."""

    def __enter__(self) -> Cronometro:
        raise NotImplementedError

    def __exit__(self, *exc: object) -> None:
        raise NotImplementedError
