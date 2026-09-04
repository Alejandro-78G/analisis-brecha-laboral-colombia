# 🇨🇴 Análisis de Vacantes Laborales y Brecha de Empleabilidad en Colombia

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![DuckDB](https://img.shields.io/badge/DuckDB-OLAP-yellow.svg)](https://duckdb.org/)
[![Apache Parquet](https://img.shields.io/badge/Apache-Parquet-orange.svg)](https://parquet.apache.org/)
[![Pydantic v2](https://img.shields.io/badge/Pydantic-v2-red.svg)](https://docs.pydantic.dev/)
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

Plataforma de Ingeniería de Datos y Analítica de vanguardia para la extracción asíncrona, validación de esquemas, procesamiento columnar OLAP y análisis espacial de la brecha entre la demanda de vacantes laborales y la oferta de graduados universitarios en Colombia.

---

## 🏗️ Arquitectura de Vanguardia

```mermaid
flowchart TD
    subgraph 1. Extracción & Ingesta (Multi-fuente)
        A1[API Socrata datos.gov.co - SPE] -->|JSON REST API| B[Ingestion Engine]
        A2[Web Scraping - HTTPX + Selectolax] -->|Async Parsing| B
        A3[SNIES - Mineducación] -->|Open Data| B
    end

    subgraph 2. Calidad & Contratos de Datos
        B --> C[Pydantic v2 / Pandera Validation]
        C -->|Schema Validated| D[(Apache Parquet Data Lake)]
    end

    subgraph 3. Processamiento & Storage OLAP
        D --> E[(DuckDB Data Warehouse)]
        E --> F[dbt Analytics Models]
    end

    subgraph 4. Consumo & Analytics
        F --> G[Streamlit App / Power BI Dashboard]
    end
```

---

## ⚡ Stack Tecnológico (Best-in-Class)

- **Gestión de Entorno**: `uv` (Astral - Gestor en Rust 100x más rápido que pip).
- **HTTP & Parsing**: `httpx` + `selectolax` (Parsing en C a velocidad nativa).
- **Data Quality**: `Pydantic v2` para validación estricta de esquemas de datos.
- **Formato Storage**: `Apache Parquet` (Formato columnar hipercomprimido).
- **Data Warehouse**: `DuckDB` (Procesamiento de consultas analíticas en milisegundos).
- **Data Modeling**: `dbt-core` (dbt-duckdb) para la capa dimensional y modelo estrella.

---

## 🚀 Guía de Inicio Rápido

### 1. Requisitos Previos
Tener instalado Python 3.11+ y `uv`.

### 2. Instalación de Dependencias
```bash
# Sincronizar dependencias con uv
uv pip install -e .
```

### 3. Ejecutar el Pipeline ETL Completo
```bash
python -m src.main
```

### 4. Ejecutar Pruebas Unitarias
```bash
pytest tests/
```

---

## 📊 Estrategia de Datos y Fuentes Oficiales

1. **Servicio Público de Empleo (SPE)**: API REST oficial Socrata a través de `datos.gov.co`.
2. **Educación Superior (SNIES)**: Microdatos de graduados por institución y municipio del Ministerio de Educación.
3. **Indicadores DANE**: Información demográfica y tasas de desempleo juvenil.

---
*Desarrollado con estándares de Ingeniería de Software Senior por **Alejandro Cristancho**.*
