# Instrumentación Biomédica III – UNMSM 2026-II

Escuela Profesional de Ingeniería Biomédica · Facultad de Ingeniería Electrónica y Eléctrica · Universidad Nacional Mayor de San Marcos

## Sobre este repositorio

Este repositorio reunirá todos los laboratorios del curso **Instrumentación Biomédica III**. Cada práctica tendrá su propia carpeta con el código cargado en el microcontrolador, los datos medidos, los scripts de análisis y la documentación (guía, esquemáticos, diagramas y gráficas), para que cada experimento pueda revisarse y reproducirse íntegramente. Los laboratorios se irán agregando a medida que se desarrollen.

## Laboratorios

| N.º | Tema | Carpeta | Estado |
|---|---|---|---|
| 1 | Acondicionamiento de señales de alta impedancia (simulador de electrodo de pH con ESP32 y buffer TL084 / LM324) | [`lab1`](lab1) | Completado |
| 3 | Amplificador de instrumentación de tres op-amps (TL084N) y rechazo de modo común | [`lab3`](lab3) | Completado |

## Organización de cada laboratorio

```
firmware/    Código cargado en el microcontrolador
data/        Datos medidos (CSV)
docs/        Guía, esquemáticos, diagramas y gráficas
hardware/    Proyectos de KiCad
analysis.py  Cálculo de errores y gráficas de resultados
README.md    Objetivos, fundamento, montaje, procedimiento y resultados
```
