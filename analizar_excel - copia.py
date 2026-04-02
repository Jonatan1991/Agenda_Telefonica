import openpyxl
from collections import Counter

# Cargar el archivo Excel
wb = openpyxl.load_workbook('agenda maria jose.xlsx')
ws = wb.active

# 1. Obtener los encabezados
headers = [cell.value for cell in ws[1]]
print('='*60)
print('ENCABEZADOS DE COLUMNAS:')
print('='*60)
for i, header in enumerate(headers, 1):
    print(f"  {i}. {header}")

# 2. Mostrar los primeros 10 registros
print('\n' + '='*60)
print('PRIMEROS 10 REGISTROS DE DATOS:')
print('='*60)
rows_data = []
for i, row in enumerate(ws.iter_rows(values_only=True), 0):
    if i == 0:  # Saltar headers
        continue
    if i > 10:  # Solo los primeros 10
        break
    rows_data.append(row)
    print(f"\nRegistro {i}:")
    for j, (header, value) in enumerate(zip(headers, row)):
        print(f"  {header}: {value}")

# 3. Analizar patrones en nombres completos
print('\n' + '='*60)
print('ANÁLISIS DE PATRONES EN NOMBRES:')
print('='*60)

# Asumir que la columna de nombre completo es la primera o contiene "nombre"
nombre_col_idx = None
for idx, header in enumerate(headers):
    if header and ('nombre' in str(header).lower()):
        nombre_col_idx = idx
        print(f"Columna de nombres detectada: '{header}' (columna {idx+1})")
        break

if nombre_col_idx is not None:
    nombres_completos = []
    for i, row in enumerate(ws.iter_rows(values_only=True), 0):
        if i == 0:  # Saltar headers
            continue
        if row[nombre_col_idx]:
            nombres_completos.append(str(row[nombre_col_idx]).strip())

    print(f"\nTotal de contactos: {len(nombres_completos)}")
    print(f"\nEjemplos de nombres completos:")
    for nombre in nombres_completos[:10]:
        print(f"  - {nombre}")
        # Analizar estructura
        partes = nombre.split()
        print(f"    Partes: {len(partes)} | {partes}")
else:
    print("No se encontró columna de nombres.")

wb.close()