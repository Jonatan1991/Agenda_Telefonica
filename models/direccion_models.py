from utils.formateadores import capitalizar_texto

class Direccion:
    def __init__(self, calle, numero, piso, puerta, escalera, cp, provincia):
        self.calle = capitalizar_texto(calle)
        self.numero = numero
        self.piso = piso
        self.puerta = puerta
        self.escalera = escalera
        self.cp = cp
        self.provincia = capitalizar_texto(provincia)

    def to_dict(self):
        return{
            "calle": self.calle,
            "numero": self.numero,
            "piso": self.piso,
            "puerta": self.puerta,
            "escalera": self.escalera,
            "cp": self.cp,
            "provincia": self.provincia
        }
    
    @classmethod
    def from_dict(cls, datos):
        return cls(
            datos.get("calle"),
            datos.get("numero"),
            datos.get("piso"),
            datos.get("puerta"),
            datos.get("escalera"),
            datos.get("cp"),
            datos.get("provincia")
        )