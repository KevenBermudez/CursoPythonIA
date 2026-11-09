"""Fundamentos 1: tipos y contenedores (sesión 1, unos 40 min). Implemente cada función y ejecute:

    uv run pytest fundamentos/test_s01_tipos.py -q

Las pruebas son la especificación: léalas antes de empezar. Solo biblioteca estándar.
"""

from __future__ import annotations

import ast
import copy
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation


# 1. Texto -------------------------------------------------------------------
def limpiar_etiquetas(texto: str) -> list[str]:
    """'Legal, RRHH ,, legal' → ['legal', 'rrhh'].

    Separa por comas, quita espacios, pasa a minúsculas (casefold), descarta vacías
    y elimina repetidas conservando el orden de la primera aparición.
    """
    labels = (e.strip().casefold() for e in texto.split(","))
    return list(dict.fromkeys(e for e in labels if e))


# 2. Números y dinero --------------------------------------------------------
def total_con_iva(precios: list[str], iva: str = "0.19") -> Decimal:
    """Suma precios escritos como texto y aplica el IVA.

    Redondea a 2 decimales, con la mitad hacia arriba.

    Lanza ValueError si algún precio no es un número válido o es negativo.
    """
    try:
        valor_iva = Decimal(iva)
    except InvalidOperation as err:
        raise ValueError("El IVA proporcionado no es un número válido.") from err

    suma_precios = Decimal("0")
    for p in precios:
        try:
            valor_precio = Decimal(p.strip())
        except InvalidOperation as err:
            raise ValueError(f"'{p!r}' no es un número válido.") from err
        if not valor_precio.is_finite() or valor_precio < 0:
            raise ValueError(f"El precio no puede ser negativo: {valor_precio!r}")

        suma_precios += valor_precio

    total = suma_precios * (1 + valor_iva)
    return total.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)


# 3. Validar entradas (código seguro) ----------------------------------------
def parsear_limite(valor: str | None, *, defecto: int = 5, maximo: int = 50) -> int:
    """Convierte el parámetro 'limite' que llega de una petición.

    None o texto vacío → defecto. Texto que no es entero → ValueError.
    Fuera de 1..maximo → ValueError. Ojo: "0" es un valor explícito, no vacío.
    """
    if valor is None or not valor.strip():
        return defecto
    try:
        valor_entero = int(valor)
    except ValueError as err:
        raise ValueError("El valor debbe ser un entero") from err
    if not 1 <= valor_entero <= maximo:
        raise ValueError(f"El valor debe estar entre 1 y {maximo}")
    return valor_entero


# 4. Datos, no código (código seguro) ----------------------------------------
def leer_lista_enteros(texto: str) -> list[int]:
    """'[1, 2, 3]' → [1, 2, 3], sin usar eval.

    Lanza ValueError si el texto no es una lista o si algún elemento no es entero
    (los booleanos tampoco cuentan como enteros).
    """
    try:
        lista = ast.literal_eval(texto)
    except (ValueError, SyntaxError) as err:
        raise ValueError("El texto no tiene un formato de lista válido.") from err
    if not isinstance(lista, list):
        raise ValueError("El texto proporcionado no representa una lista.")
    if not all(type(x) is int for x in lista):
        raise ValueError("No todos los datos de la lista son enteros")
    return lista


# 5. Diccionarios y conjuntos ------------------------------------------------
def indice_invertido(docs: dict[str, str]) -> dict[str, set[str]]:
    """Cada palabra (en minúsculas, separada por espacios) apunta a los ids que la contienen.

    {'d1': 'Vacaciones anuales', 'd2': 'vacaciones'}
    → {'vacaciones': {'d1', 'd2'}, 'anuales': {'d1'}}
    """
    indice: dict[str, set[str]] = {}
    for id_doc, text in docs.items():
        for p in text.lower().split():
            indice.setdefault(p, set()).add(id_doc)
    return indice


# 6. Copias y mutabilidad ----------------------------------------------------
def fusionar_config(base: dict[str, object], *capas: dict[str, object]) -> dict[str, object]:
    """Une configuraciones anidadas: cada capa sobrescribe a la anterior, clave por clave.

    Si en ambas un valor es dict, se fusionan recursivamente. No debe modificar
    `base` ni las capas, ni compartir con ellas diccionarios anidados.
    """
    resultado = copy.deepcopy(base)
    for capa in capas:
        for clave, valor in capa.items():
            actual = resultado.get(clave)
            if isinstance(actual, dict) and isinstance(valor, dict):
                resultado[clave] = fusionar_config(actual, valor)
            else:
                resultado[clave] = copy.deepcopy(valor)
    return resultado
