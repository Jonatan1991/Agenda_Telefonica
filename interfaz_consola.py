# ============================================================
# INTERFAZ DE CONSOLA (solo para interactuar con la agenda)
# ============================================================

from agenda import AgendaTelefonica

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

            try:
                nuevo_id = agenda.agregar_contacto(
                nombre, telefono, email, direccion
                )
                print(f"✅ Contacto añadido con ID {nuevo_id}")
            except ValueError as error:
                print("❌ Error:", error)

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
