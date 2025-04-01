WITH ofertas_unicas AS (
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
    o.ciudad_normalizada AS ciudad,
    COUNT(*) AS cantidad_ofertas,
    ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM ofertas_unicas)), 1) AS porcentaje,
    c.latitud,
    c.longitud
FROM ofertas_unicas o
LEFT JOIN (
    SELECT 'Buenos Aires (CABA)' AS ciudad, -34.6037 AS latitud, -58.3816 AS longitud UNION ALL
    SELECT 'Córdoba', -31.4201, -64.1888 UNION ALL
    SELECT 'Rosario', -32.9468, -60.6393 UNION ALL
    SELECT 'Santa Fe', -31.6333, -60.7000 UNION ALL
    SELECT 'Corrientes', -27.4806, -58.8341 UNION ALL
    SELECT 'Paraná', -31.7310, -60.5238 UNION ALL
    SELECT 'Bolivia', -16.2902, -63.5887 UNION ALL
    SELECT 'Chile', -33.4489, -70.6693 UNION ALL
    SELECT 'AMBA', -34.6000, -58.5000 UNION ALL
    SELECT 'Tandil', -37.3217, -59.1332 UNION ALL
    SELECT 'Formosa', -26.1849, -58.1731 UNION ALL
    SELECT 'Neuquén', -38.9516, -68.0591 UNION ALL
    SELECT 'Posadas', -27.3671, -55.8960 UNION ALL
    SELECT 'San Miguel de Tucumán', -26.8083, -65.2176
) c ON o.ciudad_normalizada = c.ciudad
WHERE o.ciudad_normalizada NOT LIKE '%No especificada%'
  AND o.ciudad_normalizada IS NOT NULL
GROUP BY o.ciudad_normalizada, c.latitud, c.longitud
ORDER BY cantidad_ofertas DESC
LIMIT 6;
