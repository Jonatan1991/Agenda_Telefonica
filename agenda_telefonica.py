import json
import os

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
    def __init__(self, archivo_datos="bd_agenda.json"):
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

    def agregar_contacto(self, nombre, telefono, email, direccion):
        """Añade un nuevo contacto. `direccion` es un diccionario.
        Ejemplo de `direccion`: {"calle": ..., "numero": ..., "municipio": ..., "cp": ...}
        """
        self.ultimo_id += 1
        id_contacto = str(self.ultimo_id)

        # Creamos el contacto
        self.contactos[id_contacto] = {
            "nombre": nombre,
            "telefono": telefono,
            "email": email,
            "direccion": direccion,
        }

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
            print(f"Nombre: {datos['nombre']}")
            print(f"Teléfono: {datos['telefono']}")
            print(f"Email: {datos['email']}")
            print("Dirección:")
            dir_ = datos.get('direccion', {})
            print(f"  Calle: {dir_.get('calle', '')}")
            print(f"  Número: {dir_.get('numero', '')}")
            print(f"  Municipio: {dir_.get('municipio', '')}")
            print(f"  CP: {dir_.get('cp', '')}")
            print("-" * 30)


    def editar_contacto(self, id_contacto, **datos):
        """Edita un contacto existente.
        Solo modifica los campos que se pasen. Soporta `direccion` completo.
        """
        if id_contacto not in self.contactos:
            return False

        for clave, valor in datos.items():
            if valor is not None:
                if clave == "direccion" and isinstance(valor, dict):
                    # Reemplaza la dirección completa o actualiza campos
                    self.contactos[id_contacto].setdefault("direccion", {}).update(valor)
                else:
                    self.contactos[id_contacto][clave] = valor

        self.guardar()
        return True


    def eliminar_contacto(self, id_contacto):
        """Elimina un contacto por ID."""
        if id_contacto not in self.contactos:
            return False

        del self.contactos[id_contacto]
        self.guardar()
        return True

# ============================================================
# INTERFAZ DE CONSOLA (solo para interactuar con la agenda)
# ============================================================

def menu():
    """Muestra el menú principal."""
    print("""
📞 AGENDA TELEFÓNICA
1. Añadir contacto
2. Mostrar contactos
3. Buscar por nombre
4. Editar contacto
5. Eliminar contacto
6. Salir
""")
        
def main():
    """Punto de entrada del programa."""
    agenda = AgendaTelefonica()

    while True:
        menu()
        opcion = input("Opción: ")

        # Añadir contacto
        if opcion == "1":
            nombre = input("Nombre: ")
            telefono = input("Teléfono: ")
            email = input("Email: ")

            direccion = {
                "calle": input("Calle: "),
                "numero": input("Número: "),
                "cp": input("CP: "),
                "municipio": input("Municipio: ")
            }

            nuevo_id = agenda.agregar_contacto(
                nombre, telefono, email, direccion
            )

            print(f"✅ Contacto añadido con ID {nuevo_id}")

        # Mostrar contactos
        elif opcion == "2":
            agenda.mostrar_contactos()

        # Buscar
        elif opcion == "3":
            texto = input("Contacto a buscar: ")
            resultados = agenda.buscar_por_nombre(texto)
            agenda.mostrar_contactos(resultados)

        # Editar
        elif opcion == "4":
            id_contacto = input("ID del contacto: ")
            if id_contacto not in agenda.contactos:
                print("❌ ID no encontrado")
            else:
                print("(deje vacío para no modificar)")
                nombre = input("Nuevo nombre: ").strip() or None
                telefono = input("Nuevo teléfono: ").strip() or None
                email = input("Nuevo email: ").strip() or None

                print("-- Dirección --")
                calle = input("Calle: ").strip() or None
                numero = input("Número: ").strip() or None
                municipio = input("Municipio: ").strip() or None
                cp = input("CP: ").strip() or None

                direccion = {}
                if calle is not None: direccion["calle"] = calle
                if numero is not None: direccion["numero"] = numero
                if municipio is not None: direccion["municipio"] = municipio
                if cp is not None: direccion["cp"] = cp

                success = agenda.editar_contacto(
                    id_contacto,
                    nombre=nombre,
                    telefono=telefono,
                    email=email,
                    direccion=direccion if direccion else None,
                )
                if success:
                    print("✏️ Contacto editado")
                else:
                    print("❌ No se pudo editar")
           

        # Eliminar
        elif opcion == "5":
            id_contacto = input("ID a eliminar: ")
            if agenda.eliminar_contacto(id_contacto):
                print("🗑️ Contacto eliminado")
            else:
                print("❌ ID no encontrado")

        # Salir
        elif opcion == "6":
            print("👋 Hasta luego")
            break

        else:
            print("❌ Opción no válida")


# ------------------------------------------------------------
# Ejecutar programa
# ------------------------------------------------------------
if __name__ == "__main__":
    main()