import re

def normalizar_telefono(telefono):
    """
    ELimina espacios, guiones y parentesis del telefono.
    """

    telefono = telefono.strip()
    telefono = re.sub(r"[ \-()]", "", telefono)
    return telefono

def capitalizar_texto(texto):
    """
    capitalizar el texto
    """
    texto = texto.strip()
    return texto.title()

