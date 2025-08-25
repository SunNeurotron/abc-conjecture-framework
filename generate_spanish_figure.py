import matplotlib.pyplot as plt
import numpy as np
import os

def generar_figura_principal():
    """
    Genera y guarda la figura 'El Mapa del Universo ABC' con datos simulados
    que se asemejan a la imagen original.
    """
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(14, 9))

    # --- Simulación de Datos ---
    np.random.seed(42)

    # 1. Nube de Ternas Primitivas (simulación visual)
    # Columnas densas de puntos en valores enteros de rho
    for rho_val in range(2, 15):
        n_points = np.random.randint(200, 500)
        q_points = np.random.normal(loc=0.55, scale=0.1, size=n_points)
        ax.scatter([rho_val] * n_points, q_points, color='blue', alpha=0.3, s=15, edgecolor='none')

    # Puntos dispersos adicionales
    rho_sparse = np.random.uniform(1, 14, size=200)
    q_sparse = np.random.uniform(0.7, 1.2, size=200)
    ax.scatter(rho_sparse, q_sparse, color='lightblue', alpha=0.5, s=20)

    # Etiqueta para la nube (usando un punto representativo)
    ax.scatter([], [], color='blue', alpha=0.4, label='"Nube" de Ternas Primitivas (n=60795197)')

    # 2. Constelación de Hits (basado en la imagen)
    rho_hits = [4.5, 7.5, 7.5]
    q_hits = [1.45, 1.58, 1.42]
    ax.scatter(rho_hits, q_hits, color='red', edgecolor='black', s=120,
               label='"Constelación" de Hits (q > 1.4, n=3)')

    # 3. Zona de Exclusión
    ax.add_patch(plt.Rectangle((0.5, 1.4), 4.5, 0.28,
                               color='red', alpha=0.1, linestyle='--', linewidth=2))
    ax.text(2.75, 1.5, 'Zona de Exclusión\n(Alta Calidad, Baja Complejidad)',
            color='red', fontsize=14, ha='center', va='center')

    # --- Estilo y Etiquetas (en español, como en la imagen original) ---
    ax.set_title("El Mapa del Universo ABC: Calidad vs. Complejidad de Ramificación", fontsize=20)
    ax.set_xlabel("Profundidad de Ramificación (max|v_p|)", fontsize=14)
    ax.set_ylabel("Calidad (q)", fontsize=14)

    ax.set_xlim(0, 14.5)
    ax.set_ylim(0, 1.8)

    ax.legend(fontsize=12)

    # --- Guardar la Figura ---
    output_filename = "mapa_del_universo_abc.png"
    plt.savefig(output_filename, dpi=200, bbox_inches='tight')
    plt.close(fig)

    print(f"✅ Figura creada y guardada como: '{output_filename}'")

# Ejecutar la función para crear la figura
generar_figura_principal()
