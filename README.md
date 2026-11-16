# Análisis Espaciotemporal de Congestión Vial mediante Teoría de Grafos
**Proyecto ACECOM - Ciencia de la Computación (UNI)**

## Descripción
Modelado computacional de redes viales urbanas utilizando grafos dirigidos $G=(V,E)$, cálculo del Factor de Congestión ($FC = T_{real} / T_{ideal}$) por franjas horarias y renderización cartográfica interactiva.

## Estructura del Proyecto
- `data/`: Topología vial en formato GraphML y dataset espaciotemporal CSV.
- `src/1_ingesta_datos.py`: Extracción topológica desde OpenStreetMap y generación de matriz horaria.
- `src/2_procesador_grafo.py`: Cálculo de pesos dinámicos y detección de cuellos de botella ($FC \ge 2.0$).
- `src/3_visualizador_mapa.py`: Renderización interactiva multicapa en formato HTML.
