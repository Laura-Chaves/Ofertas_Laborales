-- Distribución geográfica de ofertas laborales (CABA y Buenos Aires juntas)
WITH ofertas_unicas AS (
    -- Identificamos ofertas únicas basadas en su contenido
    SELECT 
        MIN(ol.id_oferta) AS id_oferta,
        CASE
            WHEN u.ciudad = 'CABA' OR 
                 u.ciudad = 'Ciudad Autónoma de Buenos Aires' OR 
                 u.ciudad LIKE '%Buenos Aires%'
            THEN 'Buenos Aires (CABA)'
            ELSE u.ciudad
        END AS ciudad_normalizada
    FROM oferta_laboral ol
    JOIN empresa e ON ol.id_empresa = e.id_empresa
    JOIN puesto p ON ol.id_puesto = p.id_puesto
    JOIN especialidad esp ON ol.id_especialidad = esp.id_especialidad
    JOIN ubicacion u ON ol.id_ubicacion = u.id_ubicacion
    GROUP BY 
        e.nombre_empresa,
        p.nombre_puesto,
        esp.nombre_especialidad,
        CASE
            WHEN u.ciudad = 'CABA' OR 
                 u.ciudad = 'Ciudad Autónoma de Buenos Aires' OR 
                 u.ciudad LIKE '%Buenos Aires%'
            THEN 'Buenos Aires (CABA)'
            ELSE u.ciudad
        END
)
SELECT 
    ciudad_normalizada AS ciudad,
    COUNT(*) AS cantidad_ofertas,
    ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM ofertas_unicas)), 1) AS porcentaje
FROM ofertas_unicas
WHERE ciudad_normalizada NOT LIKE '%No especificada%'
  AND ciudad_normalizada IS NOT NULL
GROUP BY ciudad_normalizada
ORDER BY cantidad_ofertas DESC
LIMIT 15;