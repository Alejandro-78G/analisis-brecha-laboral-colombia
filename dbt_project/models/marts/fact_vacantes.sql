WITH vacantes AS (
    SELECT * FROM {{ ref('stg_vacantes') }}
),
muni AS (
    SELECT * FROM {{ ref('dim_municipio') }}
),
emp AS (
    SELECT * FROM {{ ref('dim_empresa') }}
)

SELECT
    v.id_vacante,
    m.sk_municipio,
    e.sk_empresa,
    v.titulo_vacante,
    v.departamento,
    v.municipio,
    m.region_geografica,
    v.empresa,
    v.nivel_educativo,
    v.salario_min,
    v.salario_max,
    v.salario_promedio,
    v.rango_salarial_categoria,
    v.experiencia_meses,
    v.fecha_publicacion,
    v.fuente_origen
FROM vacantes v
LEFT JOIN muni m ON v.municipio = m.municipio AND v.departamento = m.departamento
LEFT JOIN emp e ON v.empresa = e.nombre_empresa
