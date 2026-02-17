import json
import os

class Agenda_telefonica:
    def __init__(self, archivo_datos="bd_agenda.json" ):
        self.archivo_datos = archivo_datos
        self.contactos = {}
        self.ultimo_id = 0
        self.cargar()

    def cargar_contactos(self):
        #carga los contactos desde el archivo JSON
        if not os.path.exists(self.archivo_datos):
            self.contactos = {}
            self.ultimo_id = 0
            return
    
        #with open garantiza que el arhcivo se cierre correctamrente a l finalizar la operacion
        with open(self.archivo_datos, "r", encoding="utf-8") as archivo:
            try:
                self.contactos = json.load(archivo)
                self.ultimo_id = self._obtener_ultimo_id()
            except json.JSONDecodeError:
                self.contactos = {}
                self.ultimo_id = 0        
        
    def guardar(self):
        #guardar contactos en el archivo JSON
        with open(self.archivo_datos, "w", encoding="utf-8") as archivo:
            json.dump(self.contactos, archivo, indent=4, ensure_ascii=False)

    def _obtener_ultimo_id(self):
        if not self.contactos:
            return 0
        return max(int(i) for i in self.contactos.keys())
    

    #_______CRUD_________

    def agregar_contacto(self, nombre, telefono, email, calle, numero, municipio, cp):
        self.ultimo_id += 1
        id_contacto = str(self.ultimo_id)

        self.contacto[id_contacto] = {
             "nombre": nombre,
            "telefono": telefono,
            "email" : email,
            "direccion": {
                "calle": calle,
                "numero" : numero,
                "municipio": municipio,
                "cp" : cp,
            }
        }


        self.guardar()
        return id_contacto


    def mostrar_contactos(contactos):
        if not contactos:
            print("La agenda esta vacia.")
            return
        
        print("\nLista de contactos")
        print("-" * 30)

        for id, datos in contactos.items():
            print(f"ID: {id}")
            print(f"Nombre: {datos['nombre']}")
            print(f"Teléfono: {datos['telefono']}")
            print(f"Email: {datos['email']}")
            print("Dirección:")
            print(f"  Calle: {datos['direccion']['calle']}")
            print(f"  Número: {datos['direccion']['numero']}")
            print(f"  Municipio: {datos['direccion']['municipio']}")
            print(f"  CP: {datos['direccion']['cp']}")
            print("-" * 30)

    def buscar_contacto(contactos):
        id = input("id a buscar: ").strip()

        if id not in contactos:
            print("❌ Contacto no encontrado.")
            return

        datos = contactos[id]
        print("\n🔍 CONTACTO ENCONTRADO")
        print(f"Nombre   : {datos["nombre"]}")
        print(f"Teléfono : {datos['telefono']}")
        print(f"Email    : {datos['email']}")

    def actualizar_contacto(contacto):
        print("actualizar")
        return

    def eliminar_contacto(contacto):
        print("eliminar")
        return


    def menu():
        print("""
    📞 AGENDA TELEFÓNICA
    1. Añadir contacto
    2. Mostrar contactos
    3. Buscar contactos
    4. Actualizar contacto
    5. Eliminar contacto
    6. Salir
    """)
        
    def main():
        contactos = cargar_contactos()

        while True:
            menu()
            opcion = input("Seleccione una opcion: ")

            if opcion == "1":
                agregar_contacto(contactos)
            elif opcion == "2":
                mostrar_contactos(contactos)
            elif opcion == "3":
                buscar_contacto(contactos)
            elif opcion == "4":
                actualizar_contacto(contactos)
            elif opcion == "5":
            eliminar_contacto(contactos)
            elif opcion == "6":
                print("👋 Saliendo de la agenda...")
                break
            else:
                print("❌ Opción no válida.")


    # if __name__ == "__main__":
    #     main()

    main()