from copy import deepcopy
from pathlib import Path

import nbformat


NOTEBOOK_NAME = "AE3_Piedrahita_Cristian_y_Londoño_Santiago.ipynb"
SECTION_A = "## A. Predicción, periodo común y variables"
SECTION_B = "## B. Carga y revisión de los datos"
SECTION_C = "## C. Análisis con NumPy"
SECTION_D = "## D. Gráficas comparativas"
SECTION_E = "## E. Interpretación de resultados"

E_MARKDOWN = """## E. Interpretación de resultados

Los hallazgos de abajo se generan a partir de las estadísticas calculadas en las secciones anteriores; no implican causalidad.

La comparación se restringe al periodo común de 2025, por lo que describe ese año y no establece por sí sola patrones de largo plazo. Los datos diarios se agregan en hora local: Medellín usa `America/Bogota` y Kampala `Africa/Kampala`, de modo que sus límites de día no corresponden al mismo intervalo UTC. Además, Open-Meteo entrega datos de reanálisis/modelo, no mediciones de estaciones; las diferencias observadas deben interpretarse considerando esa fuente y su resolución."""

E_CODE = '''from IPython.display import Markdown

promedio_tmax_medellin = estadisticas["Medellín"][
    "Temperatura máxima promedio (°C)"
]
promedio_tmax_kampala = estadisticas["Kampala"][
    "Temperatura máxima promedio (°C)"
]
diferencia_promedios_tmax = abs(
    promedio_tmax_medellin - promedio_tmax_kampala
)

total_precipitacion_medellin = estadisticas["Medellín"][
    "Precipitación total (mm)"
]
total_precipitacion_kampala = estadisticas["Kampala"][
    "Precipitación total (mm)"
]
dias_lluviosos_medellin = estadisticas["Medellín"]["Días lluviosos (≥ 1 mm)"]
dias_lluviosos_kampala = estadisticas["Kampala"]["Días lluviosos (≥ 1 mm)"]

display(
    Markdown(
        f"1. **Similitud:** los promedios anuales de temperatura máxima "
        f"fueron {promedio_tmax_medellin} °C en Medellín y "
        f"{promedio_tmax_kampala} °C en Kampala; la diferencia absoluta "
        f"calculada es {diferencia_promedios_tmax} °C. "
        f"2. **Diferencia:** la precipitación acumulada fue "
        f"{total_precipitacion_medellin} mm en Medellín y "
        f"{total_precipitacion_kampala} mm en Kampala; con el umbral "
        f"de 1 mm, se contaron {dias_lluviosos_medellin} y "
        f"{dias_lluviosos_kampala} días lluviosos, respectivamente. "
        "Estas comparaciones describen los datos del periodo estudiado, "
        "pero no identifican causas."
    )
)'''


activity_dir = Path(__file__).resolve().parents[1]
notebook_path = activity_dir / NOTEBOOK_NAME
notebook = nbformat.read(notebook_path, as_version=4)

section_indexes = {}
for heading in (SECTION_A, SECTION_B, SECTION_C, SECTION_D, SECTION_E):
    matches = [
        index
        for index, cell in enumerate(notebook.cells)
        if cell.cell_type == "markdown" and cell.source.startswith(heading)
    ]
    if len(matches) != 1:
        raise ValueError(f"Se esperaba una sola celda con el encabezado: {heading}")
    section_indexes[heading] = matches[0]

section_e_index = section_indexes[SECTION_E]
if not (
    section_indexes[SECTION_A]
    < section_indexes[SECTION_B]
    < section_indexes[SECTION_C]
    < section_indexes[SECTION_D]
    < section_e_index
):
    raise ValueError("El orden de las secciones A, B, C, D y E no es el esperado.")

protected_cells = deepcopy(notebook.cells[:section_e_index])
notebook.cells[section_e_index].source = E_MARKDOWN
notebook.cells.insert(
    section_e_index + 1,
    nbformat.v4.new_code_cell(source=E_CODE),
)

if notebook.cells[:section_e_index] != protected_cells:
    raise RuntimeError("La modificación alteró celdas anteriores a la sección E.")

nbformat.validate(notebook)
nbformat.write(notebook, notebook_path)
print(f"Sección E escrita en {notebook_path}")
