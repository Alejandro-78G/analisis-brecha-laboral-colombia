"""
Dashboard: Monitor de Brecha Laboral y Empleabilidad en Colombia
Modo demo con datos sintéticos cuando DuckDB no está disponible (Streamlit Cloud)
"""
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

# ── Configuración de página ─────────────────────────────────────────────────
st.set_page_config(
    page_title="Brecha Laboral & Empleabilidad Colombia",
    page_icon="🇨🇴",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/Alejandro-78G/analisis-brecha-laboral-colombia",
        "Report a bug": "https://github.com/Alejandro-78G/analisis-brecha-laboral-colombia/issues",
        "About": "Pipeline ETL end-to-end sobre la brecha laboral en Colombia 🇨🇴",
    },
)

# ── CSS personalizado ────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-title {
        background: linear-gradient(135deg, #003087 0%, #c8102e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.2rem;
        font-weight: 800;
    }
    .demo-badge {
        background: #f59e0b;
        color: #000;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
    }
    .metric-card {
        border-left: 4px solid #003087;
        padding-left: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ── Conexión a DuckDB o modo DEMO ────────────────────────────────────────────
DB_PATH = Path(__file__).parents[2] / "data" / "brecha_laboral.duckdb"

CIUDADES = [
    "Bogotá", "Medellín", "Cali", "Barranquilla", "Bucaramanga",
    "Cartagena", "Pereira", "Manizales", "Cúcuta", "Santa Marta",
    "Villavicencio", "Ibagué", "Neiva", "Armenia", "Montería",
]
DEPTOS = [
    "Cundinamarca", "Antioquia", "Valle del Cauca", "Atlántico",
    "Santander", "Bolívar", "Risaralda", "Caldas", "Norte de Santander",
    "Magdalena", "Meta", "Tolima", "Huila", "Quindío", "Córdoba",
]
REGIONES = [
    "Andina", "Andina", "Pacífica", "Caribe", "Andina",
    "Caribe", "Andina", "Andina", "Andina", "Caribe",
    "Orinoquía", "Andina", "Andina", "Andina", "Caribe",
]
NIVELES_EDU = [
    "Técnico", "Tecnólogo", "Universitario", "Especialización",
    "Maestría", "Bachiller", "Doctorado",
]
RANGOS_SAL = ["< 1 SMMLV", "1-2 SMMLV", "2-4 SMMLV", "4-8 SMMLV", "> 8 SMMLV"]
SECTORES = [
    "Tecnología", "Finanzas", "Salud", "Educación", "Manufactura",
    "Comercio", "Logística", "Construcción", "Agroindustria", "Servicios",
]
FUENTES = ["Computrabajo", "ElEmpleo.com", "LinkedIn", "Indeed", "Trabajando.com"]


@st.cache_data(ttl=300)
def load_data() -> tuple[pd.DataFrame, bool]:
    """Carga datos reales desde DuckDB o genera datos demo."""
    try:
        import duckdb
        if DB_PATH.exists():
            conn = duckdb.connect(str(DB_PATH), read_only=True)
            df = conn.execute("SELECT * FROM fact_vacantes;").df()
            conn.close()
            return df, False
    except Exception:
        pass

    # ── Datos sintéticos realistas para demo ──────────────────────────────
    rng = np.random.default_rng(42)
    n = 2_500

    ciudad_idx = rng.integers(0, len(CIUDADES), size=n)
    nivel_idx = rng.integers(0, len(NIVELES_EDU), size=n)
    rango_idx = rng.integers(0, len(RANGOS_SAL), size=n)

    # Salario base por nivel educativo
    sal_base = {
        "Bachiller": 1_160_000, "Técnico": 1_500_000, "Tecnólogo": 1_900_000,
        "Universitario": 2_800_000, "Especialización": 4_200_000,
        "Maestría": 6_500_000, "Doctorado": 9_800_000,
    }
    salarios = [
        int(sal_base[NIVELES_EDU[ni]] * rng.uniform(0.85, 1.45))
        for ni in nivel_idx
    ]

    df = pd.DataFrame({
        "id_vacante": [f"VAC-{i:05d}" for i in range(1, n + 1)],
        "titulo_vacante": rng.choice([
            "Desarrollador de Software", "Analista de Datos", "Contador",
            "Ingeniero Industrial", "Médico General", "Docente Universitario",
            "Administrador de Empresas", "Diseñador UX/UI", "Técnico en Sistemas",
            "Asesor Comercial", "Abogado Corporativo", "Enfermero/a",
            "Logística y Cadena de Suministro", "Auditor Financiero",
            "Data Scientist", "DevOps Engineer", "Marketing Digital",
        ], size=n),
        "empresa": rng.choice([
            "Bancolombia", "Ecopetrol", "Claro Colombia", "Nutresa",
            "Bavaria", "Avianca", "EPM", "Cemex Colombia", "Amazon Colombia",
            "Google Colombia", "Ministerio de Salud", "Grupo Bolívar",
            "Suramericana", "Colfondos", "Rappi",
        ], size=n),
        "municipio": [CIUDADES[i] for i in ciudad_idx],
        "departamento": [DEPTOS[i] for i in ciudad_idx],
        "region_geografica": [REGIONES[i] for i in ciudad_idx],
        "nivel_educativo": [NIVELES_EDU[i] for i in nivel_idx],
        "salario_promedio": salarios,
        "rango_salarial_categoria": [RANGOS_SAL[i] for i in rango_idx],
        "experiencia_meses": rng.integers(0, 120, size=n).tolist(),
        "sector_economico": rng.choice(SECTORES, size=n).tolist(),
        "fuente_origen": rng.choice(FUENTES, size=n).tolist(),
        "fecha_publicacion": pd.date_range("2024-01-01", periods=n, freq="1h").tolist(),
    })
    return df, True


# ── Cargar datos ─────────────────────────────────────────────────────────────
df_raw, es_demo = load_data()

# ── Header ───────────────────────────────────────────────────────────────────
col_title, col_badge = st.columns([6, 1])
with col_title:
    st.markdown(
        '<h1 class="main-title">🇨🇴 Monitor de Brecha Laboral en Colombia</h1>',
        unsafe_allow_html=True,
    )
with col_badge:
    if es_demo:
        st.markdown("")
        st.markdown(
            '<span class="demo-badge">📊 MODO DEMO</span>', unsafe_allow_html=True
        )

st.markdown(
    "Plataforma de inteligencia analítica impulsada por **DuckDB · dbt · Streamlit**. "
    "Analiza vacantes laborales, brechas de oportunidad por región y niveles salariales en Colombia."
)
if es_demo:
    st.info(
        "⚠️ **Modo demostración**: visualizando datos sintéticos realistas (2,500 registros). "
        "Para datos reales, ejecuta `python -m src.main` localmente y conecta tu DuckDB.",
        icon="📊",
    )

st.divider()

# ── Filtros Sidebar ───────────────────────────────────────────────────────────
st.sidebar.header("🔍 Filtros de Análisis")
st.sidebar.markdown("---")

regiones_opt = ["TODAS"] + sorted(df_raw["region_geografica"].dropna().unique().tolist())
sel_region = st.sidebar.selectbox("🗺️ Región Geográfica", regiones_opt)

df_filtered = df_raw.copy()
if sel_region != "TODAS":
    df_filtered = df_filtered[df_filtered["region_geografica"] == sel_region]

deptos_opt = ["TODOS"] + sorted(df_filtered["departamento"].dropna().unique().tolist())
sel_depto = st.sidebar.selectbox("📍 Departamento", deptos_opt)
if sel_depto != "TODOS":
    df_filtered = df_filtered[df_filtered["departamento"] == sel_depto]

niveles_opt = ["TODOS"] + sorted(df_filtered["nivel_educativo"].dropna().unique().tolist())
sel_nivel = st.sidebar.selectbox("🎓 Nivel Educativo", niveles_opt)
if sel_nivel != "TODOS":
    df_filtered = df_filtered[df_filtered["nivel_educativo"] == sel_nivel]

sectores_opt = ["TODOS"] + sorted(df_filtered["sector_economico"].dropna().unique().tolist())
sel_sector = st.sidebar.selectbox("🏭 Sector Económico", sectores_opt)
if sel_sector != "TODOS":
    df_filtered = df_filtered[df_filtered["sector_economico"] == sel_sector]

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Proyecto Open Source** · "
    "[GitHub](https://github.com/Alejandro-78G/analisis-brecha-laboral-colombia)"
)

# ── KPIs principales ─────────────────────────────────────────────────────────
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("📋 Total Vacantes", f"{len(df_filtered):,}")
with col2:
    sal_prom = df_filtered["salario_promedio"].mean()
    sal_str = f"${sal_prom:,.0f}" if pd.notnull(sal_prom) else "N/A"
    st.metric("💰 Salario Promedio", sal_str)
with col3:
    ciudad_top = (
        df_filtered["municipio"].value_counts().idxmax()
        if not df_filtered.empty else "N/A"
    )
    st.metric("🏙️ Ciudad Líder", ciudad_top)
with col4:
    exp_prom = df_filtered["experiencia_meses"].mean()
    exp_str = f"{exp_prom:.0f} meses" if pd.notnull(exp_prom) else "N/A"
    st.metric("⏱️ Experiencia Media", exp_str)
with col5:
    ciudades_count = df_filtered["municipio"].nunique()
    st.metric("📡 Ciudades Activas", ciudades_count)

st.divider()

# ── Tabs de análisis ─────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🏙️ Demanda por Ciudades",
    "💰 Análisis Salarial",
    "🎓 Brecha Educativa",
    "📄 Datos Completos",
])

with tab1:
    st.subheader("Top 15 Ciudades con Mayor Oferta Laboral")
    df_ciudades = (
        df_filtered.groupby(["departamento", "municipio"])
        .agg(vacantes=("id_vacante", "count"), salario_medio=("salario_promedio", "mean"))
        .reset_index()
        .sort_values("vacantes", ascending=False)
        .head(15)
    )
    st.bar_chart(data=df_ciudades, x="municipio", y="vacantes", color="departamento")

    st.markdown("**📊 Detalle por ciudad:**")
    df_ciudades["salario_medio"] = df_ciudades["salario_medio"].map("${:,.0f} COP".format)
    st.dataframe(df_ciudades.rename(columns={
        "departamento": "Departamento", "municipio": "Ciudad",
        "vacantes": "Vacantes", "salario_medio": "Salario Promedio",
    }), use_container_width=True)

with tab2:
    st.subheader("Distribución Salarial por Nivel Educativo")
    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.markdown("**Vacantes por Rango Salarial**")
        df_rango = df_filtered["rango_salarial_categoria"].value_counts().reset_index()
        df_rango.columns = ["Rango Salarial", "Vacantes"]
        st.bar_chart(data=df_rango, x="Rango Salarial", y="Vacantes")

    with col_g2:
        st.markdown("**Salario Promedio por Nivel Educativo**")
        df_nivel_sal = (
            df_filtered.groupby("nivel_educativo")["salario_promedio"]
            .mean()
            .reset_index()
            .sort_values("salario_promedio", ascending=False)
        )
        df_nivel_sal.columns = ["Nivel Educativo", "Salario Promedio COP"]
        st.bar_chart(data=df_nivel_sal, x="Nivel Educativo", y="Salario Promedio COP")

with tab3:
    st.subheader("Análisis de la Brecha Educativa")

    col_b1, col_b2 = st.columns(2)

    with col_b1:
        st.markdown("**Demanda de Vacantes por Nivel Educativo**")
        df_edu_demand = (
            df_filtered["nivel_educativo"].value_counts().reset_index()
        )
        df_edu_demand.columns = ["Nivel Educativo", "Vacantes"]
        st.bar_chart(data=df_edu_demand, x="Nivel Educativo", y="Vacantes")

    with col_b2:
        st.markdown("**Distribución por Sector Económico**")
        df_sector = df_filtered["sector_economico"].value_counts().reset_index()
        df_sector.columns = ["Sector", "Vacantes"]
        st.dataframe(df_sector, use_container_width=True)

    # Insight principal
    st.markdown("---")
    st.markdown("### 💡 Hallazgo Principal")
    st.error(
        "**Brecha Crítica Detectada**: Se estima aproximadamente **1 vacante formal "
        "por cada 2,868 graduados** en Colombia, evidenciando una desconexión estructural "
        "entre la formación académica y las demandas reales del mercado laboral.",
        icon="🚨",
    )

with tab4:
    st.subheader("📄 Explorador de Datos")
    cols_show = [
        "id_vacante", "titulo_vacante", "empresa", "departamento",
        "municipio", "region_geografica", "nivel_educativo",
        "salario_promedio", "rango_salarial_categoria",
        "sector_economico", "fuente_origen",
    ]
    st.dataframe(df_filtered[cols_show], use_container_width=True, height=450)

    csv = df_filtered[cols_show].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Descargar CSV",
        data=csv,
        file_name="brecha_laboral_colombia.csv",
        mime="text/csv",
    )

# ── Footer ───────────────────────────────────────────────────────────────────
st.divider()
st.caption(
    "🇨🇴 Desarrollado por **Alejandro Cristancho** · "
    "Stack: DuckDB + dbt Core + Streamlit · "
    "[GitHub](https://github.com/Alejandro-78G/analisis-brecha-laboral-colombia) · "
    "Colombia Data Analytics 2026"
)
