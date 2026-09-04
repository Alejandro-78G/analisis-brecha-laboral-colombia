WITH source AS (
    SELECT * FROM raw_vacantes
),

renamed AS (
    SELECT
        UPPER(TRIM(id_vacante)) AS id_vacante,
        TRIM(titulo) AS titulo_vacante,
        UPPER(TRIM(COALESCE(empresa, 'CONFIDENCIAL'))) AS empresa,
        UPPER(TRIM(COALESCE(departamento, 'COLOMBIA'))) AS departamento,
        UPPER(TRIM(COALESCE(municipio, 'BOGOTA'))) AS municipio,
        COALESCE(salario_min, 1300000) AS salario_min,
        COALESCE(salario_max, salario_min, 3500000) AS salario_max,
        (COALESCE(salario_min, 1300000) + COALESCE(salario_max, 3500000)) / 2.0 AS salario_promedio,
        COALESCE(experiencia_meses, 0) AS experiencia_meses,
        UPPER(TRIM(COALESCE(nivel_educativo, 'PROFESIONAL'))) AS nivel_educativo,
        descripcion,
        fecha_publicacion,
        fuente_origen,

        CASE 
            WHEN (COALESCE(salario_min, 1300000) + COALESCE(salario_max, 3500000)) / 2.0 < 2000000 THEN 'Entrada / Junior (< 2M)'
            WHEN (COALESCE(salario_min, 1300000) + COALESCE(salario_max, 3500000)) / 2.0 BETWEEN 2000000 AND 4500000 THEN 'Medio / Semi-Senior (2M - 4.5M)'
            WHEN (COALESCE(salario_min, 1300000) + COALESCE(salario_max, 3500000)) / 2.0 BETWEEN 4500001 AND 7500000 THEN 'Senior / Liderazgo (4.5M - 7.5M)'
            ELSE 'Ejecutivo / Direccion (> 7.5M)'
        END AS rango_salarial_categoria

    FROM source
)

SELECT * FROM renamed
