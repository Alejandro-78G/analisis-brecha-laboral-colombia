WITH stg AS (
    SELECT DISTINCT
        municipio,
        departamento
    FROM {{ ref('stg_vacantes') }}
)

SELECT
    ROW_NUMBER() OVER (ORDER BY departamento, municipio) AS sk_municipio,
    municipio,
    departamento,
    CASE 
        WHEN departamento IN ('CUNDINAMARCA', 'BOYACA', 'TOLIMA', 'HUILA') THEN 'Centro / Andina'
        WHEN departamento IN ('ANTIOQUIA', 'CALDAS', 'RISARALDA', 'QUINDIO') THEN 'Eje Cafetero & Antioquia'
        WHEN departamento IN ('ATLANTICO', 'BOLIVAR', 'MAGDALENA', 'CORDOBA', 'SUCRE', 'CESAR', 'LA GUAJIRA') THEN 'Caribe'
        WHEN departamento IN ('VALLE DEL CAUCA', 'CAUCA', 'NARIÑO', 'CHOCO') THEN 'Pacífico'
        WHEN departamento IN ('SANTANDER', 'NORTE DE SANTANDER') THEN 'Nororiente'
        ELSE 'Orinoquía & Amazonía'
    END AS region_geografica
FROM stg
