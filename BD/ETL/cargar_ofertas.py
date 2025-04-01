import psycopg2
import csv
import os
import re

# 🔹 Configuración de la conexión a PostgreSQL
DB_HOST = "localhost"
DB_NAME = "Ofertas_laborales"      
DB_USER = "postgres"          
DB_PASS = "123456"       
DB_PORT = "5432"

# 🔹 Ruta del archivo CSV - Usá la ruta absoluta para evitar problemas
archivo_csv = "C:/Users/Anhi Lari/Documents/Lari/2do TUPED/Practicas Academicas/Practicas Academicas/BD/ETL/ofertas_laborales.csv"

# 🔹 Lista de idiomas para detectar (en minúsculas para comparación)
idiomas_lista = ["inglés", "español", "francés", "portugués", "alemán", "italiano", "chino", "japonés"]

# 🔹 Función para extraer especialidad
def extraer_especialidad(texto):
    """Extrae la especialidad del texto del puesto o descripción."""
    # Mapeo de palabras clave a especialidades
    mapeo_especialidades = {
        "Bioinformática": ["bioinformático", "bioinformatica", "bioinformatico", "lic. bioinformatico"],
        "Ingeniería Biomédica": ["bioingeniería", "bioingenieria", "biomédica", "biomedica", "bioingeniero"],
        "Desarrollo de Software": ["desarrollador", "programador", "software", "desarrollo"],
        "Ciencia de Datos": ["datos", "data science", "analista de datos", "procesamiento de datos"],
        "Ingeniería": ["ingeniero", "ingenieria", "ingeniería"],
        "Técnico": ["técnico", "tecnico"]
    }
    
    texto_lower = texto.lower()
    
    # Buscar coincidencias en el mapeo
    for especialidad, palabras_clave in mapeo_especialidades.items():
        for palabra in palabras_clave:
            if palabra in texto_lower:
                return especialidad
    
    # Si no se encuentra ninguna coincidencia, devolver valor por defecto
    return "Otra especialidad"

# 🔹 Función para detectar idiomas en el texto
def detectar_idiomas(texto):
    """Detecta idiomas mencionados en el texto."""
    idiomas_detectados = []
    texto_lower = texto.lower()
    
    for idioma in idiomas_lista:
        if idioma in texto_lower:
            idiomas_detectados.append(idioma.capitalize())
    
    # Si no se detectó ningún idioma, agregar "Idioma no especificado"
    if not idiomas_detectados:
        idiomas_detectados.append("Idioma no especificado")
    
    return idiomas_detectados

# 🔹 Función para limpiar y normalizar texto
def limpiar_texto(texto):
    """Limpia y normaliza un texto."""
    if not texto:
        return ""
    
    # Eliminar caracteres especiales y normalizar espacios
    texto = re.sub(r'\s+', ' ', texto)
    return texto.strip()

# 🔹 Función para procesar fechas en diferentes formatos
def procesar_fecha(fecha_texto):
    """Procesa fechas en diferentes formatos y devuelve (dia, mes, anio)."""
    if not fecha_texto or fecha_texto == "No especificada":
        return None, None, None
    
    # Diccionario de meses
    meses_dict = {
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
        "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
        "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
    }
    
    try:
        # Formato: "4 de octubre de 2022"
        if " de " in fecha_texto:
            partes = fecha_texto.split(" de ")
            dia = int(partes[0])
            mes = meses_dict.get(partes[1].lower())
            anio = int(partes[2])
            return dia, mes, anio
            
        # Formato: "29/9/2022"
        elif "/" in fecha_texto:
            partes = fecha_texto.split("/")
            dia = int(partes[0])
            mes = int(partes[1])
            anio = int(partes[2])
            return dia, mes, anio
            
        # Formato: "01/04/2023" o "01-04-2023"
        elif re.match(r'\d{2}[/\-]\d{2}[/\-]\d{4}', fecha_texto):
            partes = re.split(r'[/\-]', fecha_texto)
            dia = int(partes[0])
            mes = int(partes[1])
            anio = int(partes[2])
            return dia, mes, anio
            
        # Formato: "2022-10-04" (ISO)
        elif re.match(r'\d{4}[/\-]\d{2}[/\-]\d{2}', fecha_texto):
            partes = re.split(r'[/\-]', fecha_texto)
            anio = int(partes[0])
            mes = int(partes[1])
            dia = int(partes[2])
            return dia, mes, anio
            
        # Formato: "18/07/2022" (con ceros)
        elif re.match(r'\d{1,2}/\d{1,2}/\d{4}', fecha_texto):
            partes = fecha_texto.split("/")
            dia = int(partes[0])
            mes = int(partes[1])
            anio = int(partes[2])
            return dia, mes, anio
        
        # Otros formatos no reconocidos
        else:
            print(f"⚠️ Formato de fecha no reconocido: {fecha_texto}")
            return None, None, None
            
    except Exception as e:
        print(f"⚠️ Error procesando fecha '{fecha_texto}': {e}")
        return None, None, None

try:
    # Verificar si el archivo existe
    if not os.path.exists(archivo_csv):
        print(f"❌ El archivo no existe en la ruta: {archivo_csv}")
        print(f"Directorio actual: {os.getcwd()}")
        exit(1)
        
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )
    cursor = conn.cursor()
    print("✅ Conexión exitosa a PostgreSQL")

    # 🔹 Asegurarse de que exista la especialidad "Otra especialidad"
    cursor.execute(
        "INSERT INTO especialidad (nombre_especialidad) VALUES (%s) ON CONFLICT (nombre_especialidad) DO NOTHING",
        ("Otra especialidad",)
    )
    
    # 🔹 Insertar idiomas básicos y el valor por defecto
    idiomas_lista.append("idioma no especificado")
    for idioma in idiomas_lista:
        cursor.execute(
            "INSERT INTO idioma (nombre_idioma) VALUES (%s) ON CONFLICT (nombre_idioma) DO NOTHING",
            (idioma.capitalize(),)
        )
    
    conn.commit()

    # 🔹 Leer el archivo CSV y cargar datos
    with open(archivo_csv, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        headers = next(reader)  # Leer la cabecera
        
        print(f"Cabeceras del CSV: {headers}")  # Imprimir para verificar estructura
        
        # Procesar cada fila del CSV
        for row in reader:
            try:
                # Verificar que la fila tenga todos los datos esperados
                if len(row) < 5:
                    print(f"⚠️ Fila incompleta, saltando: {row}")
                    continue
                    
                empresa_raw, puesto_raw, ciudad, fecha, habilidades = row
                
                # Limpiar y normalizar los campos
                empresa = limpiar_texto(empresa_raw)
                puesto = limpiar_texto(puesto_raw)
                ciudad = limpiar_texto(ciudad)
                
                # Si la empresa está vacía o es muy corta, usar un valor por defecto
                if len(empresa) < 3:
                    empresa = "Empresa no especificada"
                
                # Si el puesto está vacío, usar un valor por defecto
                if not puesto:
                    puesto = "Puesto no especificado"
                
                # Si la ciudad es "No especificada", usar un valor por defecto
                if ciudad == "No especificada" or not ciudad:
                    ciudad = "Ciudad no especificada"
                
                print(f"Procesando: {empresa} - {puesto} ({ciudad})")
                
                # Iniciar transacción para cada fila
                conn.autocommit = False
                
                # 🔹 Insertar empresa
                cursor.execute("INSERT INTO empresa (nombre_empresa) VALUES (%s) ON CONFLICT (nombre_empresa) DO NOTHING RETURNING id_empresa;", (empresa,))
                id_empresa_result = cursor.fetchone()
                
                # Si no devolvió ID (porque ya existía), buscarlo
                if id_empresa_result:
                    id_empresa = id_empresa_result[0]
                else:
                    cursor.execute("SELECT id_empresa FROM empresa WHERE nombre_empresa = %s;", (empresa,))
                    id_empresa = cursor.fetchone()[0]
                print(f"✅ Empresa: {empresa} (ID: {id_empresa})")

                # 🔹 Insertar puesto
                cursor.execute("INSERT INTO puesto (nombre_puesto) VALUES (%s) ON CONFLICT (nombre_puesto) DO NOTHING RETURNING id_puesto;", (puesto,))
                id_puesto_result = cursor.fetchone()
                
                if id_puesto_result:
                    id_puesto = id_puesto_result[0]
                else:
                    cursor.execute("SELECT id_puesto FROM puesto WHERE nombre_puesto = %s;", (puesto,))
                    id_puesto = cursor.fetchone()[0]
                print(f"✅ Puesto: {puesto} (ID: {id_puesto})")

                # 🔹 Insertar ubicación
                cursor.execute("INSERT INTO ubicacion (ciudad) VALUES (%s) ON CONFLICT (ciudad) DO NOTHING RETURNING id_ubicacion;", (ciudad,))
                id_ubicacion_result = cursor.fetchone()
                
                if id_ubicacion_result:
                    id_ubicacion = id_ubicacion_result[0]
                else:
                    cursor.execute("SELECT id_ubicacion FROM ubicacion WHERE ciudad = %s;", (ciudad,))
                    id_ubicacion = cursor.fetchone()[0]
                print(f"✅ Ciudad: {ciudad} (ID: {id_ubicacion})")

                # 🔹 Extraer e insertar especialidad
                especialidad = extraer_especialidad(puesto)  # Extraer del título del puesto
                
                cursor.execute("INSERT INTO especialidad (nombre_especialidad) VALUES (%s) ON CONFLICT (nombre_especialidad) DO NOTHING RETURNING id_especialidad;", (especialidad,))
                id_especialidad_result = cursor.fetchone()
                
                if id_especialidad_result:
                    id_especialidad = id_especialidad_result[0]
                else:
                    cursor.execute("SELECT id_especialidad FROM especialidad WHERE nombre_especialidad = %s;", (especialidad,))
                    id_especialidad = cursor.fetchone()[0]
                print(f"✅ Especialidad: {especialidad} (ID: {id_especialidad})")

                # 🔹 Insertar fecha - MEJORADO
                id_tiempo = None
                dia, mes, anio = procesar_fecha(fecha)
                
                if dia and mes and anio:
                    cursor.execute(
                        "INSERT INTO tiempo (dia, mes, anio) VALUES (%s, %s, %s) ON CONFLICT (dia, mes, anio) DO NOTHING RETURNING id_tiempo;",
                        (dia, mes, anio)
                    )
                    id_tiempo_result = cursor.fetchone()
                    
                    if id_tiempo_result:
                        id_tiempo = id_tiempo_result[0]
                    else:
                        cursor.execute("SELECT id_tiempo FROM tiempo WHERE dia = %s AND mes = %s AND anio = %s;", (dia, mes, anio))
                        tiempo_result = cursor.fetchone()
                        if tiempo_result:
                            id_tiempo = tiempo_result[0]
                    print(f"✅ Fecha: {dia}/{mes}/{anio} (ID: {id_tiempo})")
                else:
                    print(f"⚠️ Fecha no procesada: {fecha}")

                # 🔹 Insertar en tabla de hechos oferta_laboral
                cursor.execute("""
                    INSERT INTO oferta_laboral (id_empresa, id_puesto, id_ubicacion, id_especialidad, id_tiempo)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id_oferta;
                """, (id_empresa, id_puesto, id_ubicacion, id_especialidad, id_tiempo))

                id_oferta = cursor.fetchone()[0]
                print(f"✅ Oferta laboral creada con ID: {id_oferta}")

                # 🔹 Detectar y procesar idiomas - MEJORADO
                texto_completo = f"{puesto} {habilidades}"
                idiomas_detectados = detectar_idiomas(texto_completo)
                
                print(f"🔍 Idiomas detectados: {', '.join(idiomas_detectados)}")
                
                for idioma_nombre in idiomas_detectados:
                    # Obtener ID del idioma
                    cursor.execute("SELECT id_idioma FROM idioma WHERE nombre_idioma = %s;", (idioma_nombre,))
                    id_idioma_result = cursor.fetchone()
                    
                    if id_idioma_result:
                        id_idioma = id_idioma_result[0]
                        # Crear relación
                        cursor.execute(
                            "INSERT INTO oferta_idioma (id_oferta, id_idioma) VALUES (%s, %s) ON CONFLICT DO NOTHING;", 
                            (id_oferta, id_idioma)
                        )
                        print(f"✅ Idioma asociado: {idioma_nombre}")
                    else:
                        print(f"⚠️ No se encontró el idioma: {idioma_nombre}")

                # 🔹 Insertar habilidades técnicas y blandas en tablas intermedias
                if habilidades:
                    for habilidad_completa in habilidades.split(","):
                        habilidad_completa = habilidad_completa.strip()
                        if not habilidad_completa:
                            continue
                            
                        # Extraer el nombre de la habilidad y su tipo
                        if "(" in habilidad_completa and ")" in habilidad_completa:
                            # Formato: "python (Técnica)"
                            partes = habilidad_completa.split("(")
                            habilidad = partes[0].strip()
                            tipo = partes[1].replace(")", "").strip().lower()
                            
                            es_tecnica = "técnica" in tipo or "tecnica" in tipo
                            es_blanda = "blanda" in tipo
                        else:
                            # Si no tiene tipo, asumimos que es técnica
                            habilidad = habilidad_completa
                            es_tecnica = True
                            es_blanda = False
                        
                        # Procesar como habilidad técnica
                        if es_tecnica:
                            # Primero verificar si existe la habilidad
                            cursor.execute("SELECT id_habilidad_tecnica FROM habilidad_tecnica WHERE nombre_habilidad_tecnica = %s;", (habilidad,))
                            id_result = cursor.fetchone()
                            
                            if id_result:
                                id_habilidad_tecnica = id_result[0]
                                # Crear la relación
                                cursor.execute(
                                    "INSERT INTO oferta_habilidad_tecnica (id_oferta, id_habilidad_tecnica) VALUES (%s, %s) ON CONFLICT DO NOTHING;", 
                                    (id_oferta, id_habilidad_tecnica)
                                )
                                print(f"✅ Habilidad técnica asociada: {habilidad}")
                            else:
                                print(f"⚠️ No se encontró la habilidad técnica: {habilidad}")
                        
                        # Procesar como habilidad blanda
                        if es_blanda:
                            # Verificar si existe la habilidad
                            cursor.execute("SELECT id_habilidad_blanda FROM habilidad_blanda WHERE nombre_habilidad_blanda = %s;", (habilidad,))
                            id_result = cursor.fetchone()
                            
                            if id_result:
                                id_habilidad_blanda = id_result[0]
                                # Crear la relación
                                cursor.execute(
                                    "INSERT INTO oferta_habilidad_blanda (id_oferta, id_habilidad_blanda) VALUES (%s, %s) ON CONFLICT DO NOTHING;", 
                                    (id_oferta, id_habilidad_blanda)
                                )
                                print(f"✅ Habilidad blanda asociada: {habilidad}")
                            else:
                                print(f"⚠️ No se encontró la habilidad blanda: {habilidad}")

                # Confirmar transacción
                conn.commit()
                print(f"✅ Registro procesado: {empresa} - {puesto}")
                print("-" * 50)
                
            except Exception as e:
                # Revertir transacción en caso de error
                conn.rollback()
                print(f"❌ Error procesando registro: {e}")
                # Imprimir más detalles para depuración
                import traceback
                traceback.print_exc()

    cursor.close()
    conn.close()
    print("✅ Proceso completado")

except Exception as e:
    print(f"❌ Error general: {e}")
    # Imprimir más detalles para depuración
    import traceback
    traceback.print_exc()