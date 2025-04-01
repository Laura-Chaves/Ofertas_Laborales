-- Requisito de inglés por especialidad 
WITH ofertas_unicas AS (
    -- Identificamos ofertas únicas basadas en su contenido
    SELECT 
        MIN(ol.id_oferta) AS id_oferta,
        esp.nombre_especialidad
    FROM oferta_laboral ol
    JOIN empresa e ON ol.id_empresa = e.id_empresa
    JOIN puesto p ON ol.id_puesto = p.id_puesto
    JOIN especialidad esp ON ol.id_especialidad = esp.id_especialidad
    WHERE esp.nombre_especialidad != 'Otra especialidad'  -- Filtramos "Otra especialidad"
    GROUP BY 
        e.nombre_empresa,
        p.nombre_puesto,
        esp.nombre_especialidad
),
total_por_especialidad AS (
    SELECT 
        nombre_especialidad,
        COUNT(*) AS total
    FROM ofertas_unicas
    GROUP BY nombre_especialidad
),
ingles_por_especialidad AS (
    SELECT 
        ou.nombre_especialidad,
        COUNT(DISTINCT ou.id_oferta) AS con_ingles
    FROM ofertas_unicas ou
    JOIN oferta_idioma oi ON ou.id_oferta = oi.id_oferta
    JOIN idioma i ON oi.id_idioma = i.id_idioma
    WHERE i.nombre_idioma = 'Inglés'
    GROUP BY ou.nombre_especialidad
)
SELECT 
    t.nombre_especialidad,
    t.total AS total_ofertas,
    COALESCE(i.con_ingles, 0) AS ofertas_con_ingles,
    ROUND((COALESCE(i.con_ingles, 0) * 100.0 / t.total), 1) AS porcentaje_ingles
FROM total_por_especialidad t
LEFT JOIN ingles_por_especialidad i ON t.nombre_especialidad = i.nombre_especialidad
ORDER BY porcentaje_ingles DESC;