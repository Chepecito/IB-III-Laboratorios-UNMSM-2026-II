# IB III – Laboratorio 3: Amplificador de instrumentación y rechazo de modo común

Instrumentación Biomédica III · Escuela Profesional de Ingeniería Biomédica · UNMSM

Se implementa un amplificador de instrumentación de tres amplificadores operacionales con el TL084N, con una ganancia diferencial de diseño de 21. Se mide su respuesta ante una señal diferencial pequeña, comparable a un biopotencial, y ante una señal senoidal de 60 Hz aplicada por igual a ambas entradas, que emula la interferencia de la red eléctrica. Con ambas respuestas se calcula el CMRR.

## Objetivos

- Implementar un amplificador de instrumentación de tres op-amps con ganancia diferencial de diseño igual a 21.
- Medir la ganancia ante una señal diferencial de unos 10 mVpp y contrastarla con el valor calculado a partir de las resistencias medidas.
- Determinar qué fracción de una señal de modo común de 60 Hz llega a la salida y calcular el CMRR.
- Comprobar que el circuito amplifica la señal diferencial y atenúa la de modo común.

## Fundamento en breve

| Concepto | Expresión |
|---|---|
| Señal diferencial y de modo común | V_d = V1 − V2, V_cm = (V1 + V2) / 2 |
| Salida de un amplificador real | V_out = A_d · V_d + A_cm · V_cm |
| Ganancia diferencial (tres op-amps) | A_d = [1 + (R1a + R1b) / Rg] · (R3 / R2) |
| Razón de rechazo de modo común | CMRR = 20 · log10(A_d / A_cm) |

La etapa de entrada (A1 y A2, unidas por Rg) amplifica la señal diferencial y deja pasar el modo común con ganancia unitaria. La etapa restadora (A3) resta ambas salidas y cancela el modo común siempre que R3a/R2a = R3b/R2b. Por eso el CMRR del montaje discreto depende sobre todo del apareamiento de esas cuatro resistencias, que se midieron y aparearon antes de armar el circuito.

## Estructura

```
data/resistencias.csv           Valores nominales y medidos de las resistencias (Tabla 1)
data/mediciones.csv             Mediciones de las etapas A, B y C (Tablas 2 a 4)
analysis.py                     Ganancias, CMRR y error relativo
docs/esquematico_lab3.pdf       Esquemático exportado (etapas A, B y C)
docs/informe/informe_laboratorio_3.pdf   Informe final del grupo
hardware/kicad/                 Proyecto KiCad 10 (esquemático editable)
```

## Circuito

Esquemático: [`docs/esquematico_lab3.pdf`](docs/esquematico_lab3.pdf) (fuente editable en [`hardware/kicad/`](hardware/kicad/)).

| Etapa | Entradas | Objetivo |
|---|---|---|
| A – Montaje y verificación | V1 y V2 a GND | Comprobar que la salida en reposo es prácticamente 0 V |
| B – Señal diferencial | Generador → divisor RD1 = 10 kΩ / RD2 = 100 Ω → una entrada; la otra a GND | Medir A_d con una señal de pocos mVpp |
| C – Modo común | Generador (60 Hz) conectado a ambas entradas | Medir A_cm y calcular el CMRR |

- **A1 y A2:** R1a = R1b = 10 kΩ, Rg = 1 kΩ.
- **A3:** restador con R2a = R2b = R3a = R3b = 10 kΩ.
- **Alimentación:** dual ±12 V, con capacitores cerámicos de 100 nF de desacoplo en el TL084N. El cuarto op-amp del integrado queda como seguidor con la entrada a GND.

**Materiales:** TL084N, 7 resistencias de 10 kΩ, 1 de 1 kΩ y 1 de 100 Ω, 2 capacitores de 100 nF, protoboard, fuente dual, generador Tektronix AFG3022C, osciloscopio Tektronix TBS1154 y multímetro Fluke 115.

## Resultados

Resistencias medidas ([`data/resistencias.csv`](data/resistencias.csv)):

| R1a | R1b | Rg | R2a | R2b | R3a | R3b | RD1 | RD2 |
|---|---|---|---|---|---|---|---|---|
| 9,97 kΩ | 9,91 kΩ | 0,98 kΩ | 9,94 kΩ | 9,95 kΩ | 9,94 kΩ | 9,91 kΩ | 9,92 kΩ | 103,8 Ω |

Mediciones ([`data/mediciones.csv`](data/mediciones.csv)):

| Etapa | Entrada | Salida |
|---|---|---|
| A – Entradas a GND | 0 | 0,002 V DC |
| B – Señal diferencial | 30,3 mVpp | 468 mVpp, desfasada ≈ 180° respecto a V1 |
| C – Modo común (≈ 60 Hz) | 2,05 Vpp | 3,75 mVpp, con ruido |

Resultados calculados con `analysis.py`:

| Magnitud | Valor |
|---|---|
| A_d teórica (resistencias medidas) | 21,24 |
| A_d medida | 15,45 (error relativo 27,3 %) |
| A_cm | 1,83 × 10⁻³ (−54,8 dB) |
| A_cm esperada por el desapareamiento R3a/R2a = 1,000 vs. R3b/R2b = 0,996 | 2,0 × 10⁻³ |
| **CMRR** | **78,53 dB** |

```bash
python analysis.py
```

**Lo que se observó:**

- **El circuito rechaza el modo común.** La entrada de la Etapa C fue unas 68 veces mayor que la de la Etapa B, pero su salida fue unas 125 veces menor.
- **El CMRR lo fija el apareamiento del restador.** La diferencia de 0,4 % entre R3a/R2a y R3b/R2b predice una A_cm del mismo orden que la medida. Sin aparear, con resistencias de 5 % el CMRR en el peor caso habría sido de unos 46 dB, y de unos 60 dB con 1 %.
- **El CMRR medido es una cota inferior.** La salida de la Etapa C estuvo afectada por ruido, así que parte de los 3,75 mVpp no se debe a la señal de prueba y el rechazo real puede ser mayor.
- **La ganancia diferencial medida quedó por debajo de la teórica.** La tolerancia de las resistencias explica solo una parte mínima de la diferencia. El resto se atribuye al divisor RD1/RD2, al generador, a las conexiones en protoboard y a la medición con el osciloscopio.
- **La salida salió invertida respecto a V1.** En el esquemático, la señal entra por la rama de A2, que llega a la entrada no inversora del restador, así que la salida debería estar en fase. El desfase de 180° indica que en la protoboard la señal entró por la rama inversora: es un error de conexión que cambia el signo de la salida, no su magnitud.

**Conclusión.** El amplificador de instrumentación discreto amplifica la señal diferencial y atenúa la de modo común, con un CMRR de 78,5 dB. Ese valor supera el mínimo del TL084 (70 dB) gracias al apareamiento de las resistencias, pero queda por debajo de los 100–120 dB que garantizan amplificadores integrados como el INA128 o el AD620. Para registrar biopotenciales, el CMRR debe complementarse con electrodos de impedancia baja y similar, y con un circuito de pierna derecha.

## Referencias

- Drake Moyano, J. M. (2005). *Tema III: El amplificador de instrumentación*. Universidad de Cantabria. https://www.ctr.unican.es/asignaturas/instrumentacion_5_it/iec_3.pdf
- Acharya, V. (2011). *Improving common-mode rejection using the right-leg drive amplifier* (SBAA188). Texas Instruments. https://www.ti.com/lit/pdf/SBAA188
- Analog Devices. *AD620: Low cost, low power instrumentation amplifier* – Hoja de datos. https://www.analog.com/media/en/technical-documentation/data-sheets/ad620.pdf
- Texas Instruments. *INA128, INA129: Precision, low-power instrumentation amplifiers* – Hoja de datos. https://www.ti.com/lit/ds/symlink/ina128.pdf
- Texas Instruments. *TL08x JFET-input operational amplifiers* – Hoja de datos. https://www.ti.com/lit/ds/symlink/tl084.pdf
- Webster, J. G., & Nimunkar, A. J. (2020). *Medical Instrumentation: Application and Design* (5.ª ed.). John Wiley & Sons.
