-- Top 4 habilidades técnicas
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
    'Habilidades Técnicas' AS categoria,
    ht.nombre_habilidad_tecnica AS nombre_habilidad,
    COUNT(DISTINCT ou.id_oferta) AS cantidad_ofertas,
    ROUND((COUNT(DISTINCT ou.id_oferta) * 100.0 / (SELECT COUNT(*) FROM ofertas_unicas)), 1) AS porcentaje
FROM ofertas_unicas ou
JOIN oferta_habilidad_tecnica oht ON ou.id_oferta = oht.id_oferta
JOIN habilidad_tecnica ht ON oht.id_habilidad_tecnica = ht.id_habilidad_tecnica
GROUP BY categoria, nombre_habilidad
ORDER BY cantidad_ofertas DESC
LIMIT 4;