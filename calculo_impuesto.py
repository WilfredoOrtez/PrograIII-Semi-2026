import math


def calcular_impuesto(balance, tarifa):
    """
    Calcula el impuesto mensual según la tarifa.

    tarifa: dict con claves:
        - desde (float)
        - precio_base (float)
        - adicional (float)
        - porcentaje (float)

    Fórmulas:
      - Si porcentaje > 0: impuesto = balance * porcentaje / 100
      - Si porcentaje == 0: impuesto = precio_base + CEIL(excedente/1000) * adicional
    """
    balance = float(balance)

    if balance <= 0:
        raise ValueError("El balance debe ser mayor que cero.")

    porcentaje = float(tarifa.get('porcentaje', 0) or 0)
    precio_base = float(tarifa.get('precio_base', 0) or 0)
    adicional = float(tarifa.get('adicional', 0) or 0)
    desde = float(tarifa.get('desde', 0) or 0)

    if porcentaje > 0:
        impuesto = balance * (porcentaje / 100.0)
    else:
        excedente = balance - desde
        if excedente <= 0:
            bloques = 0
        else:
            bloques = math.ceil(excedente / 1000.0)
        impuesto = precio_base + (bloques * adicional)

    return round(impuesto, 2)


def detalle_calculo(balance, tarifa):
    """Devuelve un dict con el detalle paso a paso para mostrar en UI."""
    balance = float(balance)
    porcentaje = float(tarifa.get('porcentaje', 0) or 0)
    precio_base = float(tarifa.get('precio_base', 0) or 0)
    adicional = float(tarifa.get('adicional', 0) or 0)
    desde = float(tarifa.get('desde', 0) or 0)

    if porcentaje > 0:
        impuesto = balance * (porcentaje / 100.0)
        return {
            'tipo': 'porcentual',
            'balance': balance,
            'porcentaje': porcentaje,
            'impuesto': round(impuesto, 2)
        }

    excedente = balance - desde
    bloques = math.ceil(excedente / 1000.0) if excedente > 0 else 0
    impuesto = precio_base + (bloques * adicional)

    return {
        'tipo': 'bloques',
        'balance': balance,
        'desde': desde,
        'precio_base': precio_base,
        'excedente': round(excedente, 2),
        'bloques': bloques,
        'adicional': adicional,
        'impuesto': round(impuesto, 2)
    }