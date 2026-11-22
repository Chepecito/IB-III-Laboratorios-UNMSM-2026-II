"""
Instrumentación Biomédica III – Laboratorio 3: amplificador de instrumentación.

Lee data/resistencias.csv y data/mediciones.csv y calcula:

    Ad teórica = [1 + (R1a + R1b) / Rg] · promedio(R3a/R2a, R3b/R2b)
    Ad medida  = Vout / V1          (Etapa B, señal diferencial)
    Acm        = Vout / V1          (Etapa C, señal de modo común)
    CMRR (dB)  = 20 · log10(Ad / Acm)
"""

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def leer(nombre):
    with open(ROOT / "data" / nombre, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    r = {f["resistencia"]: float(f["medido_ohm"]) for f in leer("resistencias.csv")}
    med = {f["etapa"]: f for f in leer("mediciones.csv")}

    etapa1 = 1 + (r["R1a"] + r["R1b"]) / r["Rg"]
    rel_a = r["R3a"] / r["R2a"]
    rel_b = r["R3b"] / r["R2b"]
    ad_teo = etapa1 * (rel_a + rel_b) / 2

    ad_med = float(med["B"]["v_salida_Vpp"]) / float(med["B"]["v_entrada_Vpp"])
    acm = float(med["C"]["v_salida_Vpp"]) / float(med["C"]["v_entrada_Vpp"])
    cmrr_db = 20 * math.log10(ad_med / acm)

    # Acm esperada solo por el desapareamiento del restador (ganancia unitaria)
    acm_desap = abs(rel_a - rel_b) / 2

    print(f"Ganancia de la etapa de entrada   1 + (R1a+R1b)/Rg = {etapa1:.4f}")
    print(f"Relaciones del restador           R3a/R2a = {rel_a:.4f}   R3b/R2b = {rel_b:.4f}")
    print(f"Ad teórica                        {ad_teo:.4f}")
    print(f"Ad medida (Etapa B)               {ad_med:.4f}")
    print(f"Error relativo de Ad              {abs(ad_teo - ad_med) / ad_teo * 100:.2f} %")
    print(f"Acm medida (Etapa C)              {acm:.3e}  ({20 * math.log10(acm):.1f} dB)")
    print(f"Acm por desapareamiento           {acm_desap:.3e}")
    print(f"CMRR                              {cmrr_db:.2f} dB")


if __name__ == "__main__":
    main()
