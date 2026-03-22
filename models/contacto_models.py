from models.direccion_models import Direccion

class Contacto:
    def __init__(self, nombre, apellido_1, apellido_2, telefono, email, direccion):
        self.nombre =nombre
        self.apellido_1 =apellido_1
        self.apellido_2 =apellido_2
        self.telefono = telefono
        self.email = email
        if isinstance(direccion, dict):
            direccion = Direccion.from_dict(direccion)
        self.direccion = direccion

    def to_dict(self):
        """Convierte el objeto en diccionario para guardarlo en JSON."""
        return {
            "nombre": self.nombre,
            "apellido_1": self.apellido_1,
            "apellido_2": self.apellido_2,
            "telefono": self.telefono,
            "email": self.email,
            "direccion": self.direccion.to_dict() if self.direccion else None
        }

    @classmethod
    def from_dict(cls, datos):
        """Crea un objeto Contacto a partir de un diccionario."""
        return cls(
            datos.get("nombre"),
            datos.get("apellido_1"),
            datos.get("apellido_2"),
            datos.get("telefono"),
            datos.get("email"),
            Direccion.from_dict(datos.get("direccion", {})) if datos.get("direccion") else None
        )