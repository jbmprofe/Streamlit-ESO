import streamlit as st
from fractions import Fraction

# Muestra el logo centrado o con un ancho personalizado
st.image("logo_newton-salas.jpg", width=180)

st.title("Aplicación de Matemáticas para ESO")

# Configuración de página
st.set_page_config(
    page_title="Paso de Decimal a Fracción",
    page_icon="🔢",
    layout="centered"
)

st.title("🔢 Generador de Fracción Generatriz")
st.write("Convierte cualquier número decimal a su fracción generatriz paso a paso.")

# Listas auxiliares para el cálculo de denominadores
nueves_str = [str(9 * (10**i)) for i in range(9)]  # "9", "99", "999", ...
ceros_str = ['0' * (i + 1) for i in range(9)]       # "0", "00", "000", ...

# 1. Selector de tipo de número decimal
tipo_decimal = st.radio(
    "Selecciona el tipo de número decimal:",
    options=[
        "Decimal Exacto (E)",
        "Periódico Puro (P)",
        "Periódico Mixto (M)",
        "No Periódico / Irracional (N)"
    ],
    index=0
)

st.divider()

# --- CASO 1: DECIMAL EXACTO ---
if "Exacto" in tipo_decimal:
    st.subheader("Paso a fracción de un Decimal Exacto")
    
    col1, col2 = st.columns(2)
    with col1:
        entera = st.text_input("Parte entera:", value="3")
    with col2:
        dec_exactos = st.text_input("Parte decimal:", value="75")

    if st.button("Calcular Fracción", type="primary"):
        if dec_exactos.isdigit() and (entera.isdigit() or (entera.startswith('-') and entera[1:].isdigit())):
            exacto_str = f"{entera}.{dec_exactos}"
            num_decimales = len(dec_exactos)
            
            # Cálculo
            numerador = int(float(exacto_str) * (10**num_decimales))
            denominador = 10**num_decimales
            fraccion_red = Fraction(int(numerador), int(denominador))

            st.success(f"**Número dado:** ${exacto_str}$")
            
            st.write("### Procedimiento paso a paso:")
            st.write(f"1. Escribimos en el numerador el número sin coma y en el denominador la unidad seguida de {num_decimales} cero(s):")
            st.latex(rf"\frac{{{numerador}}}{{{denominador}}}")
            
            st.write("2. Simplificamos la fracción resultante:")
            st.latex(rf"\frac{{{numerador}}}{{{denominador}}} = \mathbf{{\frac{{{fraccion_red.numerator}}}{{{fraccion_red.denominator}}}}}")
        else:
            st.error("Por favor, introduce cifras numéricas válidas.")

# --- CASO 2: PERIÓDICO PURO ---
elif "Puro" in tipo_decimal:
    st.subheader("Paso a fracción de un Periódico Puro")
    
    col1, col2 = st.columns(2)
    with col1:
        entera = st.text_input("Parte entera:", value="2")
    with col2:
        decimales = st.text_input("Periodo (decimales que se repiten):", value="36")

    if st.button("Calcular Fracción", type="primary"):
        if decimales.isdigit() and (entera.isdigit() or (entera.startswith('-') and entera[1:].isdigit())):
            num_decimales = len(decimales)
            periodico_str = f"{entera}.{decimales}{decimales}..."
            
            minuendo = int(entera + decimales)
            sustraendo = int(entera)
            numerador = minuendo - sustraendo
            denominador = int("9" * num_decimales)
            
            fraccion_red = Fraction(numerador, denominador)

            st.success(f"**Número dado:** ${entera}.({decimales}) = {periodico_str}$")
            
            st.write("### Procedimiento paso a paso:")
            st.write(f"- **Minuendo** (parte entera + periodo): `{minuendo}`")
            st.write(f"- **Sustraendo** (parte entera): `{sustraendo}`")
            st.write(f"- **Numerador:** ${minuendo} - {sustraendo} = {numerador}$")
            st.write(rf"- **Denominador:** Tantos 9 como cifras tenga el período ({num_decimales} cifra(s)) $\rightarrow$ {denominador}")
            
            st.latex(rf"\frac{{{numerador}}}{{{denominador}}} = \mathbf{{\frac{{{fraccion_red.numerator}}}{{{fraccion_red.denominator}}}}}")
        else:
            st.error("Por favor, introduce cifras numéricas válidas.")

# --- CASO 3: PERIÓDICO MIXTO ---
elif "Mixto" in tipo_decimal:
    st.subheader("Paso a fracción de un Periódico Mixto")
    
    entera = st.text_input("Parte entera:", value="1")
    col1, col2 = st.columns(2)
    with col1:
        no_periodica = st.text_input("Anteperiodo (decimales NO periódicos):", value="2")
    with col2:
        decimales = st.text_input("Periodo (decimales PERIÓDICOS):", value="3")

    if st.button("Calcular Fracción", type="primary"):
        if no_periodica.isdigit() and decimales.isdigit() and (entera.isdigit() or (entera.startswith('-') and entera[1:].isdigit())):
            len_decimales = len(decimales)
            len_no_periodica = len(no_periodica)

            periodico_str = f"{entera}.{no_periodica}{decimales}{decimales}..."
            
            minuendo = int(entera + no_periodica + decimales)
            sustraendo = int(entera + no_periodica)
            numerador = minuendo - sustraendo
            
            denominador_str = ("9" * len_decimales) + ("0" * len_no_periodica)
            denominador = int(denominador_str)
            
            fraccion_red = Fraction(numerador, denominador)

            st.success(f"**Número dado:** ${entera}.{no_periodica}({decimales}) = {periodico_str}$")
            
            st.write("### Procedimiento paso a paso:")
            st.write(f"- **Minuendo** (cifras hasta el primer periodo): `{minuendo}`")
            st.write(f"- **Sustraendo** (cifras hasta el anteperiodo): `{sustraendo}`")
            st.write(f"- **Numerador:** ${minuendo} - {sustraendo} = {numerador}$")
            st.write(rf"- **Denominador:** {len_decimales} nueve(s) por el periodo y {len_no_periodica} cero(s) por el anteperiodo $\rightarrow${denominador_str}")
            
            st.latex(rf"\frac{{{numerador}}}{{{denominador_str}}} = \mathbf{{\frac{{{fraccion_red.numerator}}}{{{fraccion_red.denominator}}}}}")
        else:
            st.error("Por favor, introduce cifras numéricas válidas.")

# --- CASO 4: NO PERIÓDICO ---
elif "No Periódico" in tipo_decimal:
    st.subheader("Número Decimal No Periódico (Irracional)")
    st.warning("⚠️ Este tipo de números (como $\pi$, $\sqrt{2}$ o $e$) tienen infinitas cifras decimales no periódicas.")
    st.info("**Conclusión:** No se pueden expresar en forma de fracción. Son **números irracionales** ($\mathbb{I}$).")