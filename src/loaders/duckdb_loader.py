from pathlib import Path
import duckdb
import pandas as pd
from src.core.logger import logger
from src.core.config import settings
from src.transformers.schemas import VacanteSchema, GraduadoSchema


class DuckDBWarehouseLoader:
    """
    Cargador de datos a DuckDB y exportador a formato columnar Apache Parquet.
    Procesa consultas analíticas OLAP a velocidad de milisegundos.
    """

    def __init__(self, db_path: Path | None = None):
        self.db_path = db_path or settings.DUCKDB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        settings.DATA_RAW_PATH.mkdir(parents=True, exist_ok=True)
        settings.DATA_PROCESSED_PATH.mkdir(parents=True, exist_ok=True)

    def get_connection(self) -> duckdb.DuckDBPyConnection:
        return duckdb.connect(str(self.db_path))

    def save_vacantes(self, vacantes: list[VacanteSchema]) -> Path:
        """
        Exporta objetos VacanteSchema a un archivo Parquet e ingesta en la tabla raw_vacantes.
        """
        if not vacantes:
            logger.warning("No hay vacantes para guardar.")
            return settings.DATA_PROCESSED_PATH / "vacantes.parquet"

        # Convertir objetos Pydantic a Pandas DataFrame
        data = [v.model_dump() for v in vacantes]
        df = pd.DataFrame(data)

        # Ruta del archivo Parquet
        parquet_file = settings.DATA_PROCESSED_PATH / "vacantes.parquet"
        df.to_parquet(parquet_file, index=False, engine="pyarrow", compression="snappy")
        logger.info(f"[green][OK] Datos exportados a Apache Parquet en: {parquet_file}[/green]")

        # Cargar en DuckDB
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS raw_vacantes AS 
                SELECT * FROM read_parquet(?);
            """, [str(parquet_file)])

            # Si ya existía, hacer append o reemplazar
            conn.execute("""
                CREATE OR REPLACE TABLE raw_vacantes AS 
                SELECT * FROM read_parquet(?);
            """, [str(parquet_file)])

            count = conn.execute("SELECT COUNT(*) FROM raw_vacantes;").fetchone()[0]
            logger.info(f"[bold green][OK] DuckDB actualizo 'raw_vacantes' con {count} registros.[/bold green]")


        return parquet_file

    def get_vacantes_summary(self) -> pd.DataFrame:
        """
        Retorna un resumen de vacantes agrupadas por departamento y municipio.
        """
        with self.get_connection() as conn:
            df = conn.execute("""
                SELECT 
                    departamento,
                    municipio,
                    COUNT(*) AS total_vacantes,
                    ROUND(AVG(salario_min), 0) AS salario_promedio_min
                FROM raw_vacantes
                GROUP BY departamento, municipio
                ORDER BY total_vacantes DESC;
            """).df()
        return df
