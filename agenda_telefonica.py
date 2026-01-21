import json
import os

ARCHIVO_DATOS = "bd_agenda.json"

def cargar_contactos():
    #carga los contactos desde el archivo JSON
    if not os.path.exists(ARCHIVO_DATOS):
        return{}
    
    with open(ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
        try:
            return json.load(archivo)
        except json.JSONDecodeError:
            return {}
        
def guardar_contactos(contactos):
    #guardar contactos en el archivo JSON
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as archivo:
        json.dump(contactos, archivo, indent=4, ensure_ascii=False)

def agregar_contacto(contactos):
    nombre = input("Nombre del Contacto").strip()

    if nombre in contactos:
        print("El contacto ya existe")
        return
    
    id = input("ID: ").strip()
    telefono = input("Telefono: ").strip()
    email = input("Email: ").strip()
    print("Direccion: ")
    calle = input("Calle: ").strip()
    numero = input("Numero: ").strip()
    municipio = input("Municipio: ").strip()
    cp = input("CP: ").strip()


    contactos[id] = {
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

    guardar_contactos(contactos)
    print("Contacto añadido correctamente")


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



def menu():
    print("""
📞 AGENDA TELEFÓNICA
1. Añadir contacto
2. Mostrar contactos
3. Salir
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
             print("👋 Saliendo de la agenda...")
             break
        else:
            print("❌ Opción no válida.")


# if __name__ == "__main__":
#     main()

main()