-- Ofertas en CABA/Buenos Aires (sin duplicados)
WITH ofertas_unicas AS (
    -- Identificamos ofertas únicas basadas en su contenido
    SELECT 
        MIN(ol.id_oferta) AS id_oferta,
        p.nombre_puesto,
        esp.nombre_especialidad,
        u.ciudad,  -- Incluimos la ciudad original
        t.mes,
        t.dia
    FROM oferta_laboral ol
    JOIN empresa e ON ol.id_empresa = e.id_empresa
    JOIN puesto p ON ol.id_puesto = p.id_puesto
    JOIN especialidad esp ON ol.id_especialidad = esp.id_especialidad
    JOIN ubicacion u ON ol.id_ubicacion = u.id_ubicacion
    JOIN tiempo t ON ol.id_tiempo = t.id_tiempo
    WHERE u.ciudad = 'CABA' 
       OR u.ciudad = 'Ciudad Autónoma de Buenos Aires'
       OR u.ciudad LIKE '%Buenos Aires%'
    GROUP BY 
        p.nombre_puesto,
        esp.nombre_especialidad,
        u.ciudad,
        t.mes,
        t.dia
)
SELECT 
    id_oferta,
    'Buenos Aires (CABA)' AS ubicacion,  -- Mostramos ubicación normalizada
    nombre_puesto,
    nombre_especialidad,
    CASE  -- Mostramos el nombre del mes en lugar del número
        WHEN mes = 1 THEN 'Enero'
        WHEN mes = 2 THEN 'Febrero'
        WHEN mes = 3 THEN 'Marzo'
        WHEN mes = 4 THEN 'Abril'
        WHEN mes = 5 THEN 'Mayo'
        WHEN mes = 6 THEN 'Junio'
        WHEN mes = 7 THEN 'Julio'
        WHEN mes = 8 THEN 'Agosto'
        WHEN mes = 9 THEN 'Septiembre'
        WHEN mes = 10 THEN 'Octubre'
        WHEN mes = 11 THEN 'Noviembre'
        WHEN mes = 12 THEN 'Diciembre'
    END AS mes_nombre,
    dia,
    COUNT(*) OVER (PARTITION BY mes) AS ofertas_por_mes
FROM ofertas_unicas
ORDER BY mes, dia;