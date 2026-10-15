# 📦 Dashboard Ejecutivo: Supply Chain & Logística

Aplicación web interactiva desarrollada con **Python** y **Streamlit** para el monitoreo gerencial en tiempo real de operaciones logísticas, cumplimiento de entregas (*OTIF*), costos de transporte y rendimiento por centro de distribución.

---

## 🚀 Características Principales y Funciones Gerenciales
* **Controles y Filtros Dinámicos:** Selector de rangos de fechas personalizados y filtrado multi-centro de distribución (CDMX, Monterrey, Guadalajara, Querétaro).
* **Alertas Inteligentes en Vivo:** Evaluación automática del rendimiento operativo para disparar alertas críticas si el OTIF o los tiempos de entrega rebasan los umbrales de riesgo.
* **Tarjetas de KPIs Ejecutivos:** Indicadores consolidados de envíos totales, OTIF promedio, costo total de transporte y tiempos de ciclo.
* **Visualizaciones Interactivas (Plotly):** Gráficas de tendencia temporal y análisis comparativo por centro logístico con diseño *Dark Mode*.
* **Exportación de Reportes:** Botón interactivo para la descarga directa del reporte gerencial filtrado en formato CSV.

---

## 🛠️ Tecnologías y Librerías Utilizadas
* **Python:** Lenguaje de programación principal.
* **Streamlit:** Framework para el desarrollo rápido de aplicaciones web de datos y paneles ejecutivos.
* **Plotly:** Motor de gráficos interactivos y responsivos.
* **Pandas & NumPy:** Estructuración, limpieza y agregación de datos operativos.

---

## ⚙️ Instrucciones de Instalación y Ejecución Local

Sigue estos pasos para clonar y ejecutar este proyecto en tu equipo:

1. **Clona este repositorio:**
   ```bash
   git clone [https://github.com/JossJLQH/dashboard-supply-chain.git](https://github.com/JossJLQH/dashboard-supply-chain.git)
   cd dashboard-supply-chain

2. **Crea y activa un entorno virtual (recomendado):**
   ```bash
   python3 -m venv .venv
    # En Windows:
    .venv\Scripts\activate
    # En macOS / Linux:
    source .venv/bin/activate

3. **Instalar dependencias necesarias:**
   ```bash
   pip install streamlit pandas numpy plotly

4. **Ejecutar con Streamlit:**
   ```bash
   streamlit run app.py

👤 Autor
Desarrollado por José Luis Quiroz Herrera (Analista de Datos y Desarrollador).