import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Calculadora de Momento Flector",
    page_icon="🏗️",
    layout="wide"
)

# Título principal
st.title("🏗️ Calculadora de Momento Flector")
st.markdown("Análisis de vigas simplemente apoyadas con cargas puntuales y distribuidas")

# Sidebar para inputs
st.sidebar.header("📊 Parámetros de la Viga")

# Longitud de la viga
L = st.sidebar.number_input("Longitud de la viga (m)", min_value=0.1, value=10.0, step=0.1)

# Tipo de análisis
analisis_tipo = st.sidebar.selectbox(
    "Tipo de análisis",
    ["Carga puntual", "Carga distribuida uniforme", "Múltiples cargas puntuales"]
)

# Mostrar gráfico
show_graph = st.sidebar.checkbox("Mostrar Gráficos", value=True)

def calcular_momento_carga_puntual(P, a, L, x):
    """Calcula el momento flector para una carga puntual P a distancia 'a' del apoyo izquierdo"""
    b = L - a  # distancia del apoyo derecho
    
    # Reacciones en los apoyos
    RA = P * b / L  # Reacción en apoyo izquierdo
    RB = P * a / L  # Reacción en apoyo derecho
    
    # Momento flector en función de x
    M = np.zeros_like(x)
    
    for i, xi in enumerate(x):
        if xi <= a:
            M[i] = RA * xi
        else:
            M[i] = RA * xi - P * (xi - a)
    
    return M, RA, RB

def calcular_momento_carga_distribuida(w, L, x):
    """Calcula el momento flector para una carga distribuida uniforme w"""
    # Reacciones en los apoyos (simétricas)
    RA = RB = w * L / 2
    
    # Momento flector en función de x
    M = RA * x - w * x**2 / 2
    
    return M, RA, RB

# Interfaz según el tipo de análisis
if analisis_tipo == "Carga puntual":
    st.header("📍 Carga Puntual")
    
    col1, col2 = st.columns(2)
    with col1:
        P = st.number_input("Carga puntual P (kN)", value=100.0, step=1.0)
        a = st.number_input("Distancia desde apoyo izquierdo (m)", min_value=0.1, max_value=L-0.1, value=L/2, step=0.1)
    
    # Cálculos
    x = np.linspace(0, L, 1000)
    M, RA, RB = calcular_momento_carga_puntual(P, a, L, x)
    
    # Momento máximo
    b = L - a
    if a <= L/2:
        x_max = a
        M_max = RA * a
    else:
        x_max = a
        M_max = RA * a
    
    # Momento máximo teórico
    M_max_teorico = P * a * b / L
    
    with col2:
        st.subheader("📊 Resultados")
        st.write(f"**Reacción RA:** {RA:.2f} kN")
        st.write(f"**Reacción RB:** {RB:.2f} kN")
        st.write(f"**Momento máximo:** {M_max_teorico:.2f} kN·m")
        st.write(f"**Posición del momento máximo:** {a:.2f} m")

elif analisis_tipo == "Carga distribuida uniforme":
    st.header("📏 Carga Distribuida Uniforme")
    
    col1, col2 = st.columns(2)
    with col1:
        w = st.number_input("Carga distribuida w (kN/m)", value=10.0, step=0.1)
    
    # Cálculos
    x = np.linspace(0, L, 1000)
    M, RA, RB = calcular_momento_carga_distribuida(w, L, x)
    
    # Momento máximo (en el centro)
    M_max = w * L**2 / 8
    x_max = L / 2
    
    with col2:
        st.subheader("📊 Resultados")
        st.write(f"**Reacción RA:** {RA:.2f} kN")
        st.write(f"**Reacción RB:** {RB:.2f} kN")
        st.write(f"**Momento máximo:** {M_max:.2f} kN·m")
        st.write(f"**Posición del momento máximo:** {x_max:.2f} m")

elif analisis_tipo == "Múltiples cargas puntuales":
    st.header("🔢 Múltiples Cargas Puntuales")
    
    # Número de cargas
    num_cargas = st.number_input("Número de cargas", min_value=1, max_value=5, value=2)
    
    cargas = []
    posiciones = []
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📝 Cargas y Posiciones")
        for i in range(num_cargas):
            P_i = st.number_input(f"Carga {i+1} (kN)", value=50.0, step=1.0, key=f"carga_{i}")
            a_i = st.number_input(f"Posición {i+1} (m)", min_value=0.1, max_value=L-0.1, value=(i+1)*L/(num_cargas+1), step=0.1, key=f"pos_{i}")
            cargas.append(P_i)
            posiciones.append(a_i)
    
    # Cálculos para múltiples cargas
    x = np.linspace(0, L, 1000)
    M_total = np.zeros_like(x)
    RA_total = 0
    RB_total = 0
    
    for P_i, a_i in zip(cargas, posiciones):
        M_i, RA_i, RB_i = calcular_momento_carga_puntual(P_i, a_i, L, x)
        M_total += M_i
        RA_total += RA_i
        RB_total += RB_i
    
    M_max = np.max(M_total)
    x_max = x[np.argmax(M_total)]
    
    with col2:
        st.subheader("📊 Resultados")
        st.write(f"**Reacción RA:** {RA_total:.2f} kN")
        st.write(f"**Reacción RB:** {RB_total:.2f} kN")
        st.write(f"**Momento máximo:** {M_max:.2f} kN·m")
        st.write(f"**Posición del momento máximo:** {x_max:.2f} m")
        
        # Tabla de cargas
        df_cargas = pd.DataFrame({
            'Carga (kN)': cargas,
            'Posición (m)': posiciones
        })
        st.subheader("📋 Resumen de Cargas")
        st.dataframe(df_cargas)

# Gráficos
if show_graph:
    st.markdown("---")
    st.header("📈 Visualización")
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Gráfico 1: Esquema de la viga
    ax1.set_xlim(-0.5, L + 0.5)
    ax1.set_ylim(-2, 3)
    
    # Dibujar la viga
    ax1.plot([0, L], [0, 0], 'k-', linewidth=8, label='Viga')
    
    # Dibujar apoyos
    ax1.plot(0, 0, '^', markersize=15, color='red', label='Apoyo A')
    ax1.plot(L, 0, '^', markersize=15, color='red', label='Apoyo B')
    
    # Dibujar cargas según el tipo
    if analisis_tipo == "Carga puntual":
        ax1.arrow(a, 2, 0, -1.5, head_width=0.1, head_length=0.1, fc='blue', ec='blue')
        ax1.text(a, 2.5, f'P = {P} kN', ha='center', fontsize=10, color='blue')
    elif analisis_tipo == "Carga distribuida uniforme":
        for xi in np.linspace(0, L, 20):
            ax1.arrow(xi, 2, 0, -1.5, head_width=0.05, head_length=0.05, fc='green', ec='green', alpha=0.7)
        ax1.text(L/2, 2.5, f'w = {w} kN/m', ha='center', fontsize=10, color='green')
    elif analisis_tipo == "Múltiples cargas puntuales":
        for i, (P_i, a_i) in enumerate(zip(cargas, posiciones)):
            ax1.arrow(a_i, 2, 0, -1.5, head_width=0.1, head_length=0.1, fc='purple', ec='purple')
            ax1.text(a_i, 2.5, f'P{i+1} = {P_i} kN', ha='center', fontsize=8, color='purple')
    
    # Mostrar reacciones
    if analisis_tipo == "Múltiples cargas puntuales":
        ax1.text(0, -1.5, f'RA = {RA_total:.1f} kN', ha='center', fontsize=10, color='red')
        ax1.text(L, -1.5, f'RB = {RB_total:.1f} kN', ha='center', fontsize=10, color='red')
    else:
        ax1.text(0, -1.5, f'RA = {RA:.1f} kN', ha='center', fontsize=10, color='red')
        ax1.text(L, -1.5, f'RB = {RB:.1f} kN', ha='center', fontsize=10, color='red')
    
    ax1.set_xlabel('Posición (m)')
    ax1.set_title('Esquema de la Viga', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Gráfico 2: Diagrama de momento flector
    if analisis_tipo == "Múltiples cargas puntuales":
        ax2.plot(x, M_total, 'b-', linewidth=2, label='Momento flector')
        ax2.fill_between(x, M_total, alpha=0.3)
        ax2.plot(x_max, M_max, 'ro', markersize=8, label=f'Momento máximo: {M_max:.2f} kN·m')
    else:
        ax2.plot(x, M, 'b-', linewidth=2, label='Momento flector')
        ax2.fill_between(x, M, alpha=0.3)
        if analisis_tipo == "Carga puntual":
            ax2.plot(x_max, M_max_teorico, 'ro', markersize=8, label=f'Momento máximo: {M_max_teorico:.2f} kN·m')
        else:
            ax2.plot(x_max, M_max, 'ro', markersize=8, label=f'Momento máximo: {M_max:.2f} kN·m')
    
    ax2.set_xlabel('Posición (m)')
    ax2.set_ylabel('Momento flector (kN·m)')
    ax2.set_title('Diagrama de Momento Flector', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    ax2.axhline(y=0, color='k', linewidth=0.5)
    
    plt.tight_layout()
    st.pyplot(fig)

# Información adicional
st.markdown("---")
st.header("ℹ️ Información Teórica")

col3, col4 = st.columns(2)

with col3:
    st.subheader("📚 Fórmulas Importantes")
    if analisis_tipo == "Carga puntual":
        st.latex(r"M_{max} = \frac{Pab}{L}")
        st.latex(r"R_A = \frac{Pb}{L}, \quad R_B = \frac{Pa}{L}")
    elif analisis_tipo == "Carga distribuida uniforme":
        st.latex(r"M_{max} = \frac{wL^2}{8}")
        st.latex(r"R_A = R_B = \frac{wL}{2}")

with col4:
    st.subheader("🔧 Convenciones")
    st.markdown("""
    - **Momento positivo**: Fibra inferior a tracción
    - **Momento negativo**: Fibra superior a tracción
    - **Reacciones**: Fuerzas hacia arriba son positivas
    - **Cargas**: Fuerzas hacia abajo son positivas
    """)

# Footer
st.markdown("---")
st.markdown("*Calculadora de Momento Flector para Ingeniería Estructural*")