# 📞 Agenda Telefónica v1.0.0

Aplicación desktop para gestionar contactos telefónicos de manera eficiente y fácil.

## ✨ Características

- ✅ Agregar, editar y eliminar contactos
- ✅ Búsqueda rápida de contactos
- ✅ Importación masiva desde archivos Excel
- ✅ Interfaz gráfica intuitiva (PySide6)
- ✅ Almacenamiento persistente en JSON
- ✅ Información de contacto detallada (teléfono, dirección, email, etc.)

## 📋 Requisitos

- **Python 3.11+**
- **Sistema Operativo**: Windows, macOS o Linux

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Jonatan1991/Agenda_Telefonica.git
cd Agenda_Telefonica
```

### 2. Crear entorno virtual (recomendado)

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 💻 Uso

### Ejecutar la aplicación

```bash
python main_gui.py
```

Esto abrirá la interfaz gráfica principal de la aplicación.

### Usando la consola (opcional)

Para la versión de línea de comandos:

```bash
python main.py
```

## 📁 Estructura del Proyecto

```
Agenda_Telefonica/
├── controllers/          # Lógica de negocio
│   ├── agenda_controller.py
│   └── import_controller.py
├── models/              # Modelos de datos
│   ├── agenda_models.py
│   ├── contacto_models.py
│   ├── contacto_info_models.py
│   └── direccion_models.py
├── views/               # Interfaz de usuario
│   ├── consola_view.py
│   └── gui/
│       ├── main_window.py
│       ├── tabla_contactos.py
│       ├── contacto_dialog.py
│       ├── contacto_ver_dialog.py
│       └── components/
│           ├── toolbar.py
│           ├── paginador.py
│           └── buscador.py
├── utils/               # Funciones auxiliares
│   ├── validaciones.py
│   └── formateadores.py
├── style/               # Estilos CSS (QSS)
│   └── app.qss
├── data/                # Base de datos
│   └── bd_agenda.json
├── main_gui.py         # Punto de entrada (GUI)
├── main.py             # Punto de entrada (Consola)
└── requirements.txt    # Dependencias del proyecto
```

## 📦 Crear ejecutable (Windows)

Para crear un archivo `.exe` ejecutable sin necesidad de Python:

### Instalar PyInstaller

```bash
pip install pyinstaller
```

### Generar ejecutable

```bash
pyinstaller "Agenda Telefonica.spec"
```

El ejecutable se encontrará en `dist/Agenda Telefonica/Agenda Telefonica.exe`

## 🎨 Funcionalidades de la GUI

### Barra de herramientas
- **Nuevo**: Crear un contacto nuevo
- **Editar**: Modificar contacto seleccionado
- **Eliminar**: Borrar contacto
- **Importar**: Cargar contactos desde Excel
- **Buscar**: Filtrar contactos por nombre/teléfono

### Tabla de contactos
- Visualiza todos los contactos guardados
- Paginación para manejar grandes cantidades
- Ordenamiento por columnas

### Gestor de contactos
- Información completa: nombre, teléfono, email, dirección, etc.
- Validación de datos antes de guardar
- Interfaz amigable para creación/edición

## 🔧 Importar desde Excel

1. Prepara un archivo Excel con las siguientes columnas:
   - Nombre
   - Teléfono
   - Email (opcional)
   - Dirección (opcional)

2. En la aplicación, haz clic en **Importar**
3. Selecciona el archivo Excel
4. Los contactos se cargarán automáticamente

## 📝 Notas de versión v1.0.0

- ✅ Interfaz gráfica completa
- ✅ CRUD de contactos funcional
- ✅ Importación de Excel
- ✅ Búsqueda y filtrado
- ✅ Persistencia de datos

## 🐛 Problemas conocidos

_Ninguno conocido en la versión 1.0.0_

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios importantes, abre un issue primero para discutir qué cambios te gustaría hacer.

## 📄 Licencia

Este proyecto es de código abierto. Úsalo libremente.

## 👨‍💻 Autor

**Jonatan1991**

GitHub: [Jonatan1991](https://github.com/Jonatan1991)

---

**¿Preguntas o sugerencias?** Abre un [issue en GitHub](https://github.com/Jonatan1991/Agenda_Telefonica/issues)
