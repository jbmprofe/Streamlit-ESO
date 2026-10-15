import math
import matplotlib.pyplot as plt
import streamlit as st


st.markdown("![Visitas](https://visitor-badge.laobi.icu/badge?page_id=jbmprofe.app_fraccion_unitaria)")
# Muestra el logo centrado o con un ancho personalizado
st.image("logo_newton-salas.jpg", width=180)

st.title("Matemáticas para ESO")

# Configuración de la página
st.set_page_config(
    page_title="Descomposición de una fracción en fracciones unitarias",
    page_icon="icono_ns.png",
    layout="centered"
)

st.subheader(f"Descomposición de una fracción en fracciones unitarias")
st.image("numeros templo karnak.jpg", width=600)
st.markdown(r"""
Las fracciones que utilizaban en el Antiguo Egipto no eran como las que nosotros usamos. En nuestro sistema, se admite cualquier número como numerador, mientras que los egipcios solo utilizaban fracciones con numerador 1, con algunas excepciones. Llamamos *fracciones unitarias* a estas fracciones.

Los antiguos egipcios utilizaban símbolos para representar los números, por ejemplo, una barra | para representar 1, dos barras || para el dos, etc., y ∩ para representar 10, y otros símbolos para las potencias de 10 hasta un millón. En [esta dirección](https://polypad.amplify.com/p/WCOA1kpJKker6w) puedes probar a escribir números como lo hacían los egipcios.""")

st.image("simbolos numeros egipcios.jpg", width=600)

st.markdown(r"""
Como hemos dicho, los egipcios escribían todas las fracciones de manera que tuvieran denominador unidad. ¿Cómo lo hacían? ¿Cómo podían escribir, por ejemplo, la fracción $\frac{3}{4}$ como la suma de dos fracciones de denominador unidad?

Los egipcios escribían la fracción $\frac{3}{4}$ como la suma de dos fracciones de denominador unidad:

$$\frac{3}{4} = \frac{1}{2} + \frac{1}{4}$$""")

st.image("egipto 1_2 y 1_4.png", width=150)

st.markdown(r"""
Esta aplicación permite descomponer cualquier fracción propia (fracciones con numerador menor que el denominador) en una suma de fracciones unitarias (fracciones con numerador 1).
""")

st.markdown("Observa el ejemplo resuelto y prueba a introducir otros valores utilizando las cajas de la izquierda de la ventana.")

# --- COFRE DE AYUDAS / GLOSARIO (Ideal para reforzar conceptos) ---
with st.expander("💡 ¿Necesitas recordar conceptos básicos? (Haz clic para desplegar)"):
    st.markdown("""
    * **¿Qué es una fracción unitaria?** Es aquella que tiene un **1** en el numerador (arriba), como $\\frac{1}{2}$, $\\frac{1}{4}$ o $\\frac{1}{7}$. En el antiguo Egipto, todas las fracciones se expresaban como sumas de este tipo de fracciones sin repetir ninguna.
    * **El método del escriba:** Buscamos siempre la mayor fracción unitaria posible que quepa en nuestra cantidad sin pasarnos, restamos, y repetimos el proceso con lo que sobra.
    * **Mínimo común múltiplo (mcm):** Lo usamos para hallar un denominador común y poder restar las fracciones con facilidad paso a paso.
    """)

st.markdown("---")

# --- Panel Lateral de Entrada ---
st.sidebar.header("Parámetros de la Fracción")
numerador_in = st.sidebar.number_input("Numerador", min_value=1, max_value=99, value=13, step=1)
denominador_in = st.sidebar.number_input("Denominador", min_value=2, max_value=100, value=20, step=1)


def generar_grafico_equivalencia(numerador, denominador, fracciones_unitarias_str):
    """
    Genera y devuelve la figura de Matplotlib que muestra visualmente cómo
    la suma de las fracciones unitarias equivale a la fracción original.
    """
    fig, ax = plt.subplots(figsize=(10, 3.5))

    valor_original = numerador / denominador

    # 1. Barra superior: Fracción original
    ax.barh(y=1, width=valor_original, height=0.4, color='#3498db', edgecolor='black')
    ax.text(valor_original / 2, 1, f"{numerador}/{denominador}", ha='center', va='center', color='white', fontweight='bold', fontsize=12)

    # 2. Barra inferior: Fracciones unitarias apiladas
    inicio = 0.0
    colores_unitarios = ['#e74c3c', '#2ecc71', '#9b59b6', '#f1c40f', '#e67e22']

    for idx, frac_str in enumerate(fracciones_unitarias_str):
        num_u, den_u = map(int, frac_str.split('/'))
        valor_u = num_u / den_u

        color = colores_unitarios[idx % len(colores_unitarios)]
        ax.barh(y=0, width=valor_u, left=inicio, height=0.4, color=color, edgecolor='black')

        if valor_u > 0.02:
            ax.text(inicio + (valor_u / 2), 0, f"{num_u}/{den_u}", ha='center', va='center', color='black', fontweight='bold', fontsize=10)

        inicio += valor_u

    ax.set_ylim(-0.6, 1.6)
    ax.set_xlim(0, max(valor_original * 1.1, 1.0))
    ax.set_yticks([0, 1])
    ax.set_yticklabels(['Suma de Unitarias', 'Fracción Original'], fontsize=11, fontweight='bold')
    ax.set_xlabel('Valor en la recta real (de 0 a 1)', fontsize=11)
    ax.set_title(f'Equivalencia Visual: {numerador}/{denominador} = ' + ' + '.join(fracciones_unitarias_str), fontsize=12, fontweight='bold', pad=15)
    ax.grid(axis='x', linestyle='--', alpha=0.5)

    for spine in ['top', 'right', 'left']:
        ax.spines[spine].set_visible(False)

    plt.tight_layout()
    return fig


def descomponer_y_mostrar(numerador, denominador):
    if numerador >= denominador:
        st.error(f"❌ La fracción **{numerador}/{denominador}** no es propia. El numerador debe ser estrictamente menor que el denominador.")
        return

    num_orig, den_orig = numerador, denominador
    fracciones_unitarias = []

    st.subheader(f"Pasos para la fracción $\\frac{{{numerador}}}{{{denominador}}}$")

    paso = 1
    while numerador > 0:
        with st.expander(f"Paso {paso}", expanded=True):
            if numerador == 1:
                fracciones_unitarias.append(f"1/{denominador}")
                frac_actual = fr"\frac{{{numerador}}}{{{denominador}}}"
                st.write(f"• La fracción actual ${frac_actual}$ ya es una fracción unitaria.")
                st.write(f"• Añadimos ${frac_actual}$ directamente al resultado.")
                break

            n = math.ceil(denominador / numerador)
            fracciones_unitarias.append(f"1/{n}")
            # --- NUEVO CÓDIGO CLARO PARA 3º/4º ESO ---
            frac_actual = fr"\frac{{{numerador}}}{{{denominador}}}"
            valor_actual = numerador / denominador

            st.write(f"• Fracción a descomponer: ${frac_actual}$ (aprox. **{valor_actual:.3f}**).")
            st.markdown("• **¿Cómo encontramos la mayor fracción unitaria?** Probamos con los alrededores:")
            
            if n > 1:
                st.markdown(f"  - $\\frac{{1}}{{{n-1}}} = {1/(n-1):.3f}$ ❌ **Es mayor** que {valor_actual:.3f} (se pasa).")
            st.markdown(f"  - $\\frac{{1}}{{{n}}} = {1/n:.3f}$ ✅ **Es menor o igual** (es la mayor posible).")
            st.markdown(f"  - $\\frac{{1}}{{{n+1}}} = {1/(n+1):.3f}$ 📉 Es válida, pero **es menor** (nos dejaría un resto más grande).")

            num_ant, den_ant = numerador, denominador
            mcm = math.lcm(den_ant, n)
            st.write(f"• Restamos ambas fracciones. El mínimo común denominador de **{den_ant}** y **{n}** es **{mcm}**.")

            # --- EXPLICACIÓN DIDÁCTICA DE LA RESTA PASO A PASO PARA 3º/4º ESO ---
            # Calculamos los nuevos numeradores con el común denominador
            num1_ampliado = num_ant * (mcm // den_ant)
            num2_ampliado = 1 * (mcm // n)
            
            # Mostramos la conversión a común denominador y la operación agrupada
            paso_resta_latex = fr"\frac{{{num_ant}}}{{{den_ant}}} - \frac{{1}}{{{n}}} = \frac{{{num1_ampliado}}}{{{mcm}}} - \frac{{{num2_ampliado}}}{{{mcm}}} = \frac{{{num1_ampliado} - {num2_ampliado}}}{{{mcm}}}"
            st.latex(paso_resta_latex)
            # -------------------------------------------------------------------

            numerador = int(num1_ampliado - num2_ampliado)
            denominador = mcm

            # Mostramos el resultado final de la resta antes de simplificar
            resta_resultado_latex = fr"= \frac{{{numerador}}}{{{denominador}}}"
            st.latex(resta_resultado_latex)




            

            if numerador > 0:
                mcd = math.gcd(numerador, denominador)
                if mcd > 1:
                    num_simpl = numerador // mcd
                    den_simpl = denominador // mcd
                    st.write(f"• Simplificamos dividiendo numerador y denominador entre el MCD (**{mcd}**):")
                    st.latex(fr"\frac{{{numerador}}}{{{denominador}}} = \frac{{{num_simpl}}}{{{den_simpl}}}")
                    numerador, denominador = num_simpl, den_simpl
                else:
                    st.write("• La fracción resultante ya es irreducible.")

        paso += 1

    suma_fracciones = " + ".join(fracciones_unitarias)
    st.success(f"### 🎉 Resultado final:\n$$\\frac{{{num_orig}}}{{{den_orig}}} = {suma_fracciones}$$")

    # Mostrar la gráfica
    fig = generar_grafico_equivalencia(num_orig, den_orig, fracciones_unitarias)
    st.pyplot(fig)


# --- Ejecución de la app ---
descomponer_y_mostrar(numerador_in, denominador_in)