from models.agenda_models import AgendaTelefonica

class AgendaController:

    def __init__(self):
        self.agenda = AgendaTelefonica()

    def agregar_contacto(self, nombre, telefono, email, direccion):
        return self.agenda.agregar_contacto(nombre, telefono, email, direccion)
        
    def obtener_contactos(self):
        return self.agenda.obtener_todos()
        
    def buscar_contacto(self, nombre):
        return self.agenda.buscar_por_nombre(nombre)
        
    def editar_contacto(self, id_contacto, **datos):
        return self.agenda.editar_contacto(id_contacto, **datos)
        
    def eliminar_contacto(self, id_contacto):
        return self.agenda.eliminar_contacto(id_contacto)