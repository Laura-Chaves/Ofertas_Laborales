-- Porcentaje de ofertas que exigen inglés
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
total_ofertas AS (
    SELECT COUNT(*) AS total FROM ofertas_unicas
),
ofertas_con_ingles AS (
    SELECT COUNT(DISTINCT ou.id_oferta) AS con_ingles
    FROM ofertas_unicas ou
    JOIN oferta_idioma oi ON ou.id_oferta = oi.id_oferta
    JOIN idioma i ON oi.id_idioma = i.id_idioma
    WHERE i.nombre_idioma = 'Inglés'
)
SELECT 
    (SELECT total FROM total_ofertas) AS total_ofertas,
    (SELECT con_ingles FROM ofertas_con_ingles) AS ofertas_con_ingles,
    ROUND(((SELECT con_ingles FROM ofertas_con_ingles) * 100.0 / 
           (SELECT total FROM total_ofertas)), 1) AS porcentaje_ingles;