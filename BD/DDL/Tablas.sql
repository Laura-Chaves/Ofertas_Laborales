-- ====================================
-- Dimensiones
-- ====================================

-- Tabla Empresa
CREATE TABLE IF NOT EXISTS empresa (
    id_empresa SERIAL PRIMARY KEY,
    nombre_empresa VARCHAR(150) NOT NULL UNIQUE CHECK (nombre_empresa = TRIM(nombre_empresa))
);

-- Tabla Especialidad
CREATE TABLE IF NOT EXISTS especialidad (
    id_especialidad SERIAL PRIMARY KEY,
    nombre_especialidad VARCHAR(150) NOT NULL UNIQUE CHECK (nombre_especialidad = TRIM(nombre_especialidad))
);

-- Tabla Puesto (Títulos largos soportados)
CREATE TABLE IF NOT EXISTS puesto (
    id_puesto SERIAL PRIMARY KEY,
    nombre_puesto VARCHAR(200) NOT NULL UNIQUE CHECK (nombre_puesto = TRIM(nombre_puesto))
);

-- Tabla Ubicación
CREATE TABLE IF NOT EXISTS ubicacion (
    id_ubicacion SERIAL PRIMARY KEY,
    ciudad VARCHAR(100) NOT NULL UNIQUE CHECK (ciudad = TRIM(ciudad))
);

-- Tabla Idioma
CREATE TABLE IF NOT EXISTS idioma (
    id_idioma SERIAL PRIMARY KEY,
    nombre_idioma VARCHAR(50) NOT NULL UNIQUE CHECK (nombre_idioma = TRIM(nombre_idioma))
);

-- Tabla Habilidad Técnica
CREATE TABLE IF NOT EXISTS habilidad_tecnica (
    id_habilidad_tecnica SERIAL PRIMARY KEY,
    nombre_habilidad_tecnica VARCHAR(150) NOT NULL UNIQUE CHECK (nombre_habilidad_tecnica = TRIM(nombre_habilidad_tecnica))
);

-- Tabla Habilidad Blanda
CREATE TABLE IF NOT EXISTS habilidad_blanda (
    id_habilidad_blanda SERIAL PRIMARY KEY,
    nombre_habilidad_blanda VARCHAR(150) NOT NULL UNIQUE CHECK (nombre_habilidad_blanda = TRIM(nombre_habilidad_blanda))
);

-- Tabla Tiempo (Fecha estructurada) - Modificado
CREATE TABLE IF NOT EXISTS tiempo (
    id_tiempo SERIAL PRIMARY KEY,
    dia INT CHECK (dia BETWEEN 1 AND 31),
    mes INT CHECK (mes BETWEEN 1 AND 12),
    anio INT CHECK (anio >= 1900),
    UNIQUE (dia, mes, anio) -- Clave única para evitar fechas duplicadas
);

-- ====================================
-- Tabla de Hechos: Oferta Laboral
-- ====================================
CREATE TABLE IF NOT EXISTS oferta_laboral (
    id_oferta SERIAL PRIMARY KEY,
    id_empresa INT NOT NULL,
    id_puesto INT NOT NULL,
    id_especialidad INT NOT NULL,
    id_ubicacion INT NOT NULL,
    id_tiempo INT, -- Ahora puede ser NULL para fechas desconocidas
    FOREIGN KEY (id_empresa) REFERENCES empresa(id_empresa) ON DELETE CASCADE,
    FOREIGN KEY (id_puesto) REFERENCES puesto(id_puesto) ON DELETE CASCADE,
    FOREIGN KEY (id_especialidad) REFERENCES especialidad(id_especialidad) ON DELETE CASCADE,
    FOREIGN KEY (id_ubicacion) REFERENCES ubicacion(id_ubicacion) ON DELETE CASCADE,
    FOREIGN KEY (id_tiempo) REFERENCES tiempo(id_tiempo) ON DELETE SET NULL
);

-- ====================================
-- Tablas Intermedias
-- ====================================

-- Relación entre ofertas y habilidades técnicas
CREATE TABLE IF NOT EXISTS oferta_habilidad_tecnica (
    id_oferta INT NOT NULL,
    id_habilidad_tecnica INT NOT NULL,
    PRIMARY KEY (id_oferta, id_habilidad_tecnica),
    FOREIGN KEY (id_oferta) REFERENCES oferta_laboral(id_oferta) ON DELETE CASCADE,
    FOREIGN KEY (id_habilidad_tecnica) REFERENCES habilidad_tecnica(id_habilidad_tecnica) ON DELETE CASCADE
);

-- Relación entre ofertas y habilidades blandas
CREATE TABLE IF NOT EXISTS oferta_habilidad_blanda (
    id_oferta INT NOT NULL,
    id_habilidad_blanda INT NOT NULL,
    PRIMARY KEY (id_oferta, id_habilidad_blanda),
    FOREIGN KEY (id_oferta) REFERENCES oferta_laboral(id_oferta) ON DELETE CASCADE,
    FOREIGN KEY (id_habilidad_blanda) REFERENCES habilidad_blanda(id_habilidad_blanda) ON DELETE CASCADE
);

-- Relación entre ofertas y idiomas
CREATE TABLE IF NOT EXISTS oferta_idioma (
    id_oferta INT NOT NULL,
    id_idioma INT NOT NULL,
    PRIMARY KEY (id_oferta, id_idioma),
    FOREIGN KEY (id_oferta) REFERENCES oferta_laboral(id_oferta) ON DELETE CASCADE,
    FOREIGN KEY (id_idioma) REFERENCES idioma(id_idioma) ON DELETE CASCADE
);

-- ====================================
-- Índices para Mejor Rendimiento
-- ====================================
CREATE INDEX idx_oferta_empresa ON oferta_laboral(id_empresa);
CREATE INDEX idx_oferta_puesto ON oferta_laboral(id_puesto);
CREATE INDEX idx_oferta_especialidad ON oferta_laboral(id_especialidad);
CREATE INDEX idx_oferta_ubicacion ON oferta_laboral(id_ubicacion);
CREATE INDEX idx_oferta_tiempo ON oferta_laboral(id_tiempo);

CREATE INDEX idx_habilidad_tecnica ON oferta_habilidad_tecnica(id_habilidad_tecnica);
CREATE INDEX idx_habilidad_blanda ON oferta_habilidad_blanda(id_habilidad_blanda);
CREATE INDEX idx_idioma ON oferta_idioma(id_idioma);
