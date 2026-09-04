from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class VacanteSchema(BaseModel):
    """
    Contrato de datos (Data Contract) para validar vacantes laborales extraídas.
    Garantiza la limpieza y coherencia de los tipos antes de persistir en DuckDB/Parquet.
    """
    id_vacante: str = Field(description="Identificador único de la vacante")
    titulo: str = Field(description="Título del puesto de trabajo")
    empresa: str = Field(default="CONFIDENCIAL", description="Nombre de la empresa ofertante")
    departamento: str = Field(description="Departamento normalizado en Colombia")
    municipio: str = Field(description="Municipio/Ciudad normalizada")
    salario_min: float | None = Field(default=None, description="Salario mínimo expresado en COP")
    salario_max: float | None = Field(default=None, description="Salario máximo expresado en COP")
    experiencia_meses: int = Field(default=0, description="Meses de experiencia requeridos")
    nivel_educativo: str = Field(default="NO ESPECIFICADO", description="Nivel educativo requerido (Pregrado, Posgrado, Técnico)")
    descripcion: str = Field(default="", description="Detalle completo del perfil")
    fecha_publicacion: datetime = Field(default_factory=datetime.now)
    fuente_origen: str = Field(description="Fuente de donde se obtuvo la oferta (datos.gov.co, elempleo, etc.)")

    @field_validator("departamento", "municipio", mode="before")
    @classmethod
    def clean_text_upper(cls, v: str | None) -> str:
        if not v:
            return "DESCONOCIDO"
        return str(v).strip().upper()


class GraduadoSchema(BaseModel):
    """
    Contrato de datos para graduados universitarios (SNIES / Mineducación).
    """
    anio: int = Field(description="Año del reporte de graduación")
    codigo_ies: str = Field(description="Código de la Institución de Educación Superior")
    nombre_ies: str = Field(description="Nombre de la universidad o IES")
    departamento: str = Field(description="Departamento de la sede")
    municipio: str = Field(description="Municipio de la sede")
    programa_academico: str = Field(description="Nombre de la carrera o programa")
    nivel_academico: str = Field(description="Universitaria, Especialización, Maestría, Doctorado")
    total_graduados: int = Field(default=0, ge=0, description="Cantidad total de graduados en el periodo")
