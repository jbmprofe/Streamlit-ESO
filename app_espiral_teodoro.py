import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.markdown("![Visitas](https://visitor-badge.laobi.icu/badge?page_id=app_espiral_teodoro)")
# Muestra el logo centrado o con un ancho personalizado
st.image("logo_newton-salas.jpg", width=180)

st.title("📐 Espiral de Teodoro")
st.write("Triángulos rectángulos cuyas hipotenusas son raíces cuadradas de números naturales")
st.write("La espiral de Teodoro (también llamada espiral de las raíces cuadradas o de Teodoro de Cirene) es una construcción geométrica que permite dibujar de forma muy intuitiva las raíces cuadradas de los números enteros ($\sqrt{2}$, $\sqrt{3}$, $\sqrt{4}$, $\sqrt{5}$...) usando solo el teorema de Pitágoras.")

# Sección teórica explicativa para los alumnos (4º de ESO)
with st.expander("📖 Explicación teórica: ¿Qué es la Espiral de Teodoro?"):
    st.subheader("1. ¿Cómo se construye?")
    st.markdown("""
    La espiral se forma dibujando triángulos rectángulos encadenados paso a paso mediante el **teorema de Pitágoras**:
    * **Primer triángulo ($\\sqrt{2}$):** Se parte de dos catetos que miden exactamente **1 unidad**. Su hipotenusa mide $\\sqrt{1^2 + 1^2} = \\mathbf{\\sqrt{2}}$. 
    * **Segundo triángulo ($\\sqrt{3}$):** Se toma la hipotenusa anterior ($\\sqrt{2}$) como base y se le añade un nuevo cateto perpendicular de **1 unidad**. La nueva hipotenusa mide $\\sqrt{(\\sqrt{2})^2 + 1^2} = \\mathbf{\\sqrt{3}}$.
    * **Siguientes triángulos:** El proceso se repite indefinidamente, añadiendo siempre un cateto exterior de longitud **1** para obtener $\\sqrt{4}$ (que es 2), $\\sqrt{5}$, $\\sqrt{6}$, etc.
    """)
    
    st.subheader("2. ¿Cómo nos ayuda a ver los números irracionales?")
    st.markdown("""
    Los números irracionales como $\\sqrt{2}$ o $\\sqrt{5}$ tienen infinitos decimales no periódicos, lo que dificulta imaginarlos. La espiral resuelve este problema porque:
    * **Mide con precisión exacta:** Aunque no podamos escribir todos sus decimales, la longitud física de cada hipotenusa en el dibujo representa el valor real y exacto del número.
    * **Visualiza el crecimiento:** Permite ver cómo aumentan las magnitudes de manera geométrica y cómo el ritmo de crecimiento de las raíces se va suavizando poco a poco.
    """)
    
    st.info("💡 **Idea clave:** No necesitamos conocer los decimales infinitos para dibujar o comprender el tamaño real de un número irracional; basta con aplicar el teorema de Pitágoras paso a paso.")


with st.container(border=True):
    st.markdown("""
    **📝 ACTIVIDAD:** Traza la espiral de Teodoro utilizando Geogebra, o bien usando escuadra, cartabón y compás, desde el valor de $\\sqrt{2}$ hasta $\\sqrt{10}$. 
    
    Puedes ver una muestra de la actividad en Geogebra en [este enlace web](https://www.geogebra.org/classic/gnemfhmy).
    """)

# Control interactivo mediante menú desplegable (reemplaza al slider para evitar errores de carga)
raiz_elegida = st.selectbox(
    "Selecciona la raíz hasta la que deseas calcular:",
    options=[f"√{i}" for i in range(2, 16)],
    index=5 # Por defecto selecciona √7 (equivalente al valor anterior)
)

# Extraemos el número entero de la opción seleccionada para calcular n_max
n_max = int(raiz_elegida.replace("√", "")) - 1

# Configuración de la figura de Matplotlib
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_aspect('equal')
ax.axis('off') # Ocultar ejes

# Origen de la espiral
origen = np.array([0.0, 0.0])
pos_raices = []

# Listas para almacenar todas las coordenadas X e Y y calcular los límites dinámicos
all_x = [origen[0]]
all_y = [origen[1]]

# Dibujar el primer triángulo (Raíz de 2)
f = 1.0
v1 = np.array([f, 0.0])
v_actual = np.array([f, f])
pos_raices.append(v_actual)
all_x.extend([v1[0], v_actual[0]])
all_y.extend([v1[1], v_actual[1]])

# Dibujar elementos iniciales
ax.plot([origen[0], v1[0]], [origen[1], v1[1]], color='black', linestyle='--')
ax.plot([v1[0], v_actual[0]], [v1[1], v_actual[1]], color='black', linestyle='--')
ax.plot([v_actual[0], origen[0]], [v_actual[1], origen[1]], color='grey', linewidth=3)
ax.text((origen[0] + v1[0])/2, origen[1] - 0.08, "1", ha='center', va='center', fontweight='bold', fontsize=10)
ax.text(v1[0] + 0.08, (origen[1] + v1[1])/2, "1", ha='center', va='center', fontweight='bold', fontsize=10)

# Colores para las hipotenusas
colores = ['indianred', 'orangered', 'saddlebrown', 'darkseagreen',
           'darkolivegreen', 'gold', 'darkorange', 'seagreen',
           'lightseagreen', 'teal', 'chocolate', 'dodgerblue', 'magenta']

# Bucle para generar los siguientes triángulos
vertice_anterior = v_actual
for i in range(3, n_max + 2):
    vec_dir = vertice_anterior - origen
    dist = np.linalg.norm(vec_dir)
    
    unit_dir = vec_dir / dist
    normal_dir = np.array([-unit_dir[1], unit_dir[0]])
    
    nuevo_vertice = vertice_anterior + normal_dir * f
    pos_raices.append(nuevo_vertice)
    all_x.append(nuevo_vertice[0])
    all_y.append(nuevo_vertice[1])
    
    color_hip = colores[(i - 2) % len(colores)]
    
    ax.plot([vertice_anterior[0], nuevo_vertice[0]], 
            [vertice_anterior[1], nuevo_vertice[1]], 
            color='black', linestyle='--')
    
    mid_cateto = (vertice_anterior + nuevo_vertice) / 2
    ax.text(mid_cateto[0] + 0.05, mid_cateto[1] + 0.05, "1", fontsize=10, fontweight='bold')
    
    ax.plot([nuevo_vertice[0], origen[0]], 
            [nuevo_vertice[1], origen[1]], 
            color=color_hip, linewidth=3)
    
    vertice_anterior = nuevo_vertice

# Escribir las etiquetas de las raíces en el exterior
r = 2
for i, pos in enumerate(pos_raices[:n_max]):
    vec_rad = pos - origen
    vec_rad_norm = vec_rad / np.linalg.norm(vec_rad)
    pos_etiqueta = pos + vec_rad_norm * 0.35
    all_x.append(pos_etiqueta[0])
    all_y.append(pos_etiqueta[1])
    
    color_etiqueta = colores[i % len(colores)]
    ax.text(pos_etiqueta[0], pos_etiqueta[1], f"√{r}", 
            ha='center', va='center', fontsize=12, fontweight='bold', color=color_etiqueta)
    r += 1

# Márgenes dinámicos
margin = 1.0
ax.set_xlim(min(all_x) - margin, max(all_x) + margin)
ax.set_ylim(min(all_y) - margin, max(all_y) + margin)

# Mostrar la gráfica en Streamlit
st.pyplot(fig)
