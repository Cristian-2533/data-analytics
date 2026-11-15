from copy import deepcopy
from pathlib import Path

import nbformat


NOTEBOOK_NAME = "AE3_Piedrahita_Cristian_y_Londoño_Santiago.ipynb"
SECTION_C = "## C. Análisis con NumPy"
SECTION_E = "## E. Interpretación de resultados"

C_MARKDOWN = """## C. Análisis con NumPy

Se construyen arrays NumPy para las tres mediciones de cada ciudad. El corte muestra los primeros siete días del periodo común de cada ciudad. El broadcasting centra los promedios mensuales de temperatura máxima respecto al promedio compartido de las ciudades."""

OLD_PREDICTION_TEXT = '''f"- **Predicción previa.** La parte de temperaturas máximas se "
        f"confirma a escala del promedio anual, con una diferencia de "
        f"{diferencia_promedios_tmax:.2f} °C, aunque los picos y la mayor "
        f"diferencia mensual muestran estacionalidad distinta. La predicción "
        f"de que Medellín sería más lluviosa {resultado_prediccion_lluvia}.\\n\\n"'''

NEW_PREDICTION_TEXT = '''f"- **Predicción previa.** La predicción de temperaturas máximas "
        f"similares a lo largo del año se cumplió en el promedio anual "
        f"(diferencia de {diferencia_promedios_tmax:.2f} °C), pero no mes a mes: "
        f"la mayor diferencia mensual fue de {mayor_diferencia_tmax_mensual:.1f} °C "
        f"en {nombres_meses_completos[mes_mayor_diferencia_tmax - 1]}, y los meses "
        f"de mayor promedio fueron distintos: "
        f"{nombres_meses_completos[mes_pico_tmax_medellin - 1]} en Medellín y "
        f"{nombres_meses_completos[mes_pico_tmax_kampala - 1]} en Kampala. "
        f"La predicción de que Medellín sería más lluviosa "
        f"{resultado_prediccion_lluvia}.\\n\\n"'''


repo_root = Path(__file__).resolve().parents[2]
notebook_path = (
    repo_root / "AE3_comparacion_climatica" / NOTEBOOK_NAME
).resolve()
notebook = nbformat.read(notebook_path, as_version=4)


def find_unique_markdown(heading):
    matches = [
        index
        for index, cell in enumerate(notebook.cells)
        if cell.cell_type == "markdown" and cell.source.startswith(heading)
    ]
    if len(matches) != 1:
        raise ValueError(f"Se esperaba una sola celda con el encabezado: {heading}")
    return matches[0]


section_c_index = find_unique_markdown(SECTION_C)
section_e_index = find_unique_markdown(SECTION_E)
c_code_index = section_c_index + 1
e_code_index = section_e_index + 1
if notebook.cells[c_code_index].cell_type != "code":
    raise ValueError("No se encontró la celda de código de la sección C.")
if notebook.cells[e_code_index].cell_type != "code":
    raise ValueError("No se encontró la celda de código de la sección E.")

c_code = notebook.cells[c_code_index].source
for corte in (
    "fechas_comunes[ciudad][:7]",
    "tmax[:7]",
    "tmin[:7]",
    "precipitacion[:7]",
):
    if corte not in c_code:
        raise ValueError(f"El corte de siete días no contiene: {corte}")

e_code = notebook.cells[e_code_index].source
if e_code.count(OLD_PREDICTION_TEXT) != 1:
    raise ValueError("No se encontró exactamente una vez el texto actual de predicción.")

modified_ids = {
    notebook.cells[section_c_index].id,
    notebook.cells[e_code_index].id,
}
original_cells = {
    cell.id: deepcopy(cell)
    for cell in notebook.cells
    if cell.id not in modified_ids
}

notebook.cells[section_c_index].source = C_MARKDOWN
notebook.cells[e_code_index].source = e_code.replace(
    OLD_PREDICTION_TEXT,
    NEW_PREDICTION_TEXT,
    1,
)
notebook.cells[e_code_index].execution_count = None
notebook.cells[e_code_index].outputs = []

for cell_id, original_cell in original_cells.items():
    matches = [cell for cell in notebook.cells if cell.id == cell_id]
    if len(matches) != 1 or matches[0] != original_cell:
        raise RuntimeError(f"Se alteró una celda fuera de los ajustes: {cell_id}")

nbformat.validate(notebook)
nbformat.write(notebook, notebook_path)
print(f"Ajustes finales escritos en {notebook_path}")
