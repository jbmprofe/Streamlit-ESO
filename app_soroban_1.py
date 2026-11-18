import random
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Práctica con Soroban", page_icon="🧮", layout="centered"
)

st.markdown("![Visitas](https://visitor-badge.laobi.icu/badge?page_id=app_soroban_1)")
# Muestra el logo centrado o con un ancho personalizado
st.image("logo_newton-salas.jpg", width=180)

st.title("Lectura de números en soroban")
st.markdown(
    "Observa el valor representado en las columnas del ábaco y escribe debajo las unidades, decenas, centenas, etc. a que corresponde."
)

# 1. Inicializar el estado de la sesión para mantener el número aleatorio e intento_id
if "numero_actual" not in st.session_state:
    st.session_state.cifras = random.randint(3, 7)  # Entre 3 y 7 cifras
    min_val = 10 ** (st.session_state.cifras - 1)
    max_val = (10 ** st.session_state.cifras) - 1
    st.session_state.numero_actual = random.randint(min_val, max_val)
    st.session_state.intento_id = 0  # Identificador para limpiar las cajas de texto


def reiniciar_juego():
    st.session_state.cifras = random.randint(3, 7)
    min_val = 10 ** (st.session_state.cifras - 1)
    max_val = (10 ** st.session_state.cifras) - 1
    st.session_state.numero_actual = random.randint(min_val, max_val)
    # Incrementamos el identificador para forzar el reseteo de las keys de los inputs
    st.session_state.intento_id += 1


# Obtener el número actual
num = st.session_state.numero_actual
num_str = str(num)
total_cifras = len(num_str)

st.divider()

# 2. SECCIÓN VISUAL: Representación con imágenes del soroban
st.subheader("Representación en el Soroban")

# Etiquetas de las posiciones estándar de mayor a menor
posiciones_posibles = ["MM", "CM", "DM", "UM", "C", "D", "U"]
# Nos quedamos solo con las que corresponden a la cantidad de cifras del número generado
posiciones_activas = posiciones_posibles[-total_cifras:]

# Creamos columnas visuales en Streamlit para mostrar cada cifra/ábaco alineados
cols = st.columns(total_cifras)

for i, col in enumerate(cols):
    digito_char = num_str[i]
    pos_nombre = posiciones_activas[i]

    with col:
        st.markdown(f"<h3 style='text-align: center;'>{pos_nombre}</h3>", unsafe_allow_html=True)

        # Carga de la imagen del soroban correspondiente al dígito
        st.image(f"imagenes/app_abaco_{digito_char}.png", width=70)
        # st.markdown(f"<p style='text-align: center; font-size: 20px;'><b>{digito_char}</b></p>", unsafe_allow_html=True)

st.divider()

# 3. SECCIÓN DE RESPUESTA: Cajas de texto para el alumno
st.subheader("¿Qué número está representado?")
st.markdown("Escribe en cada casilla el valor numérico que corresponde a esa posición:")

# Creamos un formulario para comprobar las respuestas de forma ordenada
with st.form("form_comprobar"):
    respuestas_usuario = {}

    # Creamos una caja de entrada para cada posición activa
    cols_inputs = st.columns(total_cifras)
    for i, col in enumerate(cols_inputs):
        pos_nombre = posiciones_activas[i]
        with col:
            # Añadimos __{st.session_state.intento_id} para vaciar las cajas al cambiar de número
            input_key = f"input_{pos_nombre}_{st.session_state.intento_id}"
            respuestas_usuario[pos_nombre] = st.text_input(
                f"{pos_nombre}", key=input_key
            )

    submitted = st.form_submit_button("Comprobar respuesta")

    if submitted:
        # Validar si el alumno ha acertado posición por posición
        acertado = True
        for i, pos_nombre in enumerate(posiciones_activas):
            digito_esperado = num_str[i]
            val_usuario = respuestas_usuario[pos_nombre].strip()
            if val_usuario != digito_esperado:
                acertado = False

        if acertado:
            st.success("🎉 ¡Excelente! ¡Has colocado cada cifra en su sitio correcto!")
            st.balloons()
        else:
            st.error("❌ Hay algún error en las posiciones. ¡Vuelve a revisar el ábaco e inténtalo de nuevo!")

st.markdown("---")
if st.button("🔄 Generar otro número aleatorio"):
    reiniciar_juego()
    st.rerun()