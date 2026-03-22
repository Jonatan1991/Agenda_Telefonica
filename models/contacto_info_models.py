from utils.formateadores import capitalizar_texto

class InfoContactos:
    def __init__(self, email, telefono_1, telefono_2, telefono_3, telefono_4, nota_1, nota_2, nota_3, nota_4, observaciones, auxiliar, ):
        self.email = email
        self.telefono_1 = telefono_1
        self.telefono_2 = telefono_2
        self.telefono_3 = telefono_3
        self.telefono_4 = telefono_4
        self.nota_1 = nota_1
        self.nota_2 = nota_2
        self.nota_3 = nota_3
        self.nota_4 = nota_4
        self.observaciones = observaciones
        self.auxiliar = auxiliar

    def to_dict(self):
        return {
            "email": self.email,
            "telefono_1": self.telefono_1,
            "telefono_2": self.telefono_2,
            "telefono_3": self.telefono_3,
            "telefono_4": self.telefono_4,
            "nota_1": self.nota_1,
            "nota_2": self.nota_2,
            "nota_3": self.nota_3,
            "nota_4": self.nota_4,
            "observaciones": self.observaciones,
            "auxiliar": self.auxiliar
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get("email"),
            data.get("telefono_1"),
            data.get("telefono_2"),
            data.get("telefono_3"),
            data.get("telefono_4"),
            data.get("nota_1"),
            data.get("nota_2"),
            data.get("nota_3"),
            data.get("nota_4"),
            data.get("observaciones"),
            data.get("auxiliar")

        )