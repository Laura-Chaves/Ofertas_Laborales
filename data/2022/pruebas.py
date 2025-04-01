import os
from bs4 import BeautifulSoup
import psycopg2
import logging

# Configurar el registro de errores
logging.basicConfig(filename='errores.log', level=logging.ERROR, format='%(asctime)s %(message)s')

# Conexión con la DB
try:
    conn = psycopg2.connect(database="Practicas Academicas",
                            host="localhost",
                            user="postgres",
                            password="123456",
                            port="5432")
    cur = conn.cursor()
    print("Conexión a la base de datos exitosa.")
except Exception as e:
    print(f"Error al conectar con la base de datos: {e}")
    logging.error(f"Error al conectar con la base de datos: {e}")

# Diccionario para convertir los meses a números
meses = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
    "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
    "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
}

# Función para extraer datos básicos desde el HTML
def extraer_datos_basicos(soup):
    try:
        fecha = soup.find('h2').text.strip().replace("\n", " ") if soup.find('h2') else None
        titulo_puesto = soup.find('h4').text.strip() if soup.find('h4') else None
        descripcion = soup.find_all('p')[0].text.strip() if len(soup.find_all('p')) > 0 else None
        print(f"Datos básicos extraídos: Fecha={fecha}, Título={titulo_puesto}")
        return fecha, titulo_puesto, descripcion
    except Exception as e:
        print(f"Error al extraer datos básicos: {e}")
        logging.error(f"Error al extraer datos básicos: {e}")

# Función para extraer y descomponer la fecha en día, mes y año
def procesar_fecha(fecha):
    try:
        if fecha:
            fecha = fecha.replace("\xa0", " ")  # Reemplazar caracteres no separables
            partes_fecha = fecha.split(' ')
            dia = int(partes_fecha[0])
            mes = meses[partes_fecha[2].lower()]
            anio = int(partes_fecha[4])
            print(f"Fecha procesada correctamente: Día={dia}, Mes={mes}, Año={anio}")
            return dia, mes, anio
        return None, None, None
    except Exception as e:
        print(f"Error al procesar la fecha: {e}")
        logging.error(f"Error al procesar la fecha: {e}")

# Función para extraer datos adicionales desde el HTML
def extraer_datos_adicionales(soup):
    try:
        tipo_empresa = soup.find('p', string=lambda x: 'Empresa' in x).text.strip() if soup.find('p', string=lambda x: 'Empresa' in x) else "Empresa no especificada"
        especialidad = soup.find('p', string=lambda x: 'Especialidad' in x).text.strip() if soup.find('p', string=lambda x: 'Especialidad' in x) else "Especialidad no especificada"
        region = soup.find('p', string=lambda x: 'Región' in x).text.strip() if soup.find('p', string=lambda x: 'Región' in x) else "Región no especificada"
        
        # Descomponer región en provincia y ciudad
        if region and ', ' in region:
            provincia, ciudad = region.split(', ')
        else:
            provincia, ciudad = "Provincia no especificada", "Ciudad no especificada"
        
        idioma = soup.find('p', string=lambda x: 'Idioma' in x).text.strip() if soup.find('p', string=lambda x: 'Idioma' in x) else "Idioma no especificado"
        habilidad_tecnica = soup.find('p', string=lambda x: 'Habilidad técnica' in x).text.strip() if soup.find('p', string=lambda x: 'Habilidad técnica' in x) else "Habilidad técnica no especificada"
        habilidad_blanda = soup.find('p', string=lambda x: 'Habilidad blanda' in x).text.strip() if soup.find('p', string=lambda x: 'Habilidad blanda' in x) else "Habilidad blanda no especificada"
        
        print(f"Datos adicionales extraídos: Empresa={tipo_empresa}, Especialidad={especialidad}, Región={provincia}, {ciudad}, Idioma={idioma}")
        return tipo_empresa, especialidad, provincia, ciudad, idioma, habilidad_tecnica, habilidad_blanda
    except Exception as e:
        print(f"Error al extraer datos adicionales: {e}")
        logging.error(f"Error al extraer datos adicionales: {e}")
        return "Empresa no especificada", "Especialidad no especificada", "Provincia no especificada", "Ciudad no especificada", "Idioma no especificado", "Habilidad técnica no especificada", "Habilidad blanda no especificada"

# Función para insertar datos en las dimensiones
def insertar_dimension(cur, query, valor):
    try:
        cur.execute(query, (valor,))
        return cur.fetchone()[0] if cur.rowcount > 0 else None
    except Exception as e:
        print(f"Error al insertar en la dimensión: {e}")
        logging.error(f"Error al insertar en la dimensión: {e}")

# Función para insertar datos en la tabla de hechos
def insertar_en_hechos(cur, empresa_id, especialidad_id, puesto_id, tiempo_id, region_id, idioma_id, habilidad_tecnica_id, habilidad_blanda_id):
    try:
        cur.execute("""
            INSERT INTO hecho_ofertas_laborales (
                empresa_id, especialidad_id, puesto_id, tiempo_id, 
                region_id, idioma_id, habilidad_tecnica_id, habilidad_blanda_id, numero_de_ofertas
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (empresa_id, especialidad_id, puesto_id, tiempo_id, region_id, idioma_id, habilidad_tecnica_id, habilidad_blanda_id, 1))
        print("Datos insertados en la tabla de hechos.")
    except Exception as e:
        print(f"Error al insertar en la tabla de hechos: {e}")
        logging.error(f"Error al insertar en la tabla de hechos: {e}")

# Ruta de la carpeta donde están los archivos HTML
ruta_carpeta = "C:/Users/Anhi Lari/Documents/Lari/2do TUPED/Practicas Academicas/Archivoshtml_practicas/2022"

# Listar todos los archivos HTML en la carpeta
archivos_html = [archivo for archivo in os.listdir(ruta_carpeta) if archivo.endswith(".html")]

try:
    # Iterar sobre todos los archivos HTML
    for archivo in archivos_html:
        print(f"Procesando archivo: {archivo}")
        ruta_archivo = os.path.join(ruta_carpeta, archivo)
        
        # Abrir y procesar cada archivo HTML
        with open(ruta_archivo, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")
            
            # Extraer los datos básicos y fecha
            fecha, titulo_puesto, descripcion = extraer_datos_basicos(soup)
            dia, mes, anio = procesar_fecha(fecha)

            # Extraer datos adicionales (empresa, especialidad, región, etc.)
            tipo_empresa, especialidad, provincia, ciudad, idioma, habilidad_tecnica, habilidad_blanda = extraer_datos_adicionales(soup)

            # Insertar datos en las dimensiones
            empresa_id = insertar_dimension(cur, "INSERT INTO dimension_empresa (tipo_empresa) VALUES (%s) ON CONFLICT DO NOTHING RETURNING empresa_id;", tipo_empresa)
            especialidad_id = insertar_dimension(cur, "INSERT INTO dimension_especialidad (nombre_espe) VALUES (%s) ON CONFLICT DO NOTHING RETURNING especialidad_id;", especialidad)
            puesto_id = insertar_dimension(cur, "INSERT INTO dimension_puesto (puesto) VALUES (%s) ON CONFLICT DO NOTHING RETURNING puesto_id;", titulo_puesto)
            tiempo_id = insertar_dimension(cur, "INSERT INTO dimension_tiempo (fecha, dia, mes, anio) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING RETURNING tiempo_id;", fecha)
            region_id = insertar_dimension(cur, "INSERT INTO dimension_region (provincia, ciudad) VALUES (%s, %s) ON CONFLICT DO NOTHING RETURNING region_id;", provincia)
            idioma_id = insertar_dimension(cur, "INSERT INTO dimension_idioma (idioma) VALUES (%s) ON CONFLICT DO NOTHING RETURNING idioma_id;", idioma)
            habilidad_tecnica_id = insertar_dimension(cur, "INSERT INTO dimension_habilidad_tecnica (habilidad_tecnica) VALUES (%s) ON CONFLICT DO NOTHING RETURNING habilidad_tecnica_id;", habilidad_tecnica)
            habilidad_blanda_id = insertar_dimension(cur, "INSERT INTO dimension_habilidad_blanda (habilidad_blanda) VALUES (%s) ON CONFLICT DO NOTHING RETURNING habilidad_blanda_id;", habilidad_blanda)

            # Insertar en la tabla de hechos
            insertar_en_hechos(cur, empresa_id, especialidad_id, puesto_id, tiempo_id, region_id, idioma_id, habilidad_tecnica_id, habilidad_blanda_id)

    # Confirmar los cambios en la base de datos
    conn.commit()

    # Verificar datos en la tabla hecho_ofertas_laborales
    cur.execute("SELECT * FROM hecho_ofertas_laborales;")
    registros = cur.fetchall()
    print("\nDatos en hecho_ofertas_laborales:")
    for registro in registros:
        print(f"ID: {registro[0]}, Empresa ID: {registro[1]}, Especialidad ID: {registro[2]}, Puesto ID: {registro[3]}, Tiempo ID: {registro[4]}, Region ID: {registro[5]}, Idioma ID: {registro[6]}, Habilidad Técnica ID: {registro[7]}, Habilidad Blanda ID: {registro[8]}, Número de Ofertas: {registro[9]}")

except Exception as e:
    logging.error(f"Error procesando archivo {archivo}: {str(e)}")

finally:
    # Cerrar el cursor y la conexión
    cur.close()
    conn.close()
    print("Conexión cerrada correctamente.")
