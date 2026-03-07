import re
from utils.formateadores import normalizar_telefono

# ==========================================
# VALIDACIONES DE LA AGENDA
# ==========================================

def validar_nombre(nombre):
    """Valida que el nombre tenga al menos 2 caracteres."""
    
    if not nombre or len(nombre.strip()) < 2:
        raise ValueError("El nombre debe tener al menos 2 caracteres")
    
    return nombre.strip()


def validar_telefono(telefono):
    """
    Valida que el teléfono tenga entre 9 y 15 dígitos. 
    y lo formateamos para que todos tengan el mismo formato
    """

    telefono = normalizar_telefono(telefono)

    if telefono.startswith("+"):
        numero = telefono[1:]
    else:
        numero = telefono

    if not telefono.isdigit():
        raise ValueError("El teléfono solo puede contener números")

    if len(numero) < 9 or len(numero) > 15:
        raise ValueError("El teléfono debe tener entre 9 y 15 dígitos")

    return telefono

    return telefono


def validar_email(email):
    """Valida el formato de un email."""

    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if not re.match(patron, email):
        raise ValueError("Escriba un email válido, ej: correo@dominio.com")

    return email