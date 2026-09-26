"""
Instrumentación Biomédica III – Laboratorio 1: análisis del efecto de carga.

Lee data/mediciones_lab1.csv, calcula el error porcentual de cada medición
respecto al voltaje teórico y guarda la gráfica comparativa en
docs/error_carga.png.

    Error (%) = (V_teórico − V_medido) / V_teórico · 100
"""

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent
CSV = ROOT / "data" / "mediciones_lab1.csv"
FIG = ROOT / "docs" / "error_carga.png"

COLUMNAS = {
    "nodoA_multimetro_V": "Nodo A sin buffer (multímetro)",
    "nodoA_osciloscopio_V": "Nodo A sin buffer (osciloscopio)",
    "nodoB_tl084_V": "Nodo B buffer TL084",
    "nodoB_lm324_V": "Nodo B buffer LM324",
}


def error_pct(v_teo, v_med):
    return (v_teo - v_med) / v_teo * 100


def main():
    with open(CSV, newline="", encoding="utf-8") as f:
        filas = list(csv.DictReader(f))

    ph = [f["ph"] for f in filas]
    v_teo = np.array([float(f["v_teorico_V"]) for f in filas])

    errores = {}
    print(f"{'pH':>4} {'V teórico':>10}  " + "  ".join(f"{c:>34}" for c in COLUMNAS.values()))
    for col in COLUMNAS:
        v_med = np.array([float(f[col]) for f in filas])
        errores[col] = error_pct(v_teo, v_med)
    for i, p in enumerate(ph):
        celdas = "  ".join(
            f"{float(filas[i][c]):>24.3f} V ({errores[c][i]:>6.2f} %)" for c in COLUMNAS
        )
        print(f"{p:>4} {v_teo[i]:>8.4f} V  {celdas}")

    x = np.arange(len(ph))
    ancho = 0.2
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for k, (col, etiqueta) in enumerate(COLUMNAS.items()):
        ax.bar(x + (k - 1.5) * ancho, errores[col], ancho, label=etiqueta)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xticks(x, [f"pH {p}" for p in ph])
    ax.set_ylabel("Error respecto al V teórico (%)")
    ax.set_title("Efecto de carga: sin buffer vs. buffer TL084 / LM324")
    ax.legend(fontsize=8)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    FIG.parent.mkdir(exist_ok=True)
    fig.savefig(FIG, dpi=150)
    print(f"\nGráfica guardada en {FIG.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
