import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fractions import Fraction

st.markdown("![Visitas](https://visitor-badge.laobi.icu/badge?page_id=jbmprofe.app_millas_km)")
# Muestra el logo centrado o con un ancho personalizado
st.image("logo_newton-salas.jpg", width=180)
st.title("Matemáticas para ESO")

# Configuración de la página
st.set_page_config(
    page_title="Aproximación de Millas a Kilómetros con Fibonacci",
    page_icon="icono_ns.png",
    layout="wide"
)

st.title("Aproximación de millas a kilómetros mediante la sucesión de Fibonacci")
st.markdown(
    "Esta aplicación muestra cómo los números consecutivos de la sucesión de"
    " Fibonacci sirven como una buena aproximación para convertir millas"
    " a kilómetros."
)

# --- 1. Generar la serie de Fibonacci ---
def fibonacci(n):
    secuencia = [0, 1]
    while len(secuencia) < n:
        secuencia.append(secuencia[-1] + secuencia[-2])
    return secuencia[:n]

serie_fib = fibonacci(14)
millas = serie_fib[2:]  # Comenzamos desde el 1 para las millas

# Sidebar - Teoría rápida
st.sidebar.header("📚 Recordatorio Teórico")
st.sidebar.markdown(r"**Error Absoluto ($E_a$)** = $|V_{\text{aproximado}} - V_{\text{real}}|$")
st.sidebar.markdown(r"**Error Relativo ($E_r$)** = $\frac{E_a}{V_{\text{real}}} \cdot 100\%$")
st.sidebar.markdown("""
* **Error Absoluto:** Nos indica la diferencia física real (en la misma unidad, en este caso km).
* **Error Relativo:** Nos da una idea porcentual de la importancia de ese error. ¡Un error de 1 km no es lo mismo si medimos 2 km que si medimos 1000 km!
""")

# Crear pestañas para organizar la actividad
tab1, tab2, tab3 = st.tabs(["📈 Gráfica Interactiva", "🧮 Calculadora de Errores e Interpolación", "📊 Tabla General de Errores"])

with tab1:
    st.header("Visualización del Modelo")
    st.write("Observa cómo los puntos de la aproximación de Fibonacci (Millas, Km aproximados) se sitúan casi perfectamente sobre la recta de conversión exacta (1 milla = 1.609 km).")

    # Gráfico
    m_km = 1.609
    x_fib = serie_fib[2:-1]
    y_fib = serie_fib[3:]

    x_recta = np.linspace(0, max(x_fib) + 10, 500)
    y_recta_exacta = x_recta * m_km

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x_recta, y_recta_exacta, label='Conversión Real Exacta (y = x * 1.609)', color='#2ca02c', linestyle='--')
    ax.scatter(x_fib, y_fib, color='#1f77b4', s=80, zorder=5, label='Aproximación Fibonacci (Millas, Km)')

    # Anotaciones didácticas
    for i, m_val in enumerate(x_fib[:7]): # Anotar los primeros puntos para que se entienda mejor
        ax.annotate(f"({m_val}, {y_fib[i]})", (m_val, y_fib[i]), textcoords="offset points", xytext=(10,-5), ha='left', fontsize=9)

    ax.set_xlabel('Distancia en Millas (x)')
    ax.set_ylabel('Distancia en Kilómetros (y)')
    ax.set_title('Millas vs Kilómetros: Real vs Fibonacci')
    ax.legend()
    ax.grid(True, linestyle=':', alpha=0.6)

    st.pyplot(fig)

with tab2:
    st.header("🔍 Interpolación y Cálculo de Errores a la Carta")
    st.write("¿Qué pasa si queremos convertir un valor que no es exactamente un término de Fibonacci? Usamos **interpolación proporcional**. Introduce cualquier velocidad o distancia en millas:")

    # Input del alumno
    val_usuario = st.number_input("Introduce el valor en millas (mph o millas):", min_value=1.0, max_value=200.0, value=65.0, step=0.5)

    # Filtrar duplicados para la interpolación limpia
    serie_filtrada = []
    for x in serie_fib:
        if x not in serie_filtrada or x >= 1:
            if x == 1 and 1 in serie_filtrada: continue
            serie_filtrada.append(x)

    # Buscar intervalo
    f_menor, f_mayor, km_menor, km_mayor = 1, 2, 2, 3
    for i in range(len(serie_filtrada) - 1):
        if serie_filtrada[i] <= val_usuario <= serie_filtrada[i+1]:
            f_menor = serie_filtrada[i]
            f_mayor = serie_filtrada[i+1]
            km_menor = serie_filtrada[i+1]
            km_mayor = serie_filtrada[i+2]
            break

    # Cálculos
    fraccion = (val_usuario - f_menor) / (f_mayor - f_menor)
    km_estimados = km_menor + fraccion * (km_mayor - km_menor)
    real_km = val_usuario * 1.609

    err_abs_interp = abs(km_estimados - real_km)
    err_rel_interp_pct = (err_abs_interp / real_km) * 100

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🧠 Paso 1: Localizar los intervalos")
        st.info(f"**{val_usuario} millas** se encuentra entre los números de Fibonacci:\n\n" 
                f"👉 **{f_menor}** (equivale a {km_menor} km)\n\n" 
                f"👉 **{f_mayor}** (equivale a {km_mayor} km)")

        st.subheader("⚖️ Paso 2: Proporción del intervalo")
        st.write(f"El valor está a una distancia proporcional de:")
        numerador = int(val_usuario - f_menor)
        denominador = int(f_mayor - f_menor)
        # Creas la fracción y Python la simplifica automáticamente
        fraccion_simplificada = Fraction(numerador, denominador)
        # Obtienes el nuevo numerador y denominador simplificados
        nuevo_numerador = fraccion_simplificada.numerator
        nuevo_denominador = fraccion_simplificada.denominator
        if nuevo_numerador != numerador:
            st.markdown(f"$$\\frac{{{val_usuario} - {f_menor}}}{{{f_mayor} - {f_menor}}} = \\frac{{{numerador}}}{{{denominador}}} = \\frac{{{nuevo_numerador}}}{{{nuevo_denominador}}}= {round(fraccion, 3)}$$")
        else:
            st.markdown(f"$$\\frac{{{val_usuario} - {f_menor}}}{{{f_mayor} - {f_menor}}} = \\frac{{{numerador}}}{{{denominador}}} = {round(fraccion, 3)}$$")
        st.write(f"Es decir, cubrimos el **{round(fraccion*100, 1)}%** del camino.")

    with col2:
        st.subheader("🚗 Paso 3: Estimar el resultado en km")
        st.markdown(f"${km_menor} + {round(fraccion, 3)} \\cdot ({km_mayor} - {km_menor}) = {round(km_estimados, 1)}$ km")
        st.subheader("🎯 Comparación Real")
        st.success(f"Valor exacto por fórmula (Millas × 1.609):")
        st.success(f"**{round(real_km, 2)} km**")

    # Sección de evaluación de errores bien destacada
    st.markdown("--- ")
    st.subheader("🔥 Cálculo de los Errores cometidos")

    col_err1, col_err2 = st.columns(2)
    with col_err1:
        st.metric(label="Error Absoluto", value=f"{round(err_abs_interp, 2)} km", delta=None)
        st.write("**Desglose de la operación:**")
        st.markdown(f"$E_a = |{round(km_estimados, 2)} - {round(real_km, 2)}| \\simeq {round(err_abs_interp, 1)}$ km")
    with col_err2:
        st.metric(label="Error Relativo (%)", value=f"{round(err_rel_interp_pct, 1)}%", delta=None)
        st.write("**Desglose de la operación:**")
        Erelativo_real = 100 * round(err_abs_interp, 1) / round(real_km, 1)
        Ereativo_aprox = 100 * round(err_abs_interp, 1) / round(km_estimados, 1)
        # st.markdown(f"$E_r = \\frac{{{round(err_abs_interp, 1)}}}{{{round(real_km, 1)}}} \\cdot 100 \\simeq {round(err_rel_interp_pct, 1)}\\%$")
        st.markdown(f"$E_r = \\frac{{{round(err_abs_interp, 1)}}}{{{round(real_km, 1)}}} \\cdot 100 \\simeq {round(Erelativo_real, 1)}\\%$")
        st.write("En general, desconocemos el valor real, y se suele tomar el valor estimado para calcular el error relativo ")
        st.write("Puesto que el error absoluto se puede considerar mucho menor que el valor real y que el valor estimado,")
        st.write("el error relativo toma prácticamente el mismo valor en ambos casos:")
        st.markdown(f"$E_r = \\frac{{{round(err_abs_interp, 1)}}}{{{round(km_estimados, 1)}}} \\cdot 100 \\simeq {round(Ereativo_aprox, 1)}\\%$")

with tab3:
    st.header("📊 Tabla de Errores para Distancias Exactas de Fibonacci")
    st.write("Esta tabla muestra el error exacto cometido al usar un término puro de la sucesión de Fibonacci para estimar el kilómetro correspondiente.")

    resultados = []
    for i in range(len(millas) - 1):
        m = millas[i]
        aprox_km = millas[i+1]
        real_km = m * 1.609
        err_abs = abs(aprox_km - real_km)
        err_rel_pct = (err_abs / real_km) * 100

        resultados.append({
            "Millas (F_n)": m,
            "Aprox. Km (F_n+1)": aprox_km,
            "Valor real exacto (km)": round(real_km, 3),
            "Error absoluto (km)": round(err_abs, 3),
            "Error relativo (%)": f"{round(err_rel_pct, 2)}%"
        })

    df_errores_st = pd.DataFrame(resultados)
    st.dataframe(df_errores_st, use_container_width=True)
    st.caption("💡 ¡Nota cómo a medida que los números de la sucesión de Fibonacci se hacen más grandes, el error relativo se reduce drásticamente por debajo del 1%!")


st.info(
    f"🔍 **Análisis de Error de la Interpolación:**\n"
    f"- **Error absoluto:** `{round(err_abs_interp, 2)}` km/h\n"
    f"- **Error relativo:** `{round(err_rel_interp_pct, 2)}%`"
)
