import httpx
from datetime import datetime
from src.core.logger import logger
from src.core.config import settings
from src.extractors.base import BaseExtractor
from src.transformers.schemas import VacanteSchema


class SPEDataGovExtractor(BaseExtractor):
    """
    Extractor oficial para consumos de la API Socrata de datos.gov.co
    (Servicio Público de Empleo de Colombia).
    """

    def __init__(self):
        self.endpoint_url = "https://www.datos.gov.co/resource/2pnw-mmge.json"
        self.headers = {"User-Agent": settings.USER_AGENT}
        if settings.DATOS_GOV_APP_TOKEN:
            self.headers["X-App-Token"] = settings.DATOS_GOV_APP_TOKEN

    async def extract(self, limit: int = 2500) -> list[VacanteSchema]:
        logger.info(f"[bold blue]Iniciando extraccion masiva desde API Datos Abiertos Colombia (SPE) - Limite: {limit}...[/bold blue]")
        vacantes_validas: list[VacanteSchema] = []

        params = {
            "$limit": limit,
            "$order": ":id DESC"
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(self.endpoint_url, params=params, headers=self.headers)
                
                if response.status_code == 200:
                    raw_records = response.json()
                    logger.info(f"Se obtuvieron {len(raw_records)} registros brutos de datos.gov.co")

                    for item in raw_records:
                        try:
                            dept = item.get("departamento") or item.get("nom_dept") or "COLOMBIA"
                            muni = item.get("municipio") or item.get("nom_mpio") or item.get("ciudad") or "BOGOTA"

                            vacante = VacanteSchema(
                                id_vacante=str(item.get("codigo_vacante") or item.get(":id") or item.get("id", f"SPE-{hash(str(item)) & 0xFFFFFFF}")),
                                titulo=item.get("titulo_vacante") or item.get("nombre_vacante") or item.get("cargo") or "Vacante General",
                                empresa=item.get("empresa") or item.get("razon_social") or "CONFIDENCIAL",
                                departamento=dept,
                                municipio=muni,
                                salario_min=float(item["salario_minimo"]) if "salario_minimo" in item and item["salario_minimo"] else 1300000.0,
                                salario_max=float(item["salario_maximo"]) if "salario_maximo" in item and item["salario_maximo"] else 3500000.0,
                                experiencia_meses=int(item.get("experiencia_meses", 6)),
                                nivel_educativo=item.get("nivel_estudio") or "PROFESIONAL",
                                descripcion=str(item.get("descripcion_vacante") or item.get("perfil_laboral") or "")[:500],
                                fecha_publicacion=datetime.now(),
                                fuente_origen="datos.gov.co (SPE)"
                            )
                            vacantes_validas.append(vacante)
                        except Exception as ve:
                            logger.debug(f"Registro omitido por fallo de validación: {ve}")
                else:
                    logger.warning(f"Respuesta HTTP {response.status_code} de la API.")

        except Exception as e:
            logger.error(f"Error de red o conexión al consumir datos.gov.co: {e}")

        logger.info(f"[green][OK] Extraccion completada. {len(vacantes_validas)} vacantes validadas de todo Colombia.[/green]")
        return vacantes_validas


