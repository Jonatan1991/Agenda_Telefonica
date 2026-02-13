import json
import os

ARCHIVO_DATOS = "bd_agenda.json"

def cargar_contactos():
    #carga los contactos desde el archivo JSON
    if not os.path.exists(ARCHIVO_DATOS):
        return{}
    
    #with open garantiza que el arhcivo se cierre correctamrente a l finalizar la operacion
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
    if not contactos:
        return 1  # Si está vacío, el primer ID es 1
    
    # Convertir las claves a enteros y obtener el máximo
    max_id = max([int(i) for i in contactos.keys()])
    id = max_id + 1
    print (id)

    nombre = input("Nombre: ").strip()

    for contacto in contactos:
        if contacto[nombre] in contactos:
            print("El contacto ya existe")
            return
    
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