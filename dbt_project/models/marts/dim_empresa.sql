WITH stg AS (
    SELECT DISTINCT
        empresa
    FROM {{ ref('stg_vacantes') }}
)

SELECT
    ROW_NUMBER() OVER (ORDER BY empresa) AS sk_empresa,
    empresa AS nombre_empresa
FROM stg
