import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# Configuración inicial de la página en modo ancho
st.set_page_config(
    page_title="Supply Chain & Logistics Executive Dashboard", 
    page_icon="📦", 
    layout="wide"
)

st.title("📦 Dashboard Ejecutivo: Supply Chain & Logística")
st.markdown("Monitoreo gerencial en tiempo real de operaciones logísticas, cumplimiento de entregas (*OTIF*), costos de transporte y rendimiento por centro de distribución.")

# Generación de datos simulados avanzados (múltiples centros de distribución y rutas)
@st.cache_data
def load_data():
    np.random.seed(42)
    dates = pd.date_range(start='2025-10-01', end='2026-06-01', freq='D')
    centros = ['CDMX - Centro', 'MTY - Norte', 'GDL - Occidente', 'QRO - Bajío']
    
    data = []
    for fecha in dates:
        for centro in centros:
            envios = np.random.randint(40, 90)
            otif = np.random.uniform(82, 99)
            costo = np.random.uniform(1200, 3500)
            tiempo = np.random.uniform(1.8, 4.2)
            data.append([fecha, centro, envios, otif, costo, tiempo])
            
    df = pd.DataFrame(data, columns=['Fecha', 'Centro_Distribucion', 'Envios_Totales', 'OTIF_Rate (%)', 'Costo_Transporte ($)', 'Tiempo_Promedio_Dias'])
    df['OTIF_Rate (%)'] = df['OTIF_Rate (%)'].round(1)
    df['Costo_Transporte ($)'] = df['Costo_Transporte ($)'].round(2)
    df['Tiempo_Promedio_Dias'] = df['Tiempo_Promedio_Dias'].round(1)
    return df

df_full = load_data()

# -------------------------------------------------------------
# SIDEBAR: CONTROLES Y FILTROS GERENCIALES
# -------------------------------------------------------------
st.sidebar.header("⚙️ Controles y Filtros Gerenciales")

# 1. Filtro dinámico de rango de fechas
min_date = df_full['Fecha'].min().date()
max_date = df_full['Fecha'].max().date()

date_range = st.sidebar.date_input(
    "Selecciona Rango de Fechas",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# 2. Filtro por Centro de Distribución
centros_disponibles = df_full['Centro_Distribucion'].unique().tolist()
centros_seleccionados = st.sidebar.multiselect(
    "Centros de Distribución",
    options=centros_disponibles,
    default=centros_disponibles
)

# 3. Selector de métrica principal para los gráficos
metrica_seleccionada = st.sidebar.selectbox(
    "Métrica Principal de Análisis",
    ['OTIF_Rate (%)', 'Costo_Transporte ($)', 'Envios_Totales', 'Tiempo_Promedio_Dias']
)

# Aplicar filtros al DataFrame
if len(date_range) == 2:
    start_date, end_date = date_range
    mask = (
        (df_full['Fecha'].dt.date >= start_date) & 
        (df_full['Fecha'].dt.date <= end_date) & 
        (df_full['Centro_Distribucion'].isin(centros_seleccionados))
    )
else:
    mask = df_full['Centro_Distribucion'].isin(centros_seleccionados)

df_filtered = df_full.loc[mask]

# -------------------------------------------------------------
# VALIDACIÓN Y ALERTAS DINÁMICAS
# -------------------------------------------------------------
if df_filtered.empty:
    st.warning("⚠️ No hay datos disponibles para los filtros seleccionados. Amplía el rango de fechas o selecciona más centros.")
else:
    otif_promedio_actual = df_filtered['OTIF_Rate (%)'].mean()
    tiempo_promedio_actual = df_filtered['Tiempo_Promedio_Dias'].mean()

    # Alertas inteligentes basadas en umbrales de negocio
    if otif_promedio_actual < 89.0:
        st.error(f"🚨 **Alerta Crítica de Servicio:** El OTIF promedio ({otif_promedio_actual:.1f}%) está por debajo del umbral objetivo del 90.0%.")
    elif tiempo_promedio_actual > 3.5:
        st.warning(f"⚠️ **Advertencia Operativa:** El tiempo promedio de entrega ({tiempo_promedio_actual:.1f} días) muestra retrasos acumulados.")
    else:
        st.success("✅ **Estado Operativo Estable:** Todos los indicadores principales operan dentro de los parámetros óptimos.")

    # -------------------------------------------------------------
    # TARJETAS DE INDICADORES CLAVE (KPI METRICS)
    # -------------------------------------------------------------
    col1, col2, col3, col4 = st.columns(4)
    total_envios = df_filtered['Envios_Totales'].sum()
    costo_total = df_filtered['Costo_Transporte ($)'].sum()
    
    col1.metric("Envíos Totales", f"{total_envios:,}")
    col2.metric("OTIF Promedio", f"{otif_promedio_actual:.1f}%", f"{otif_promedio_actual - 90:+.1f}% vs Meta")
    col3.metric("Costo Total Transporte", f"${costo_total:,.2f}")
    col4.metric("Tiempo Promedio Entrega", f"{tiempo_promedio_actual:.1f} días")

    st.markdown("---")

    # -------------------------------------------------------------
    # SECCIÓN DE GRÁFICAS INTERACTIVAS CON PLOTLY
    # -------------------------------------------------------------
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader(f"📈 Tendencia Temporal: {metrica_seleccionada}")
        df_trend = df_filtered.groupby('Fecha')[metrica_seleccionada].mean().reset_index()
        fig_trend = px.line(
            df_trend, x='Fecha', y=metrica_seleccionada, 
            markers=False, line_shape="spline",
            color_discrete_sequence=['#38bdf8']
        )
        fig_trend.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font=dict(color='#f8fafc')
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    with col_b:
        st.subheader("🏢 Comparativa por Centro de Distribución")
        df_centro = df_filtered.groupby('Centro_Distribucion')[metrica_seleccionada].mean().reset_index()
        fig_bar = px.bar(
            df_centro, x='Centro_Distribucion', y=metrica_seleccionada,
            color='Centro_Distribucion',
            color_discrete_sequence=['#38bdf8', '#8b5cf6', '#ec4899', '#10b981']
        )
        fig_bar.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font=dict(color='#f8fafc'),
            showlegend=False
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    # -------------------------------------------------------------
    # TABLA DE DATOS Y DESCARGA DE REPORTES
    # -------------------------------------------------------------
    st.subheader("📋 Detalle de Registros y Reporte Ejecutivo")
    st.dataframe(df_filtered, use_container_width=True, hide_index=True)

    # Botón interactivo para exportar el reporte filtrado en CSV
    csv_data = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Reporte Ejecutivo en CSV",
        data=csv_data,
        file_name="reporte_supply_chain_ejecutivo.csv",
        mime="text/csv",
    )