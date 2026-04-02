import openpyxl
import re
from models.contacto_models import Contacto
from models.direccion_models import Direccion
from models.contacto_info_models import InfoContactos
from utils.formateadores import capitalizar_texto

class ImportController:
    """
    Controlador para importar contactos desde archivos Excel.
    Maneja datos desorganizados y omite validaciones para campos vacíos.
    """
    
    def __init__(self):
        self.errores = []
        self.importados = 0
        
    def importar_excel(self, ruta_archivo):
        """
        Importa contactos desde un archivo Excel.
        
        Args:
            ruta_archivo (str): Ruta al archivo .xlsx
            
        Returns:
            tuple: (lista_contactos, errores, estadisticas)
        """
        self.errores = []
        self.importados = 0
        contactos = []
        
        try:
            # Cargar archivo Excel
            wb = openpyxl.load_workbook(ruta_archivo)
            ws = wb.active
            
            # Procesar cada fila (saltando headers)
            seen_data = False
            empty_streak = 0
            for fila_idx, fila in enumerate(ws.iter_rows(values_only=True), 1):
                if fila_idx == 1:  # Saltar encabezados
                    continue

                fila_tiene_datos = any(
                    (celda is not None) and str(celda).strip() != ""
                    for celda in fila
                )
                if not fila_tiene_datos:
                    if seen_data:
                        empty_streak += 1
                        if empty_streak >= 5:
                            break
                    continue

                seen_data = True
                empty_streak = 0
                    
                try:
                    contacto = self._procesar_fila(fila)
                    if contacto:
                        contactos.append(contacto)
                        self.importados += 1
                        
                except Exception as e:
                    self.errores.append(f"Fila {fila_idx}: {str(e)}")
                    
        except Exception as e:
            self.errores.append(f"Error al abrir archivo: {str(e)}")
        finally:
            if 'wb' in locals():
                wb.close()
                
        return contactos, self.errores, {
            'total_filas': fila_idx if 'fila_idx' in locals() else 0,
            'importados': self.importados,
            'errores': len(self.errores)
        }
    
    def _procesar_fila(self, fila):
        """
        Procesa una fila del Excel y crea un objeto Contacto.
        
        Args:
            fila (tuple): Tupla con los valores de la fila
            
        Returns:
            Contacto or None: Objeto contacto creado o None si falla
        """
        fila_tiene_datos = any(
            (celda is not None) and str(celda).strip() != ""
            for celda in fila
        )
        if not fila_tiene_datos:
            return None

        # Extraer datos básicos
        nombre_completo = str(fila[0]).strip() if fila[0] else ""
        
        # Extraer toda la información disponible de todas las columnas
        datos_completos = self._extraer_datos_completos(fila)
        
        # Procesar nombre completo
        nombre, apellido_1, apellido_2 = self._procesar_nombre_completo(nombre_completo)
        
        # Crear dirección (inteligente)
        direccion = self._crear_direccion_inteligente(datos_completos)
        
        # Crear información de contacto
        info_contactos = self._crear_info_contactos(datos_completos)
        
        # Crear contacto sin validaciones
        return Contacto(
            nombre=nombre,
            apellido_1=apellido_1, 
            apellido_2=apellido_2,
            direccion=direccion,
            info_contactos=info_contactos
        )
    
    def _procesar_nombre_completo(self, nombre_completo):
        """
        Procesa un nombre completo y lo divide en nombre, apellido_1, apellido_2.
        
        Args:
            nombre_completo (str): Nombre completo del contacto
            
        Returns:
            tuple: (nombre, apellido_1, apellido_2)
        """
        if not nombre_completo:
            return "", "", ""
            
        # Limpiar el nombre
        nombre_limpio = nombre_completo.upper()
        
        # Remover títulos profesionales comunes
        titulos = ['DR.', 'DRA.', 'ABOGADA', 'ABOGADO', 'ING.', 'LIC.', 'SR.', 'SRA.', 'PROF.']
        for titulo in titulos:
            nombre_limpio = nombre_limpio.replace(titulo, '').strip()
        
        # Manejar casos con coma (Apellido, Nombre)
        if ',' in nombre_limpio:
            partes = nombre_limpio.split(',')
            if len(partes) >= 2:
                apellido_partes = partes[0].strip().split()
                nombre_partes = partes[1].strip().split()
                
                # Última parte de apellido como apellido_1
                apellido_1 = apellido_partes[-1] if apellido_partes else ""
                # Resto de apellidos como apellido_2
                apellido_2 = ' '.join(apellido_partes[:-1]) if len(apellido_partes) > 1 else ""
                # Primera parte del nombre como nombre
                nombre = nombre_partes[0] if nombre_partes else ""
                
                return capitalizar_texto(nombre), capitalizar_texto(apellido_1), capitalizar_texto(apellido_2)
        
        # Caso normal: dividir por espacios
        partes = nombre_limpio.split()
        
        if len(partes) == 1:
            return capitalizar_texto(partes[0]), "", ""
        elif len(partes) == 2:
            return capitalizar_texto(partes[1]), capitalizar_texto(partes[0]), ""
        elif len(partes) >= 3:
            return capitalizar_texto(partes[-1]), capitalizar_texto(partes[-2]), ' '.join(partes[:-2])
        
        return "", "", ""
    
    def _extraer_datos_completos(self, fila):
        """
        Extrae toda la información disponible de la fila.
        
        Args:
            fila (tuple): Valores de la fila
            
        Returns:
            dict: Diccionario con toda la información encontrada
        """
        datos = {
            'telefonos': [],
            'emails': [],
            'direcciones': [],
            'notas': [],
            'observaciones': "",
            'auxiliar': ""
        }
        
        # Columnas específicas según el Excel
        mapeo_columnas = {
            1: 'nombre',      # Columna 0 (índice 0)
            2: 'direccion',   # Columna 1
            3: 'poblacion',   # Columna 2
            4: 'telefono_1',  # Columna 3
            5: 'notas_1',     # Columna 4
            6: 'telefono_2',  # Columna 5
            7: 'notas_2',     # Columna 6
            8: 'telefono_3',  # Columna 7
            9: 'notas_3',     # Columna 8
            10: 'telefono_4', # Columna 9
            11: 'notas_4',    # Columna 10
            12: 'observaciones', # Columna 11
            13: 'auxiliar',   # Columna 12
            14: 'email'       # Columna 13
        }
        
        for idx, valor in enumerate(fila):
            if valor is None:
                continue
                
            valor_str = str(valor).strip()
            if not valor_str:
                continue
                
            columna = mapeo_columnas.get(idx + 1, f'columna_{idx + 1}')
            
            # Extraer teléfonos
            telefonos_encontrados = self._extraer_telefonos(valor_str)
            datos['telefonos'].extend(telefonos_encontrados)
            
            # Extraer emails
            emails_encontrados = self._extraer_emails(valor_str)
            datos['emails'].extend(emails_encontrados)
            
            # Clasificar por tipo de columna
            if columna in ['direccion', 'poblacion']:
                datos['direcciones'].append(valor_str)
            elif columna.startswith('notas_'):
                datos['notas'].append(valor_str)
            elif columna == 'observaciones':
                datos['observaciones'] = valor_str
            elif columna == 'auxiliar':
                datos['auxiliar'] = valor_str
        
        return datos
    
    def _extraer_telefonos(self, texto):
        """
        Extrae números de teléfono de un texto usando expresiones regulares.
        
        Args:
            texto (str): Texto a analizar
            
        Returns:
            list: Lista de teléfonos encontrados
        """
        telefonos = []
        
        # Patrones comunes de teléfono español
        patrones = [
            r'\b\d{9}\b',           # 9 dígitos
            r'\b\d{2,3}[\s\-\.]?\d{2,3}[\s\-\.]?\d{2,3}[\s\-\.]?\d{2,3}\b',  # Con separadores
            r'\b\d{3}[\s\-\.]\d{3}[\s\-\.]\d{3}\b',  # Formato XXX-XXX-XXX
            r'\+\d{2,3}[\s\-\.]?\d{9}\b'  # Internacional
        ]
        
        for patron in patrones:
            matches = re.findall(patron, texto)
            for match in matches:
                # Limpiar el teléfono
                telefono_limpio = re.sub(r'[^\d]', '', match)
                if len(telefono_limpio) >= 9 and telefono_limpio not in telefonos:
                    telefonos.append(telefono_limpio)
        
        return telefonos
    
    def _extraer_emails(self, texto):
        """
        Extrae direcciones de email de un texto.
        
        Args:
            texto (str): Texto a analizar
            
        Returns:
            list: Lista de emails encontrados
        """
        emails = []
        patron_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(patron_email, texto, re.IGNORECASE)
        
        for match in matches:
            if match not in emails:
                emails.append(match.lower())
        
        return emails
    
    def _crear_direccion_inteligente(self, datos):
        """
        Crea un objeto Dirección de forma inteligente a partir de datos desorganizados.
        
        Args:
            datos (dict): Datos extraídos de la fila
            
        Returns:
            Direccion: Objeto dirección creado
        """
        # Unir todas las direcciones encontradas
        texto_direccion = ' '.join(datos['direcciones'])
        
        # Intentar extraer componentes de dirección
        calle = ""
        numero = ""
        piso = ""
        puerta = ""
        escalera = ""
        cp = ""
        provincia = ""
        
        if texto_direccion:
            # Buscar código postal (5 dígitos)
            cp_match = re.search(r'\b\d{5}\b', texto_direccion)
            if cp_match:
                cp = cp_match.group()
                # Remover CP del texto para no interferir
                texto_direccion = texto_direccion.replace(cp, '').strip()
            
            # Buscar número (normalmente después de calle)
            numero_match = re.search(r'\b\d{1,3}\b(?!\s*(?:º|ª|°|piso|p|pta|puerta|esc|escalera|cp|provincia))', texto_direccion)
            if numero_match:
                numero = numero_match.group()
            
            # Buscar piso, puerta, escalera
            piso_match = re.search(r'(\d{1,2})(?:º|ª|°)\s*(?:piso|p\.?)?', texto_direccion, re.IGNORECASE)
            if piso_match:
                piso = piso_match.group(1)
            
            puerta_match = re.search(r'(?:puerta|pta\.?)\s*([A-Za-z0-9]+)', texto_direccion, re.IGNORECASE)
            if puerta_match:
                puerta = puerta_match.group(1)
            
            escalera_match = re.search(r'(?:escalera|esc\.?)\s*([A-Za-z0-9]+)', texto_direccion, re.IGNORECASE)
            if escalera_match:
                escalera = escalera_match.group(1)
            
            # Lo que queda es probablemente la calle
            calle = re.sub(r'\b\d{1,3}(?:º|ª|°)?\s*(?:piso|p\.?|puerta|pta\.?|escalera|esc\.?)\s*[A-Za-z0-9]*', '', texto_direccion).strip()
            calle = re.sub(r'\s+', ' ', calle)  # Normalizar espacios
        
        # Crear dirección sin validaciones
        return Direccion(
            calle=calle,
            numero=numero,
            piso=piso,
            puerta=puerta,
            escalera=escalera,
            cp=cp,
            provincia=provincia  # Difícil de extraer automáticamente
        )
    
    def _crear_info_contactos(self, datos):
        """
        Crea un objeto InfoContactos con la información disponible.
        
        Args:
            datos (dict): Datos extraídos de la fila
            
        Returns:
            InfoContactos: Objeto información de contactos
        """
        # Asignar teléfonos encontrados (máximo 4)
        telefonos = datos['telefonos'][:4]
        telefono_1 = telefonos[0] if len(telefonos) > 0 else None
        telefono_2 = telefonos[1] if len(telefonos) > 1 else None
        telefono_3 = telefonos[2] if len(telefonos) > 2 else None
        telefono_4 = telefonos[3] if len(telefonos) > 3 else None
        
        # Asignar notas
        notas = datos['notas'][:4]
        nota_1 = notas[0] if len(notas) > 0 else None
        nota_2 = notas[1] if len(notas) > 1 else None
        nota_3 = notas[2] if len(notas) > 2 else None
        nota_4 = notas[3] if len(notas) > 3 else None
        
        # Email principal
        email = datos['emails'][0] if datos['emails'] else None
        
        # Crear objeto sin validaciones
        return InfoContactos(
            email=email,
            telefono_1=telefono_1,
            telefono_2=telefono_2,
            telefono_3=telefono_3,
            telefono_4=telefono_4,
            nota_1=nota_1,
            nota_2=nota_2,
            nota_3=nota_3,
            nota_4=nota_4,
            observaciones=datos['observaciones'],
            auxiliar=datos['auxiliar']
        )
