"""Reglas compartidas: ninguna validación convierte un dato inválido en válido."""

from decimal import Decimal, InvalidOperation  # Evita errores binarios en cálculos monetarios.

from .excepciones import ValidacionError  # Usa errores propios en lugar de fallas sin controlar.


def texto(valor, campo):
    """Acepta únicamente una cadena no vacía, sin saltos de línea."""
    if not isinstance(valor, str) or not valor.strip() or not valor.isprintable():  # Valida formato.
        raise ValidacionError(f"{campo}: debe ser un texto no vacío y sin caracteres de control.")
    return valor.strip()  # Elimina espacios externos.


def numero(valor, campo, minimo=Decimal("0"), incluir_minimo=False, maximo=None):
    """Valida números finitos; los límites se expresan en Decimal."""
    if isinstance(valor, bool) or not isinstance(valor, (int, float, str, Decimal)):  # Rechaza bool.
        raise ValidacionError(f"{campo}: debe ser un número.")  # Evita True como duración o precio.
    try:  # La conversión puede fallar con cadenas como 'dos'.
        resultado = Decimal(str(valor))  # Conserva la representación decimal de entrada.
    except (InvalidOperation, ValueError) as causa:  # Captura la conversión inválida.
        raise ValidacionError(f"{campo}: no se pudo convertir a número.") from causa  # Encadena causa.
    if not resultado.is_finite():  # Impide NaN e infinitos en los cálculos.
        raise ValidacionError(f"{campo}: debe ser finito.")  # Mantiene costos comparables.
    if resultado < minimo or (resultado == minimo and not incluir_minimo):  # Aplica límite inferior.
        if incluir_minimo:  # Distingue si se permite un valor igual al límite.
            comparador = "mayor o igual que"  # Describe un límite que incluye la igualdad.
        else:  # En los demás casos se exige superar el límite.
            comparador = "mayor que"  # Describe un límite estricto.
        raise ValidacionError(f"{campo}: debe ser {comparador} {minimo}.")  # Informa el límite.
    if maximo is not None and resultado > maximo:  # Aplica límite superior, si existe.
        raise ValidacionError(f"{campo}: no puede superar {maximo}.")  # Rechaza exceso.
    return resultado  # Entrega un Decimal ya validado.


def entero_positivo(valor, campo):
    """Rechaza fracciones sin truncarlas silenciosamente."""
    resultado = numero(valor, campo)  # Primero valida número positivo y finito.
    if resultado != resultado.to_integral_value():  # Detecta partes decimales.
        raise ValidacionError(f"{campo}: debe ser un número entero.")  # No redondea capacidades.
    return int(resultado)  # Convierte únicamente después de validar.
