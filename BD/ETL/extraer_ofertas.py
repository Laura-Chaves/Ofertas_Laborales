import os
import re
import csv
from bs4 import BeautifulSoup
from unidecode import unidecode

#====================================================
# 🔹 Diccionarios y listas para almacenar entidades y relaciones
#====================================================

empresas = {}
puestos = {}
ubicaciones = {}
idiomas_almacenados = {}
habilidades_tecnicas = {}
habilidades_blandas = {}
especialidades = {}
tiempos = {}

ofertas_laborales = []
oferta_habilidad_tecnica = []
oferta_habilidad_blanda = []
oferta_idioma = []

# =========================================
# 🔹 Carpeta donde están los archivos HTML
# =========================================
carpeta_ofertas = "data/2022"
archivo_csv = "ofertas_laborales.csv"

if not os.path.exists(carpeta_ofertas):
    print(f"❌ La carpeta '{carpeta_ofertas}' no existe. Verifica la ruta.")
    exit()


#=========================================
# 🔹 Lista de palabras vacías (para limpiar textos)
#=========================================

palabras_a_descartar = [
    "si", "para", "como", "a", "de", "y", "o", "con", "por", "el", "la", "en", "los", "las", "que", "un", "una",
    "su", "del", "al", "se", "más", "es", "son", "no", "sobre", "entre", "hasta"
]

lista_especialidades = ["Licenciado/a Bioinformático","Lic. Bioinformatico","Bioinformática","Licenciado/a","Licendiado","Licenciada", "Bioingeniero/a","Bioingeniero","Bioingeniera","Bioingeniería","Ingeniería Biomédica"
                        "Biotecnología","Ingeniería", "Ingeniero","Ingeniero en Transporte", "Ing. en Transporte","Técnico","Tecnico","Tecnico en Procesamiento de Datos","Ciencia de Datos","Desarrollo de Software"]

mapeo_habilidades = {
    # Habilidades técnicas
    "informática": "Técnica",
    "programación": "Técnica",
    "software": "Técnica",
    "bases de datos": "Técnica",
    "sql": "Técnica",
    "python": "Técnica",
    "c": "Técnica",
    "c++": "Técnica",
    "powerbi": "Técnica",
    "ingenieria biomédica": "Técnica",
    "bioingeniero": "Técnica",
    "bioinformático": "Técnica",
    "técnico": "Técnica",
    "ingeniero": "Técnica",
    "licenciado": "Técnica",
    "analista": "Técnica",
    "desarrollador": "Técnica",
    "autocad": "Técnica",
    "curso auditor": "Técnica",
    "herramientas informáticas": "Técnica",
    "herramientas de electrónica": "Técnica",
    "manejo de herramientas de oficina": "Técnica",
    "manejo de equipos": "Técnica",
    "iso 9000": "Técnica",
    "iso 13485": "Técnica",
    "redes": "Técnica",
    "manejo maquinarias": "Técnica",
    "manejo de maquinaria de estetica": "Técnica",
    "manejo de maquinaria industrial": "Técnica",
    "manejo de maquinaria agrícola": "Técnica",
    "manejo de maquinaria hospitalaria": "Técnica",
    "planos esquemáticos": "Técnica",
    "manejo de técnicas estadísticas": "Técnica",
    "reparación de equipos": "Técnica",
    "experiencia en reparación de equipos": "Técnica",
    
    # Habilidades blandas
    "experiencia": "Blanda",
    "comunicación": "Blanda",
    "trabajo en equipo": "Blanda",
    "liderazgo": "Blanda",
    "empatía": "Blanda",
    "proactividad": "Blanda",
    "capacidad de gestión": "Blanda",
    "perfil comercial": "Blanda",
    "trabajo interdisciplinario": "Blanda",
    "capacidad de análisis": "Blanda",
    "capacidad de organización": "Blanda",
    "capacidad de resolución de problemas": "Blanda",
    "capacidad de aprendizaje": "Blanda",
    "capacidad de adaptación": "Blanda",
    "capacidad de trabajo bajo presión": "Blanda",
    "capacidad de comunicación": "Blanda",
    "capacidad de liderazgo": "Blanda",
    "capacidad de negociación": "Blanda",
    "capacidad de planificación": "Blanda",
    "orientación al cliente": "Blanda",
    "orientación a resultados": "Blanda",
    "resolución de problemas": "Blanda",
    "docencia": "Blanda",
    "disponibilidad horaria": "Blanda",
    "disponibilidad para viajar": "Blanda"
}


# Lista de frases irrelevantes para filtrar
frases_ignoradas = [
    "Búsquedas Laborales FIUNER",
    "Facultad de Ingeniería - Universidad Nacional de Entre Ríos",
    "contacto@ingenieria", 
    "Tel:", 
    "Se distribuye a más de", 
    "© Copyright"
]
#===================================================
# 🔹 Lista ampliada de ciudades de Argentina y países limítrofes
#===================================================
ciudades = [

    # Buenos Aires
    "AMBA", "Buenos Aires", "La Plata", "Mar del Plata", "Bahía Blanca", "Tandil", "San Nicolás", "Pergamino", "Olavarría",
    # CABA
    "CABA", "Ciudad Autónoma de Buenos Aires",
    # Córdoba
    "Córdoba", "Cordoba", "Villa Carlos Paz", "Río Cuarto", "Villa María", "Alta Gracia", "San Francisco",
    # Santa Fe
    "Rosario", "Santa Fe", "Rafaela", "Venado Tuerto", "Reconquista", "Villa Gobernador Gálvez",
    # Mendoza
    "Mendoza", "San Rafael", "Godoy Cruz", "Maipú", "Las Heras",
    # Entre Ríos
    "Paraná", "Concordia", "Gualeguaychú", "Gualeguay", "Victoria", "Colón", "Diamante", "Oro Verde"
    # Salta
    "Salta", "Tartagal", "Cafayate", "Orán", "San Ramón de la Nueva Orán",
    # Tucumán
    "San Miguel de Tucumán", "Yerba Buena", "Tafí Viejo", "Concepción", "Monteros",
    # Neuquén
    "Neuquén", "San Martín de los Andes", "Villa La Angostura", "Zapala",
    # Río Negro
    "Viedma", "San Carlos de Bariloche", "General Roca", "Cipolletti",
    # Chaco
    "Resistencia", "Roque Sáenz Peña", "Villa Ángela", "Charata",
    # Misiones
    "Posadas", "Eldorado", "Oberá", "Puerto Iguazú",
    # Corrientes
    "Corrientes", "Goya", "Paso de los Libres", "Mercedes",
    # Chubut
    "Rawson", "Comodoro Rivadavia", "Trelew", "Puerto Madryn",
    # Jujuy
    "San Salvador de Jujuy", "Palpalá", "Libertador General San Martín",
    # San Juan
    "San Juan", "Rivadavia", "Chimbas", "Pocito",
    # San Luis
    "San Luis", "Villa Mercedes", "La Punta",
    # Catamarca
    "San Fernando del Valle de Catamarca", "Belén", "Tinogasta",
    # La Rioja
    "La Rioja", "Chilecito",
    # Santa Cruz
    "Río Gallegos", "Caleta Olivia", "El Calafate",
    # Tierra del Fuego
    "Ushuaia", "Río Grande",
    # Formosa
    "Formosa", "Clorinda",
    # La Pampa
    "Santa Rosa", "General Pico",
    # Santiago del Estero
    "Santiago del Estero", "La Banda", "Termas de Río Hondo",
    # Países Limítrofes
    # Bolivia
    "Bolivia", "La Paz", "Cochabamba", "Santa Cruz", "Sucre", "Oruro", "Potosí", "Tarija",
    # Chile
    "Chile", "Santiago", "Valparaíso", "Concepción", "La Serena", "Antofagasta", "Temuco", "Rancagua", "Iquique", "Punta Arenas",
    # Paraguay
    "Paraguay", "Asunción", "Ciudad del Este", "Encarnación", "San Lorenzo", "Luque",
    # Uruguay
    "Uruguay", "Montevideo", "Salto", "Paysandú", "Maldonado", "Rivera", "Canelones",
    # Brasil
    "Brasil", "Sao Paulo", "Rio de Janeiro", "Brasilia", "Porto Alegre", "Curitiba", "Florianópolis", "Recife", "Fortaleza"
]

# Lista de idiomas comunes
idiomas = ["Inglés", "Español", "Francés", "Portugués", "Alemán", "Italiano", "Chino", "Japonés"]

# ===========================================
# 🔹 Funciones de Extracción y Limpieza
# ===========================================

def extraer_titulos_puesto(soup):
    """ Extrae todos los títulos de puesto encontrados. """
    titulos = [h4.get_text(strip=True) for h4 in soup.find_all('h4')]
    return titulos if titulos else ["Puesto no especificado"]

def extraer_empresa(soup):
    """ Extrae el nombre de la empresa evitando capturar frases irrelevantes. """
    texto = soup.get_text().replace("\n", " ")  # Quitamos saltos de línea innecesarios
    
    # Patrones mejorados para detectar nombres de empresa
    patrones_empresa = [
        r'(?:Empresa|Instituto|Organización|Laboratorio|Fundación|Universidad|Institución|Compañía)\s*[:\-]?\s*([A-Z][\w\s&.,-]+)',
        r'busca\s+([A-Z][\w\s&.,-]+)',   # "Se busca X"
        r'convoca\s+([A-Z][\w\s&.,-]+)', # "Convoca a X"
        r'ofrece\s+([A-Z][\w\s&.,-]+)',  # "Ofrece X"
        r'para\s+([A-Z][\w\s&.,-]+)',    # "Para empresa X"
    ]

    for patron in patrones_empresa:
        match = re.search(patron, texto, re.IGNORECASE)
        if match:
            empresa = match.group(1).strip()
            if 2 < len(empresa.split()) < 7:  # Aseguramos que no sea una frase demasiado larga
                return empresa

    return "Empresa no especificada"


def extraer_ciudad(texto):
    """ Busca ciudades en el texto y devuelve la primera encontrada. """
    for ciudad in ciudades:
        if re.search(rf"\b{ciudad}\b", texto, re.IGNORECASE):
            return ciudad
    return "Ciudad no especificada"

def extraer_fecha(soup):
    """Busca la fecha de publicación en el texto y la devuelve en formato limpio."""
    match = re.search(r'\d{1,2}\s+de\s+\w+\s+de\s+\d{4}', soup.get_text())
    return match.group(0).replace("\n", " ") if match else "Fecha no especificada"


def extraer_especialidad(texto):
    """ Busca especialidades en el texto y devuelve la primera encontrada. """
    for especialidad in lista_especialidades:
        if re.search(rf"\b{especialidad}\b", texto, re.IGNORECASE):
            return especialidad
    return "Especialidad no especificada"

def extraer_idioma(texto):
    """ Busca idiomas mencionados en el texto y devuelve el primero encontrado. """
    for idioma in idiomas:
        if re.search(rf"\b{idioma}\b", texto, re.IGNORECASE):
            return idioma
    return "Idioma no especificado"


def extraer_habilidades(texto):
    """ Extrae habilidades técnicas y blandas, evitando falsos positivos. """
    habilidades_detectadas = []
    texto_limpio = unidecode(texto.lower())

    # Identifica secciones clave donde suelen mencionarse habilidades
    secciones = re.findall(
        r'(?:requisitos|habilidades|perfil requerido|conocimientos requeridos):([\s\S]+?)(?:\n[A-Z]|\Z)',
        texto_limpio,
        re.IGNORECASE
    )
    contenido_relevante = " ".join(secciones) if secciones else " ".join(texto_limpio.split()[:500])

    for patron, tipo in mapeo_habilidades.items():
        if patron in ["c", "c++"]:
            # Solo acepta si están bien delimitadas (no parte de otra palabra)
            if re.search(rf"\b{patron}\b", contenido_relevante):  
                habilidades_detectadas.append((patron, tipo))
        else:
            if re.search(rf"\b{re.escape(patron)}\b", contenido_relevante):
                habilidades_detectadas.append((patron, tipo))

    return habilidades_detectadas if habilidades_detectadas else [("Habilidades no especificadas", "N/A")]


# =========================================
# 🔹 Función para extraer datos de un HTML
# =========================================

def procesar_html(ruta_archivo):
    print(f"📄 Procesando: {ruta_archivo}")

    try:
        with open(ruta_archivo, 'r', encoding='utf-8', errors='ignore') as archivo:
            contenido_html = archivo.read()

        if not contenido_html.strip():
            print(f"⚠️ Archivo vacío, omitiendo: {ruta_archivo}")
            return None  # 🔹 Ahora devolvemos None si el archivo está vacío

        soup = BeautifulSoup(contenido_html, 'html.parser')
        texto_completo = soup.get_text(separator=" ").lower()

        # 🔹 Extraer empresa
        patrones_empresa = [
            r"(?:empresa|instituto|organización|laboratorio|fundación|universidad|institución|compañía|beca|posgrado|vacante|oferta)[:\s]?([\w\s&.,-]+)",
            r"buscamos ([A-Z][\w\s&.,-]+)",  
            r"convoca a ([A-Z][\w\s&.,-]+)",  
            r"para empresa ([A-Z][\w\s&.,-]+)",  
            r"se solicita en ([A-Z][\w\s&.,-]+)",  
        ]
        empresa = "No especificada"
        for patron in patrones_empresa:
            match = re.search(patron, texto_completo, re.IGNORECASE)
            if match:
                empresa = match.group(1).strip().title()
                empresa = " ".join(empresa.split()[:5])  # Limitar a 5 palabras
                break

        # 🔹 Extraer ciudad
        ciudad = next((c for c in ciudades if re.search(rf"\b{c.lower()}\b", texto_completo)), "No especificada")

        # 🔹 Extraer fecha
        patrones_fecha = [
            r"(\d{1,2} de [a-z]+ de \d{4})",  # "4 de octubre de 2022"
            r"(\d{1,2}/\d{1,2}/\d{4})",  # "29/9/2022"
            r"(\d{4}-\d{2}-\d{2})"  # "2022-10-04"
        ]
        fecha = "No especificada"
        for patron in patrones_fecha:
            match_fecha = re.search(patron, texto_completo, re.IGNORECASE)
            if match_fecha:
                fecha = match_fecha.group(0)
                break

        # 🔹 Extraer título del puesto
        titulo_puesto = soup.find('h4').get_text(strip=True) if soup.find('h4') else "No especificado"

        # 🔹 Extraer habilidades
        habilidades_encontradas = []
        for habilidad, tipo in mapeo_habilidades.items():
            if habilidad in texto_completo:
                habilidades_encontradas.append(f"{habilidad} ({tipo})")

        # 🔹 Devolver los datos como una tupla
        return [empresa, titulo_puesto, ciudad, fecha, ", ".join(habilidades_encontradas)]

    except Exception as e:
        print(f"❌ Error procesando {ruta_archivo}: {e}")
        return None  # 🔹 Devuelve None si hay un error

# =========================================
# 🔹 Procesar archivos HTML y guardar en CSV
# =========================================

datos_extraidos = []

# 🔹 Procesar archivos HTML
for archivo in os.listdir(carpeta_ofertas):
    if archivo.endswith(".html"):
        datos = procesar_html(os.path.join(carpeta_ofertas, archivo))
        if datos:  # 🔹 Solo añadir si datos no es None
            datos_extraidos.append(datos)

# 🔹 Guardar en CSV
with open(archivo_csv, "w", newline="", encoding="utf-8") as csvfile:
    escritor = csv.writer(csvfile)
    
    # 🔹 Escribir encabezados
    escritor.writerow(["Empresa", "Puesto", "Ciudad", "Fecha", "Habilidades"])  
    
    # 🔹 Escribir filas de datos
    escritor.writerows(datos_extraidos)

print(f"✅ Archivo CSV generado: {archivo_csv}")