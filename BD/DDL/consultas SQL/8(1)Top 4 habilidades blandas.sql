-- Top 4 habilidades blandas
WITH ofertas_unicas AS (
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
)
SELECT 
    'Habilidades Blandas' AS categoria,
    hb.nombre_habilidad_blanda AS nombre_habilidad,
    COUNT(DISTINCT ou.id_oferta) AS cantidad_ofertas,
    ROUND((COUNT(DISTINCT ou.id_oferta) * 100.0 / (SELECT COUNT(*) FROM ofertas_unicas)), 1) AS porcentaje
FROM ofertas_unicas ou
JOIN oferta_habilidad_blanda ohb ON ou.id_oferta = ohb.id_oferta
JOIN habilidad_blanda hb ON ohb.id_habilidad_blanda = hb.id_habilidad_blanda
GROUP BY categoria, nombre_habilidad
ORDER BY cantidad_ofertas DESC
LIMIT 4;