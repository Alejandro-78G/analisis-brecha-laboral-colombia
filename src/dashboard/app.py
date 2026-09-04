import streamlit as st
import duckdb
import pandas as pd
from pathlib import Path

# Configuración de página Streamlit
st.set_page_config(
    page_title="Brecha Laboral & Empleabilidad Colombia",
    page_icon="🇨🇴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Conexión a DuckDB Warehouse
DB_PATH = Path(__file__).parents[2] / "data" / "brecha_laboral.duckdb"

@st.cache_data(ttl=60)
def load_data() -> pd.DataFrame:
    if not DB_PATH.exists():
        st.error(f"Base de datos no encontrada en {DB_PATH}. Ejecute 'python -m src.main' primero.")
        return pd.DataFrame()
    
    conn = duckdb.connect(str(DB_PATH), read_only=True)
    df = conn.execute("SELECT * FROM fact_vacantes;").df()
    conn.close()
    return df

# Título Principal
st.title("🇨🇴 Monitor de Brecha Laboral y Empleabilidad en Colombia")
st.markdown("""
Plataforma de inteligencia analítica impulsada por **DuckDB + dbt + Streamlit**. 
Analiza la demanda de vacantes laborales, la brecha de oportunidades por región y los niveles salariales en Colombia.
""")

df_raw = load_data()

if df_raw.empty:
    st.stop()

# ===================== FILTROS EN SIDEBAR =====================
st.sidebar.header("🔍 Filtros de Análisis")

# Filtro Región
regiones_opt = ["TODAS"] + sorted(df_raw["region_geografica"].dropna().unique().tolist())
sel_region = st.sidebar.selectbox("Región Geográfica", regiones_opt)

# Filtrar dataframe dinámicamente por región
df_filtered = df_raw.copy()
if sel_region != "TODAS":
    df_filtered = df_filtered[df_filtered["region_geografica"] == sel_region]

# Filtro Departamento
deptos_opt = ["TODOS"] + sorted(df_filtered["departamento"].dropna().unique().tolist())
sel_depto = st.sidebar.selectbox("Departamento", deptos_opt)
if sel_depto != "TODOS":
    df_filtered = df_filtered[df_filtered["departamento"] == sel_depto]

# Filtro Nivel Educativo
niveles_opt = ["TODOS"] + sorted(df_filtered["nivel_educativo"].dropna().unique().tolist())
sel_nivel = st.sidebar.selectbox("Nivel Educativo", niveles_opt)
if sel_nivel != "TODOS":
    df_filtered = df_filtered[df_filtered["nivel_educativo"] == sel_nivel]

# ===================== METRICAS PRINCIPALES (KPIS) =====================
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_vacantes = len(df_filtered)
    st.metric("Total Vacantes Analizadas", f"{total_vacantes:,}")

with col2:
    salario_prom = df_filtered["salario_promedio"].mean()
    salario_str = f"${salario_prom:,.0f} COP" if pd.notnull(salario_prom) else "N/A"
    st.metric("Salario Promedio Nacional", salario_str)

with col3:
    ciudad_top = df_filtered["municipio"].value_counts().idxmax() if not df_filtered.empty else "N/A"
    st.metric("Ciudad con Mayor Oferta", ciudad_top)

with col4:
    experiencia_prom = df_filtered["experiencia_meses"].mean()
    exp_str = f"{experiencia_prom:.1f} meses" if pd.notnull(experiencia_prom) else "N/A"
    st.metric("Experiencia Promedio Requerida", exp_str)

st.divider()

# ===================== GRAFICOS ANALITICOS =====================
tab1, tab2, tab3 = st.tabs(["🏙️ Demanda por Ciudades", "💰 Niveles Salariales", "📄 Datos Detallados"])

with tab1:
    st.subheader("Top 15 Ciudades con Mayor Oferta Laboral")
    df_ciudades = (
        df_filtered.groupby(["departamento", "municipio"])
        .agg(
            vacantes=("id_vacante", "count"),
            salario_medio=("salario_promedio", "mean")
        )
        .reset_index()
        .sort_values(by="vacantes", ascending=False)
        .head(15)
    )
    
    st.bar_chart(
        data=df_ciudades,
        x="municipio",
        y="vacantes",
        color="departamento"
    )

with tab2:
    st.subheader("Distribución Salarial por Nivel Educativo")
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.markdown("**Vacantes por Rango Salarial**")
        df_rango = df_filtered["rango_salarial_categoria"].value_counts().reset_index()
        df_rango.columns = ["Rango Salarial", "Vacantes"]
        st.dataframe(df_rango)

    with col_g2:
        st.markdown("**Salario Promedio por Nivel Educativo**")
        df_nivel_sal = (
            df_filtered.groupby("nivel_educativo")["salario_promedio"]
            .mean()
            .reset_index()
            .sort_values(by="salario_promedio", ascending=False)
        )
        df_nivel_sal["salario_promedio"] = df_nivel_sal["salario_promedio"].map("${:,.0f} COP".format)
        st.dataframe(df_nivel_sal)

with tab3:
    st.subheader("Explorador Interactivo del Data Lake (DuckDB Marts)")
    st.dataframe(
        df_filtered[[
            "id_vacante", "titulo_vacante", "empresa", "departamento", 
            "municipio", "region_geografica", "nivel_educativo", 
            "salario_promedio", "rango_salarial_categoria", "fuente_origen"
        ]]
    )


st.caption("Desarrollado con DuckDB + dbt Core + Streamlit | Colombia Data Analytics 2026")
