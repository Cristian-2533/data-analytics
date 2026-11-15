from copy import deepcopy
from pathlib import Path

import nbformat


NOTEBOOK_NAME = "AE3_Piedrahita_Cristian_y_Londoño_Santiago.ipynb"
SECTION_D = "## D. Gráficas comparativas"


def replace_once(source, old, new):
    if source.count(old) != 1:
        raise ValueError(f"No se encontró exactamente una vez el texto: {old}")
    return source.replace(old, new, 1)


activity_dir = Path(__file__).resolve().parents[1]
notebook_path = activity_dir / NOTEBOOK_NAME
notebook = nbformat.read(notebook_path, as_version=4)

section_indexes = [
    index
    for index, cell in enumerate(notebook.cells)
    if cell.cell_type == "markdown" and cell.source.startswith(SECTION_D)
]
if len(section_indexes) != 1:
    raise ValueError("Se esperaba una sola celda con el encabezado de D.")

code_index = section_indexes[0] + 1
if code_index >= len(notebook.cells) or notebook.cells[code_index].cell_type != "code":
    raise ValueError("No se encontró la celda de código de la sección D.")

code_cell = notebook.cells[code_index]
original_cells = {
    cell.id: deepcopy(cell)
    for cell in notebook.cells
    if cell.id != code_cell.id
}
source = code_cell.source
replacements = [
    (
        "{tmax_mensual.loc[mes_pico_medellin, 'Medellín']}",
        "{tmax_mensual.loc[mes_pico_medellin, 'Medellín']:.1f}",
    ),
    (
        "{tmax_mensual.loc[mes_pico_kampala, 'Kampala']}",
        "{tmax_mensual.loc[mes_pico_kampala, 'Kampala']:.1f}",
    ),
    (
        "{precipitacion_mensual.loc[mes_lluvioso_medellin, 'Medellín']}",
        "{precipitacion_mensual.loc[mes_lluvioso_medellin, 'Medellín']:.1f}",
    ),
    (
        "{precipitacion_mensual.loc[mes_lluvioso_kampala, 'Kampala']}",
        "{precipitacion_mensual.loc[mes_lluvioso_kampala, 'Kampala']:.1f}",
    ),
    (
        "{mediana_tmin_medellin}",
        "{mediana_tmin_medellin:.1f}",
    ),
    (
        "{mediana_tmin_kampala}",
        "{mediana_tmin_kampala:.1f}",
    ),
]
for old, new in replacements:
    source = replace_once(source, old, new)

code_cell.source = source
code_cell.execution_count = None
code_cell.outputs = []

for cell_id, original_cell in original_cells.items():
    matches = [cell for cell in notebook.cells if cell.id == cell_id]
    if len(matches) != 1 or matches[0] != original_cell:
        raise RuntimeError(f"Se alteró una celda fuera de D: {cell_id}")

nbformat.validate(notebook)
nbformat.write(notebook, notebook_path)
print(f"Textos numéricos de D formateados en {notebook_path}")
