import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Interés Compuesto - 3º ESO",
    page_icon="📈",
    layout="wide"
)

st.markdown("![Visitas](https://visitor-badge.laobi.icu/badge?page_id=app_interes_compuesto)")
# Muestra el logo centrado o con un ancho personalizado
st.image("logo_newton-salas.jpg", width=180)

# Encabezado principal
st.title("📈 Interés Compuesto (3.º ESO)")
st.markdown(
    "¿Sabías que el **interés compuesto** hace que tus ahorros crezcan generando nuevos intereses "
    "sobre los intereses anteriores? Modifica los valores en el panel de la izquierda y observa cómo evoluciona tu dinero. "
    "Utiliza esa app web como fuente de ejercicios solucionados y para entender cómo aumenta el capital según aumenta el interés "
    "y la frecuencia de capitalización (aumenta más si se cobran los intereses cada mes, que si se cobran cada año)."
)

# ==========================================
# 1. BARRA LATERAL (ENTRADA DE DATOS)
# ==========================================
st.sidebar.header("⚙️ Configura tu inversión")

ci = st.sidebar.number_input(
    "💰 Capital inicial (€):",
    min_value=10.0,
    max_value=10000.0,
    value=1000.0,
    step=100.0,
    help="Cantidad de dinero con la que empiezas a ahorrar."
)

r = st.sidebar.slider(
    "📈 Interés anual (%):",
    min_value=0.1,
    max_value=20.0,
    value=4.8,
    step=0.1,
    help="Porcentaje de interés nominal anual que ofrece el banco."
)

opciones_periodo = {
    "Anual (1 vez al año)": (1, "años", "Anual"),
    "Trimestral (4 veces al año)": (4, "trimestres", "Trimestral"),
    "Mensual (12 veces al año)": (12, "meses", "Mensual"),
    "Semanal (52 veces al año)": (52, "semanas", "Semanal"),
    "Diario (365 veces al año)": (365, "días", "Diario")
}

seleccion = st.sidebar.selectbox(
    "📅 Frecuencia de capitalización:",
    options=list(opciones_periodo.keys()),
    index=0  # Por defecto: Anual
)
m, texto_eje, nombre_periodo = opciones_periodo[seleccion]

plazo_anos = st.sidebar.slider(
    "⏳ Tiempo de inversión (años):",
    min_value=1,
    max_value=25,
    value=5,
    step=1,
    help="Duración total del ahorro (limitado a un máximo de 25 años)."
)

# ==========================================
# 2. CÁLCULOS Y EXPLICACIÓN MATEMÁTICA
# ==========================================
n_periodos_totales = int(m * plazo_anos)
tasa_periodo = (r / m) / 100
iv_periodo = 1 + tasa_periodo

cf = round(ci * (iv_periodo ** n_periodos_totales), 2)
intereses_totales = round(cf - ci, 2)

st.divider()

# Mostrar métricas principales en columnas
col1, col2, col3 = st.columns(3)
col1.metric(label="Capital Inicial ($C_i$)", value=f"{ci:,.2f} €".replace(",", "X").replace(".", ",").replace("X", "."))
col2.metric(label="Capital Final ($C_f$)", value=f"{cf:,.2f} €".replace(",", "X").replace(".", ",").replace("X", "."))
col3.metric(
    label="Intereses ganados 🚀",
    value=f"{intereses_totales:,.2f} €".replace(",", "X").replace(".", ",").replace("X", "."),
    delta=f"+{round((intereses_totales / ci) * 100, 1)} % sobre tu dinero"
)

# Desplegable con la fórmula aplicada paso a paso
with st.expander("🧮 Ver la fórmula matemática paso a paso", expanded=True):
    st.markdown(f"Con capitalización **{nombre_periodo.lower()}** ($m = {m}$), el interés de cada periodo es $\\frac{{{r}\\%}}{{{m}}} = {round(r/m, 4)}\\%$, por lo que el índice de variación es $IV = {round(iv_periodo, 6)}$.")
    st.latex(
        rf"C_f = C_i \cdot \left(1 + \frac{{r/m}}{{100}}\right)^{{t \cdot m}} = "
        rf"{ci} \cdot \left(1 + \frac{{{r}/{m}}}{{100}}\right)^{{{plazo_anos} \cdot {m}}} = "
        rf"{ci} \cdot ({round(iv_periodo, 6)})^{{{n_periodos_totales}}} = \mathbf{{{cf}\text{{ €}}}}"
    )

# ==========================================
# 3. GRÁFICA INTERACTIVA
# ==========================================
st.subheader("📊 Evolución de tus ahorros")

tiempo = np.linspace(0, n_periodos_totales, 500)
capital_evolucion = ci * (iv_periodo ** tiempo)

tiempo_discreto = np.arange(0, n_periodos_totales + 1)
capital_discreto = ci * (iv_periodo ** tiempo_discreto)

fig, ax = plt.subplots(figsize=(11, 5.5))

# Línea base del capital inicial
ax.axhline(y=ci, color='gray', linestyle=':', alpha=0.8, label=f'Tu dinero inicial ({ci} €)')

# Barras discretas para frecuencias bajas o relleno continuo para altas
if m in [1, 4, 12] and n_periodos_totales <= 180:
    ax.bar(
        tiempo_discreto[:-1], capital_discreto[:-1], width=1.0, align='edge',
        alpha=0.35, color='gold', edgecolor='darkgoldenrod',
        label='Evolución escalonada (Capital + Intereses)'
    )
else:
    ax.fill_between(
        tiempo, ci, capital_evolucion, alpha=0.22, color='green',
        label='Intereses acumulados (¡Ganancias!)'
    )

# Curva exponencial de crecimiento
ax.plot(tiempo, capital_evolucion, color='darkgreen', linewidth=2.5, label='Curva de crecimiento')

# Puntos inicial y final
ax.scatter(0, ci, color='blue', s=70, zorder=5, label='Inicio')
ax.scatter(n_periodos_totales, cf, color='red', s=100, zorder=5, label=f'Final: {cf} €')

ax.set_title(f'Crecimiento del capital durante {plazo_anos} años (Capitalización {nombre_periodo})', fontsize=13, fontweight='bold', color='darkgreen')
ax.set_xlabel(f'Tiempo transcurrido ({texto_eje})', fontsize=11)
ax.set_ylabel('Cantidad de dinero (€)', fontsize=11)

ax.set_ylim(0, max(capital_evolucion) * 1.15)
ax.set_xlim(0, n_periodos_totales)

intervalo_ticks = max(1, int(n_periodos_totales / 15))
ax.set_xticks(np.arange(0, n_periodos_totales + 1, intervalo_ticks))

ax.grid(True, linestyle='--', alpha=0.3)
ax.legend(loc='upper left', fontsize=10)

st.pyplot(fig)

# ==========================================
# 4. TABLA RESUMIDA AÑO A AÑO
# ==========================================
st.subheader("📋 Resumen año a año")

hitos_anos = np.arange(0, plazo_anos + 1)
tabla_resumida = pd.DataFrame({
    'Año transcurrido': hitos_anos,
    'Dinero en tu cuenta (€)': [round(ci * (iv_periodo ** (m * t)), 2) for t in hitos_anos],
    'Ganancia acumulada (€)': [round((ci * (iv_periodo ** (m * t))) - ci, 2) for t in hitos_anos]
})

st.dataframe(
    tabla_resumida,
    use_container_width=True,
    hide_index=True
)
