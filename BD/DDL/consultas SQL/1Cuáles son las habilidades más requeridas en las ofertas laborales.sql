-- Habilidades más requeridas (técnicas y blandas combinadas)
WITH ofertas_unicas AS (
    -- Identificamos ofertas únicas basadas en su contenido
    SELECT 
        MIN(ol.id_oferta) AS id_oferta
    FROM oferta_laboral ol
    JOIN empresa e ON ol.id_empresa = e.id_empresa
    JOIN puesto p ON ol.id_puesto = p.id_puesto
    JOIN especialidad esp ON ol.id_especialidad = esp.id_especialidad
    GROUP BY 
        e.nombre_empresa,
        p.nombre_puesto,
        esp.nombre_especialidad
),
habilidades_tecnicas AS (
    -- Contamos habilidades técnicas
    SELECT 
        'Técnica' AS tipo_habilidad,
        ht.nombre_habilidad_tecnica AS nombre_habilidad,
        COUNT(DISTINCT ou.id_oferta) AS cantidad_ofertas,
        ROUND((COUNT(DISTINCT ou.id_oferta) * 100.0 / (SELECT COUNT(*) FROM ofertas_unicas)), 1) AS porcentaje
    FROM ofertas_unicas ou
    JOIN oferta_habilidad_tecnica oht ON ou.id_oferta = oht.id_oferta
    JOIN habilidad_tecnica ht ON oht.id_habilidad_tecnica = ht.id_habilidad_tecnica
    GROUP BY tipo_habilidad, nombre_habilidad
),
habilidades_blandas AS (
    -- Contamos habilidades blandas
    SELECT 
        'Blanda' AS tipo_habilidad,
        hb.nombre_habilidad_blanda AS nombre_habilidad,
        COUNT(DISTINCT ou.id_oferta) AS cantidad_ofertas,
        ROUND((COUNT(DISTINCT ou.id_oferta) * 100.0 / (SELECT COUNT(*) FROM ofertas_unicas)), 1) AS porcentaje
    FROM ofertas_unicas ou
    JOIN oferta_habilidad_blanda ohb ON ou.id_oferta = ohb.id_oferta
    JOIN habilidad_blanda hb ON ohb.id_habilidad_blanda = hb.id_habilidad_blanda
    GROUP BY tipo_habilidad, nombre_habilidad
)
-- Combinamos ambos tipos y mostramos las más solicitadas
SELECT * FROM (
    SELECT * FROM habilidades_tecnicas
    UNION ALL
    SELECT * FROM habilidades_blandas
) AS todas_habilidades
ORDER BY cantidad_ofertas DESC
LIMIT 20;