import json
import os

from utils.validaciones import validar_email, validar_nombre, validar_telefono, validar_apellido
from models.contacto_models import Contacto

# ============================================================
# CLASE PRINCIPAL: AgendaTelefonica
# ============================================================
# Esta clase encapsula TODA la lógica del programa.
# Es responsable de:
# - Mantener los contactos en memoria
# - Cargar y guardar el archivo JSON
# - Gestionar IDs únicos
# - Crear, leer, editar y eliminar contactos
# ============================================================

class AgendaTelefonica:
    # --------------------------------------------------------
    # Constructor de la clase
    # Se ejecuta automáticamente al crear la agenda
    # --------------------------------------------------------
    def __init__(self, archivo_datos="data/bd_agenda.json"):
        # Ruta del archivo donde se guardan los contactos
        self.archivo_datos = archivo_datos

        # Diccionario principal de contactos en memoria
        self.contactos = {}
        
        # Último ID usado (sirve para generar el siguiente)
        self.ultimo_id = 0

        # Cargamos los datos al iniciar la app
        self.cargar_contactos()

    
    # ========================================================
    # MÉTODOS DE PERSISTENCIA (JSON)
    # ========================================================
    def cargar_contactos(self):
        """Carga los contactos desde el archivo JSON.
        Si no existe, crea una agenda vacía y resetea el contador de IDs.
        """
        if not os.path.exists(self.archivo_datos):
            self.contactos = {}
            self.ultimo_id = 0
            return
    
        # with open garantiza que el archivo se cierre correctamente al finalizar la operación
        with open(self.archivo_datos, "r", encoding="utf-8") as archivo:
            try:
                self.contactos = json.load(archivo)
                # Calculamos el último ID usado
                self.ultimo_id = self._obtener_ultimo_id()
            except json.JSONDecodeError:
                # Si el archivo está corrupto o vacío
                self.contactos = {}
                self.ultimo_id = 0
        
    def guardar(self):
        """
        Guarda los contactos actuales en el archivo JSON.
        Se llama automáticamente después de cada cambio.
        """
        with open(self.archivo_datos, "w", encoding="utf-8") as archivo:
            json.dump(self.contactos, archivo, indent=4, ensure_ascii=False)

    def _obtener_ultimo_id(self):
        """
        Método interno que obtiene el ID más alto existente.
        Sirve para continuar numerando sin repetir IDs.
        """
        if not self.contactos:
            return 0
        # Convertimos las claves a número para compararlas
        return max(int(i) for i in self.contactos.keys())
    

    #_______CRUD_________

    # def agregar_contacto(self, nombre, telefono, email, direccion):
    def agregar_contacto(self, contacto: Contacto):
        """Añade un nuevo contacto. `direccion` es un diccionario.
        Ejemplo de `direccion`: {"calle": ..., "numero": ..., "municipio": ..., "cp": ...}
        """
        self.ultimo_id += 1
        id_contacto = str(self.ultimo_id)

        contacto.nombre = validar_nombre(contacto.nombre)
        contacto.apellido_1 = validar_apellido(contacto.apellido_1)
        contacto.apellido_2 = validar_apellido(contacto.apellido_2)
        if contacto.info_contactos:
            contacto.info_contactos.telefono_1 = validar_telefono(contacto.info_contactos.telefono_1) if contacto.info_contactos.telefono_1 else None
            contacto.info_contactos.telefono_2 = validar_telefono(contacto.info_contactos.telefono_2) if contacto.info_contactos.telefono_2 else None
            contacto.info_contactos.telefono_3 = validar_telefono(contacto.info_contactos.telefono_3) if contacto.info_contactos.telefono_3 else None
            contacto.info_contactos.telefono_4 = validar_telefono(contacto.info_contactos.telefono_4) if contacto.info_contactos.telefono_4 else None
            contacto.info_contactos.email = validar_email(contacto.info_contactos.email) if contacto.info_contactos.email else None

        self.contactos[id_contacto] = contacto.to_dict()

        # Guardamos cambios
        self.guardar()
        return id_contacto

    def agregar_contacto_sin_validaciones(self, contacto: Contacto):
        """Añade un nuevo contacto sin aplicar validaciones (usado para importación)."""
        self.ultimo_id += 1
        id_contacto = str(self.ultimo_id)

        # Guardar el contacto sin validaciones
        self.contactos[id_contacto] = contacto.to_dict()

        # Guardamos cambios
        self.guardar()
        return id_contacto

    def buscar_por_nombre(self, nombre):
        """Devuelve un diccionario con los contactos cuyo nombre contiene el texto dado."""
        nombre = nombre.lower()
        resultados = {}
        for id_contacto, datos in self.contactos.items():
            if nombre in datos.get("nombre", "").lower():
                resultados[id_contacto] = datos
        return resultados

    def obtener_todos(self):
        """Devuelve todos los contactos."""
        return self.contactos

    def mostrar_contactos(self, contactos=None):
        """Imprime una lista de contactos. Si `contactos` es None, muestra todos."""
        if contactos is None:
            contactos = self.contactos

        if not contactos:
            print("La agenda está vacía o no hay coincidencias.")
            return
        
        print("\nLista de contactos")
        print("-" * 30)

        for id, datos in contactos.items():
            print(f"ID: {id}")
            print(f"Nombre: {datos.get('nombre', '')}")
            print(f"Apellido 1: {datos.get('apellido_1', '')}")
            print(f"Apellido 2: {datos.get('apellido_2', '')}")
            # print(f"Teléfono: {datos.get('telefono', '')}")
            # print(f"Email: {datos.get('email', '')}")
            print("Dirección:")
            dir_ = datos.get('direccion', {})
            print(f"  Calle: {dir_.get('calle', '')}")
            print(f"  Número: {dir_.get('numero', '')}")
            print(f"  Piso: {dir_.get('piso', '')}")
            print(f"  Puerta: {dir_.get('puerta', '')}")
            print(f"  Escalera: {dir_.get('escalera', '')}")
            print(f"  CP: {dir_.get('cp', '')}")
            print(f"  Provincia: {dir_.get('provincia', '')}")
            print("-" * 30)
            print('Datos de contacto:')
            info_ = datos.get('info_contactos', {})
            print(f"  Email: {info_.get('email', '')}")
            print(f"  Teléfono 1: {info_.get('telefono_1', '')}")
            print(f"  Nota 1: {info_.get('nota_1', '')}")
            print(f"  Teléfono 2: {info_.get('telefono_2', '')}")
            print(f"  Nota 2: {info_.get('nota_2', '')}")
            print(f"  Teléfono 3: {info_.get('telefono_3', '')}")
            print(f"  Nota 3: {info_.get('nota_3', '')}")
            print(f"  Teléfono 4: {info_.get('telefono_4', '')}")
            print(f"  Nota 4: {info_.get('nota_4', '')}")
            print(f"  Observaciones: {info_.get('observaciones', '')}")
            print(f"  Auxiliar: {info_.get('auxiliar', '')}")


    def editar_contacto(self, id_contacto, contacto: Contacto):
        """Edita un contacto existente.
        Reemplaza el contacto completo con el objeto Contacto proporcionado.
        """
        if id_contacto not in self.contactos:
            return False

        # Validar los campos del contacto
        contacto.nombre = validar_nombre(contacto.nombre)
        contacto.apellido_1 = validar_apellido(contacto.apellido_1)
        contacto.apellido_2 = validar_apellido(contacto.apellido_2)
        # contacto.telefono = validar_telefono(contacto.telefono)
        # contacto.email = validar_email(contacto.email)
        if contacto.info_contactos:
            contacto.info_contactos.telefono_1 = validar_telefono(contacto.info_contactos.telefono_1) if contacto.info_contactos.telefono_1 else None
            contacto.info_contactos.telefono_2 = validar_telefono(contacto.info_contactos.telefono_2) if contacto.info_contactos.telefono_2 else None
            contacto.info_contactos.telefono_3 = validar_telefono(contacto.info_contactos.telefono_3) if contacto.info_contactos.telefono_3 else None
            contacto.info_contactos.telefono_4 = validar_telefono(contacto.info_contactos.telefono_4) if contacto.info_contactos.telefono_4 else None
            contacto.info_contactos.email = validar_email(contacto.info_contactos.email) if contacto.info_contactos.email else None

        # Reemplazar el contacto completo
        self.contactos[id_contacto] = contacto.to_dict()

        self.guardar()
        return True


    def eliminar_contacto(self, id_contacto):
        """Elimina un contacto por ID."""
        if id_contacto not in self.contactos:
            return False

        del self.contactos[id_contacto]
        self.guardar()
        return True

