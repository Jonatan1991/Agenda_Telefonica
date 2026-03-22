# ============================================================
# INTERFAZ DE CONSOLA (solo para interactuar con la agenda)
# ============================================================

from controllers.agenda_controller import AgendaController
from models.contacto_models import Contacto
from models.direccion_models import Direccion

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
        
def iniciar_consola():
    """Punto de entrada del programa."""
    agenda = AgendaController()

    while True:
        menu()
        opcion = input("Opción: ")

        # Añadir contacto
        if opcion == "1":
            nombre = input("Nombre: ")

            direccion = {
                "calle": input("Calle: "),
                "numero": input("Número: "),
                "cp": input("CP: "),
                "provincia": input("Provincia: ")
            }

            direccion_obj = Direccion.from_dict(direccion) if any(direccion.values()) else None

            contacto_obj = Contacto(
                nombre=nombre,
                apellido_1="",
                apellido_2="",
                telefono=telefono,
                email=email,
                direccion=direccion_obj
            )

            try:
                nuevo_id = agenda.agregar_contacto(contacto_obj)
                print(f"✅ Contacto añadido con ID {nuevo_id}")
            except ValueError as error:
                print("❌ Error:", error)

        # Mostrar contactos
        elif opcion == "2":
            contactos = agenda.obtener_contactos()
            agenda.agenda.mostrar_contactos(contactos)

        # Buscar
        elif opcion == "3":
            texto = input("Contacto a buscar: ")
            resultados = agenda.buscar_contacto(texto)
            agenda.agenda.mostrar_contactos(resultados)

        # Editar
        elif opcion == "4":
            id_contacto = input("ID del contacto: ")
            if id_contacto not in agenda.agenda.contactos:
                print("❌ ID no encontrado")
            else:
                datos_existentes = agenda.agenda.contactos[id_contacto]
                contacto_existente = Contacto.from_dict(datos_existentes)

                print("(deje vacío para no modificar)")
                nombre = input(f"Nuevo nombre ({contacto_existente.nombre}): ").strip() or contacto_existente.nombre

                print("-- Dirección --")
                dir_dict = contacto_existente.direccion.to_dict() if contacto_existente.direccion else {}
                calle = input(f"Calle ({dir_dict.get('calle', '')}): ").strip() or dir_dict.get('calle', '')
                numero = input(f"Número ({dir_dict.get('numero', '')}): ").strip() or dir_dict.get('numero', '')
                provincia = input(f"Provincia ({dir_dict.get('provincia', '')}): ").strip() or dir_dict.get('provincia', '')
                cp = input(f"CP ({dir_dict.get('cp', '')}): ").strip() or dir_dict.get('cp', '')

                nueva_direccion = Direccion(calle=calle, numero=numero, provincia=provincia, cp=cp)

                contacto_actualizado = Contacto(
                    nombre=nombre,
                    apellido_1=contacto_existente.apellido_1,
                    apellido_2=contacto_existente.apellido_2,
                    direccion=nueva_direccion
                )

                try:
                    success = agenda.editar_contacto(id_contacto, contacto_actualizado)

                    if success:
                        print("✏️ Contacto editado")
                    else:
                        print("❌ No se pudo editar")

                except ValueError as error:
                    print("❌ Error:", error)
           

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