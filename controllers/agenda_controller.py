from models.agenda_models import AgendaTelefonica
from models.contacto_models import Contacto

class AgendaController:

    def __init__(self):
        self.agenda = AgendaTelefonica()

    # def agregar_contacto(self, nombre, telefono, email, direccion):
    def agregar_contacto(self, contacto: Contacto):
        return self.agenda.agregar_contacto(contacto)
        
    def obtener_contactos(self):
        return self.agenda.obtener_todos()
        
    def buscar_contacto(self, nombre):
        return self.agenda.buscar_por_nombre(nombre)
        
    def editar_contacto(self, id_contacto, contacto: Contacto):
        return self.agenda.editar_contacto(id_contacto, contacto)
        
    def eliminar_contacto(self, id_contacto):
        return self.agenda.eliminar_contacto(id_contacto)