import sys
import asyncio
import pandas as pd
from rich.console import Console

from rich.table import Table
from src.core.logger import logger
from src.extractors.spe_api import SPEDataGovExtractor
from src.extractors.async_scraper import FastWebScraper
from src.loaders.duckdb_loader import DuckDBWarehouseLoader

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

console = Console(force_terminal=True)


async def run_pipeline():
    console.print("\n[bold magenta]=====================================================[/bold magenta]")
    console.print("[bold cyan]PIPELINE DE INGENIERIA DE DATOS - BRECHA LABORAL COLOMBIA[/bold cyan]")
    console.print("[bold magenta]=====================================================[/bold magenta]\n")

    # 1. Extracción de API Oficial (datos.gov.co)
    spe_extractor = SPEDataGovExtractor()
    spe_vacantes = await spe_extractor.extract(limit=2500)

    # 2. Extracción de Web Scraping Asíncrono a nivel nacional
    scraper = FastWebScraper()
    web_vacantes = await scraper.extract(limit=2500)

    # Consolidación de registros validados
    todas_vacantes = spe_vacantes + web_vacantes
    logger.info(f"[bold yellow]Total vacantes validadas consolidada a nivel nacional: {len(todas_vacantes)}[/bold yellow]")

    # 3. Almacenamiento en Parquet y DuckDB
    loader = DuckDBWarehouseLoader()
    parquet_path = loader.save_vacantes(todas_vacantes)

    # 4. Consulta Analítica OLAP con DuckDB
    summary_df = loader.get_vacantes_summary()

    # Presentación visual con Rich Table
    table = Table(title="Resumen Nacional de Vacantes por Ciudad (DuckDB OLAP Engine - Top 20)")
    table.add_column("Departamento", style="cyan")
    table.add_column("Municipio", style="magenta")
    table.add_column("Total Vacantes", justify="right", style="green")
    table.add_column("Salario Promed. Min (COP)", justify="right", style="yellow")

    for _, row in summary_df.head(20).iterrows():
        salario = f"${row['salario_promedio_min']:,.0f}" if pd.notnull(row['salario_promedio_min']) and str(row['salario_promedio_min']) != 'nan' else "N/A"
        table.add_row(
            str(row["departamento"]),
            str(row["municipio"]),
            f"{row['total_vacantes']:,}",
            salario
        )


    console.print("\n", table, "\n")
    console.print("[bold green][OK] PIPELINE COMPLETADO EXITOSAMENTE.[/bold green]")
    console.print(f"Data Lake Parquet: [link=file://{parquet_path.absolute()}]{parquet_path}[/link]")
    console.print(f"DuckDB Warehouse: [bold]{loader.db_path}[/bold]\n")


def main():
    asyncio.run(run_pipeline())


if __name__ == "__main__":
    main()
