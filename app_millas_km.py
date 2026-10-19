import pandas as pd
import streamlit as st

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


serie_fibonacci = fibonacci(20)

st.subheader("1. La sucesión de Fibonacci")
st.write("Los primeros términos de la sucesión de Fibonacci son 0, 1:")
st.write("Los siguientes términos de la sucesión se obtienen sumando los dos términos anteriores:")
st.code(str(serie_fibonacci))

st.write("La sucesión de Fibonacci aparece en múltiples fenómenos naturales, y también nos sirve")
st.write("para hacer un cambio de unidades rápido de millas a km (o de mph a km/h)")

millas = serie_fibonacci[2:]
st.write("Si tomamos los términos de la sucesión de Fibonacci como distancias (o velocidades) en millas:")
st.code(str(millas))

st.write(
    "**Aproximación:** Cada número de la sucesión en millas se aproxima al"
    " siguiente término en kilómetros:"
)

# Mostrar equivalencias en columnas o texto destacado
equivalencias_texto = []
for i in range(0, len(millas) - 1):
  equivalencias_texto.append(f"**{millas[i]} millas** => {millas[i+1]} km")
st.markdown(" | ".join(equivalencias_texto[:5]))

# --- 2. Tabla de Errores ---
st.subheader("2. Cálculo de los errores absoluto y relativo")
m_km = 1.609

st.write("Calculamos para cada distancia el valor del error absoluto y del error")
st.markdown(f"relativo tomando la equivalencia: 1 milla = {m_km} km.")

resultados = []
for i in range(len(millas) - 1):
  m = millas[i]
  aprox_km = millas[i + 1]
  real_km = m * m_km
  err_abs = abs(aprox_km - real_km)
  err_rel = err_abs / real_km
  err_rel_pct = err_rel * 100
  operacion_err_abs = f"|{aprox_km} - {round(real_km, 3)}| = {round(err_abs, 3)}"
  resultados.append({
      "Millas": m,
      "Aproximación (km)": aprox_km,
      "Valor Real (km)": round(real_km, 3),
      "Error Absoluto (km)": operacion_err_abs,
      "Error Relativo (%)": f"{round(err_rel_pct, 1)}%",
  })

df_errores = pd.DataFrame(resultados)
# En Streamlit se usa st.dataframe en lugar de display() o print()
# st.dataframe(df_errores, use_container_width=True)
# st.write(df_errores)
# Convertir el DataFrame a HTML plano para evitar que Streamlit/Pandas carguen pyarrow
st.markdown(df_errores.to_html(index=False, escape=False), unsafe_allow_html=True)

# --- 3. Sección Interactiva: Método de Interpolación para Alumnos ---
st.divider()
st.subheader("3. 🧮 Herramienta Interactiva de Interpolación")
st.markdown(
    "Introduce un valor de millas para ver cómo se calcula la aproximación por"
    " interpolación lineal usando Fibonacci:"
)

# Selector interactivo en Streamlit en lugar de input()
millas_usuario = st.number_input(
    "Introduce el valor de millas (mph):", min_value=1.0, value=10.0, step=1.0
)

# Serie de Fibonacci de referencia
serie_fib = [
    0,
    1,
    1,
    2,
    3,
    5,
    8,
    13,
    21,
    34,
    55,
    89,
    144,
    233,
    377,
    610,
    987,
    1597,
    2584,
    4181,
]

serie_filtrada = []
for x in serie_fib:
  if x not in serie_filtrada or x >= 1:
    if x == 1 and 1 in serie_filtrada:
      continue
    serie_filtrada.append(x)

# Identificar límites
if millas_usuario <= 1:
  f_menor = 1
  f_mayor = 2
  km_menor = 2
  km_mayor = 3
else:
  f_menor = 1
  f_mayor = 2
  encontrado = False
  for i in range(len(serie_filtrada) - 1):
    if serie_filtrada[i] <= millas_usuario <= serie_filtrada[i + 1]:
      f_menor = serie_filtrada[i]
      f_mayor = serie_filtrada[i + 1]
      km_menor = serie_filtrada[i + 1]
      km_mayor = serie_filtrada[i + 2]
      encontrado = True
      break
  if not encontrado:
    f_menor = serie_filtrada[-2]
    f_mayor = serie_filtrada[-1]
    km_menor = serie_filtrada[-1]
    km_mayor = serie_filtrada[-1] + f_menor

# Cálculos de interpolación
fraccion = (millas_usuario - f_menor) / (f_mayor - f_menor)
km_estimados = km_menor + fraccion * (km_mayor - km_menor)
real_km_h = millas_usuario * 1.609
err_abs_interp = abs(km_estimados - real_km_h)
err_rel_interp_pct = (
    (err_abs_interp / real_km_h) * 100 if real_km_h != 0 else 0
)

# Mostrar resultados paso a paso de forma visual
col1, col2 = st.columns(2)

with col1:
  st.markdown("### Pasos de la Interpolación")
  st.markdown(f"**1. Intervalo identificado:**")
  st.markdown(
      f"- Límite inferior: **{f_menor} mph** (aprox. **{km_menor} km/h**)"
  )
  st.markdown(
      f"- Límite superior: **{f_mayor} mph** (aprox. **{km_mayor} km/h**)"
  )

  st.markdown(f"**2. Cálculo de la proporción:**")
  st.latex(
    f"\\frac{{{millas_usuario} - {f_menor}}}{{{f_mayor} - {f_menor}}} ="
    f" {round(fraccion, 4)} \\text{{ ({round(fraccion * 100, 1)}\\% del"
    " intervalo)}")

with col2:
  st.markdown("### Resultados y Errores")
  st.metric(
      label="Kilómetros Estimados (Aproximación)",
      value=f"{round(km_estimados, 2)} km/h",
  )
  st.metric(
      label="Valor Real Exacto",
      value=f"{round(real_km_h, 3)} km/h",
      delta=f"{round(km_estimados - real_km_h, 2)} km/h",
  )

st.info(
    f"🔍 **Análisis de Error de la Interpolación:**\n"
    f"- **Error absoluto:** `{round(err_abs_interp, 2)}` km/h\n"
    f"- **Error relativo:** `{round(err_rel_interp_pct, 2)}%`"
)