import pytest
from pathlib import Path
from src.transformers.schemas import VacanteSchema
from src.loaders.duckdb_loader import DuckDBWarehouseLoader


def test_vacante_schema_validation():
    """
    Verifica que Pydantic v2 normalice textos a mayúsculas y aplique valores por defecto.
    """
    data = {
        "id_vacante": "TEST-001",
        "titulo": "Analista de Datos Senior",
        "departamento": " cundinamarca ",
        "municipio": " bogota ",
        "fuente_origen": "Test Unitario"
    }

    vacante = VacanteSchema(**data)
    assert vacante.departamento == "CUNDINAMARCA"
    assert vacante.municipio == "BOGOTA"
    assert vacante.empresa == "CONFIDENCIAL"
    assert vacante.salario_min is None


def test_duckdb_loader(tmp_path: Path):
    """
    Verifica que DuckDB cree la base de datos temporal y guarde vacantes correctamente.
    """
    test_db = tmp_path / "test_brecha.duckdb"
    loader = DuckDBWarehouseLoader(db_path=test_db)

    vacante = VacanteSchema(
        id_vacante="TEST-99",
        titulo="Ingeniero de Datos",
        empresa="Tech Corp",
        departamento="ANTIOQUIA",
        municipio="MEDELLIN",
        salario_min=4500000.0,
        fuente_origen="Pytest"
    )

    parquet_file = loader.save_vacantes([vacante])
    assert parquet_file.exists()

    summary = loader.get_vacantes_summary()
    assert not summary.empty
    assert summary.iloc[0]["municipio"] == "MEDELLIN"
