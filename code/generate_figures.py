import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from collections import Counter
import csv
import os

# ==============================================================================
# MÓDULO 1: HERRAMIENTAS DE TEORÍA DE NÚMEROS
# ==============================================================================

def get_prime_factorization(n):
    if n == 0: return Counter({0: 1})
    n = abs(n)
    factors = Counter()
    d = 2
    temp_n = n
    while d * d <= temp_n:
        while temp_n % d == 0:
            factors[d] += 1
            temp_n //= d
        d += 1
    if temp_n > 1:
        factors[temp_n] += 1
    return factors

def radical_from_factors(factors_a, factors_b, factors_c):
    all_primes = set(factors_a.keys()) | set(factors_b.keys()) | set(factors_c.keys())
    return math.prod(all_primes) if all_primes else 1

def quality_q_from_factors(c, factors_a, factors_b, factors_c):
    rad_abc = radical_from_factors(factors_a, factors_b, factors_c)
    if rad_abc <= 1:
        return float('inf') if c > 1 else 0
    return math.log(c) / math.log(rad_abc)

def calculate_formal_rho(factors_a, factors_b, factors_c):
    all_primes = set(factors_a.keys()) | set(factors_b.keys()) | set(factors_c.keys())
    max_rho = 0
    if not all_primes:
        return 0
    for p in all_primes:
        v_p_a = factors_a.get(p, 0)
        v_p_b = factors_b.get(p, 0)
        v_p_c = factors_c.get(p, 0)
        rho_p_ac = abs(v_p_a - v_p_c)
        rho_p_bc = abs(v_p_b - v_p_c)
        max_rho = max(max_rho, rho_p_ac, rho_p_bc)
    return max_rho

# ==============================================================================
# MÓDULO 2: GENERADOR DE TERNAS
# ==============================================================================

def generate_abc_triples_optimized(c_limit, output_csv):
    print(f"Iniciando generación de ternas ABC hasta c = {c_limit}, guardando en {output_csv}...")
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['a', 'b', 'c', 'Quality (q)', 'Profundidad de Ramificación (ρ)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        count = 0
        for a in range(1, c_limit // 2 + 1):
             for c in range(a + 1, c_limit + 1):
                 b = c - a
                 if a < b and math.gcd(a, b) == 1:
                     factors_a = get_prime_factorization(a)
                     factors_b = get_prime_factorization(b)
                     factors_c = get_prime_factorization(c)
                     q = quality_q_from_factors(c, factors_a, factors_b, factors_c)
                     ramification_depth = calculate_formal_rho(factors_a, factors_b, factors_c)
                     writer.writerow({
                         'a': a, 'b': b, 'c': c,
                         'Quality (q)': q if q is not None else 'NaN',
                         'Profundidad de Ramificación (ρ)': ramification_depth
                     })
                     count += 1
                     if count % 500000 == 0:
                         print(f"  ... {count} ternas analizadas y guardadas.")
    print(f"\nGeneración completada. Total de {count} ternas guardadas en {output_csv}.")
    return output_csv

# ==============================================================================
# MÓDULO 3: EXPERIMENTO PRINCIPAL
# ==============================================================================

def run_abc_experiment(c_limit=20000, quality_threshold=1.4, output_csv='../data/abc_triples_analysis.csv'):
    generated_csv_path = generate_abc_triples_optimized(c_limit, output_csv)
    print(f"Cargando datos desde {generated_csv_path} para visualización...")
    try:
        df = pd.read_csv(generated_csv_path)
        df['Quality (q)'] = pd.to_numeric(df['Quality (q)'], errors='coerce')
        df.dropna(subset=['Quality (q)'], inplace=True)
        df = df[df['Quality (q)'] != float('inf')]
    except FileNotFoundError:
        print(f"ERROR: No se encontró {generated_csv_path}.")
        return
    if df.empty:
        print("DataFrame vacío, no hay datos para visualizar.")
        return
    print(f"Datos cargados. Filas para visualización: {len(df)}")
    notable_hits = df[df['Quality (q)'] > quality_threshold].sort_values(by='Quality (q)', ascending=False)
    print(f"\n--- Hits Notables (q > {quality_threshold}) ---")
    if not notable_hits.empty:
        print(notable_hits.to_string(index=False))
    else:
        print(f"No se encontraron 'hits' con q > {quality_threshold} para c <= {c_limit}.")
    fig, ax = plt.subplots(figsize=(14, 9))
    sample_size = 500000
    df_plot_sample = df.sample(n=min(len(df), sample_size), random_state=42)
    print(f"Graficando una muestra de {len(df_plot_sample)} ternas.")
    ax.scatter(
        df_plot_sample['Profundidad de Ramificación (ρ)'],
        df_plot_sample['Quality (q)'],
        alpha=0.3, s=15, color='blue', label=f'Ternas Primitivas (n={len(df)})'
    )
    if not notable_hits.empty:
        ax.scatter(
            notable_hits['Profundidad de Ramificación (ρ)'],
            notable_hits['Quality (q)'],
            color='red', s=50, edgecolors='black', label=f'Hits Notables (q > {quality_threshold}, n={len(notable_hits)})'
        )
    max_q = df['Quality (q)'].max() if not df.empty else 2
    zone_height = max_q + 0.1 - quality_threshold
    if not notable_hits.empty:
        rho_min_high_q = notable_hits['Profundidad de Ramificación (ρ)'].min()
        zone_width = rho_min_high_q
        print(f"Zona de Exclusión determinada dinámicamente: ρ < {zone_width} para q > {quality_threshold}")
    else:
        zone_width = 5
        print(f"No se encontraron hits. Zona de Exclusión por defecto: ρ < {zone_width} para q > {quality_threshold}")
    exclusion_zone = patches.Rectangle(
        (0, quality_threshold), zone_width, zone_height,
        linewidth=2, linestyle='--', edgecolor='red', facecolor='red', alpha=0.1
    )
    ax.add_patch(exclusion_zone)
    ax.text(
        zone_width / 2, quality_threshold + zone_height / 2,
        'Zona de Exclusión\n(Alta Calidad, Baja Complejidad)',
        color='red', fontsize=12, style='italic', ha='center', va='center'
    )
    ax.set_title('El Mapa del Universo ABC: Calidad vs. Complejidad de Ramificación', fontsize=18)
    ax.set_xlabel('Profundidad de Ramificación (ρ)', fontsize=14)
    ax.set_ylabel('Calidad (q)', fontsize=14)
    ax.legend(fontsize=12)
    ax.grid(True, which='both', linestyle=':', linewidth=0.5)
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0.5)
    output_figure_path = '../figures/quality_vs_rho.png'
    os.makedirs(os.path.dirname(output_figure_path), exist_ok=True)
    plt.savefig(output_figure_path, dpi=300, bbox_inches='tight')
    print(f"Visualización guardada en {output_figure_path}.")
    # plt.show() # Disabled for non-interactive environments

if __name__ == "__main__":
    C_LIMIT = 20000
    QUALITY_THRESHOLD = 1.4
    run_abc_experiment(c_limit=C_LIMIT, quality_threshold=QUALITY_THRESHOLD)
