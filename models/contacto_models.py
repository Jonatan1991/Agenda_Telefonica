class Contacto:
    def __init__(self, nombre, telefono, email, direccion):
        self.nombre =nombre
        self.telefono = telefono
        self.email = email
        self.direccion = direccion

    def to_dict(self):
        """Convierte el objeto en diccionario para guardarlo en JSON."""
        return {
            "nombre": self.nombre,
            "telefono": self.telefono,
            "email": self.email,
            "direccion": self.direccion
        }

    @classmethod
    def from_dict(cls, datos):
        """Crea un objeto Contacto a partir de un diccionario."""
        return cls(
            datos.get("nombre"),
            datos.get("telefono"),
            datos.get("email"),
            datos.get("direccion", {})
        )