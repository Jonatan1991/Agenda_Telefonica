import re

def normalizar_telefono(telefono):
    """
    ELimina espacios, guiones y parentesis del telefono.
    """

    telefono = telefono.strip()
    telefono = re.sub(r"[ \-()]", "", telefono)
    return telefono