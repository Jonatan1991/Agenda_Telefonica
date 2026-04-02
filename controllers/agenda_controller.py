from models.agenda_models import AgendaTelefonica
from models.contacto_models import Contacto

from controllers.import_controller import ImportController

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
    
    def importar_contactos_excel(self, ruta_archivo):
        """
        Importa contactos desde un archivo Excel y los agrega a la agenda.
        
        Args:
            ruta_archivo (str): Ruta al archivo Excel
            
        Returns:
            dict: Resultados de la importación
        """
        import_controller = ImportController()
        contactos, errores, estadisticas = import_controller.importar_excel(ruta_archivo)
        
        # Agregar contactos importados a la agenda
        contactos_agregados = 0
        errores_agregado = []
        
        for contacto in contactos:
            try:
                self.agenda.agregar_contacto_sin_validaciones(contacto)
                contactos_agregados += 1
            except Exception as e:
                errores_agregado.append(f"Error al agregar {contacto.nombre}: {str(e)}")
        
        return {
            'contactos_importados': contactos_agregados,
            'errores_importacion': errores,
            'errores_agregado': errores_agregado,
            'estadisticas': estadisticas
        }