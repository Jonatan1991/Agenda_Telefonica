from models.direccion_models import Direccion
from models.contacto_info_models import InfoContactos

class Contacto:
    def __init__(self, nombre, apellido_1, apellido_2, direccion, info_contactos=None):
        self.nombre = nombre
        self.apellido_1 = apellido_1
        self.apellido_2 = apellido_2
        if isinstance(direccion, dict):
            direccion = Direccion.from_dict(direccion)
        self.direccion = direccion
        if isinstance(info_contactos, dict):
            info_contactos = InfoContactos.from_dict(info_contactos)
        self.info_contactos = info_contactos


    def to_dict(self):
        """Convierte el objeto en diccionario para guardarlo en JSON."""
        return {
            "nombre": self.nombre,
            "apellido_1": self.apellido_1,
            "apellido_2": self.apellido_2,

            "direccion": self.direccion.to_dict() if self.direccion else None,
            "info_contactos": self.info_contactos.to_dict() if self.info_contactos else None
        }

    @classmethod
    def from_dict(cls, datos):
        """Crea un objeto Contacto a partir de un diccionario."""
        return cls(
            datos.get("nombre"),
            datos.get("apellido_1"),
            datos.get("apellido_2"),

            Direccion.from_dict(datos.get("direccion", {})) if datos.get("direccion") else None,
            InfoContactos.from_dict(datos.get("info_contactos", {})) if datos.get("info_contactos") else None
        )