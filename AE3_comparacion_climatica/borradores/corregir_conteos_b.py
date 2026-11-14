from copy import deepcopy
from pathlib import Path

import nbformat


NOTEBOOK_NAME = "AE3_Piedrahita_Cristian_y_Londoño_Santiago.ipynb"
SECTION_B = "## B. Carga y revisión de los datos"


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
    if cell.cell_type == "markdown" and cell.source.startswith(SECTION_B)
]
if len(section_indexes) != 1:
    raise ValueError("Se esperaba una sola celda con el encabezado de B.")

code_index = section_indexes[0] + 1
if code_index >= len(notebook.cells) or notebook.cells[code_index].cell_type != "code":
    raise ValueError("No se encontró la celda de código de la sección B.")

code_cell = notebook.cells[code_index]
original_cells = {
    cell.id: deepcopy(cell)
    for cell in notebook.cells
    if cell.id != code_cell.id
}
source = code_cell.source
source = replace_once(
    source,
    'columnas_requeridas = ["time", *columnas_medicion]\n',
    'columnas_requeridas = ["time", *columnas_medicion]\n'
    "resumen_calidad = {}\n"
    "dias_esperados = len(pd.date_range(PERIODO_INICIO, PERIODO_FIN, freq=\"D\"))\n",
)
source = replace_once(
    source,
    "    validas = en_periodo & df[columnas_requeridas].notna().all(axis=1)\n",
    "    validas = en_periodo & df[columnas_requeridas].notna().all(axis=1)\n"
    "    observaciones_validas = int(validas.sum())\n"
    "    faltantes_por_columna = df.isna().sum()\n"
    "    fechas_duplicadas = int(df.duplicated(subset=\"time\").sum())\n"
    "    resumen_calidad[ciudad] = {\n"
    '        "observaciones_validas": observaciones_validas,\n'
    '        "dias_esperados": dias_esperados,\n'
    '        "faltantes": int(df[columnas_requeridas].isna().sum().sum()),\n'
    '        "fechas_duplicadas": fechas_duplicadas,\n'
    "    }\n",
)
source = replace_once(
    source,
    '    print("Fechas duplicadas:", int(df.duplicated(subset="time").sum()))\n',
    '    print("Fechas duplicadas:", fechas_duplicadas)\n',
)
source = replace_once(
    source,
    '    print("Observaciones válidas en el periodo común:", int(validas.sum()))',
    '    print("Observaciones válidas en el periodo común:", observaciones_validas)',
)

code_cell.source = source
code_cell.execution_count = None
code_cell.outputs = []

for cell_id, original_cell in original_cells.items():
    matches = [cell for cell in notebook.cells if cell.id == cell_id]
    if len(matches) != 1 or matches[0] != original_cell:
        raise RuntimeError(f"Se alteró una celda fuera de B: {cell_id}")

nbformat.validate(notebook)
nbformat.write(notebook, notebook_path)
print(f"Conteos de calidad de B guardados en {notebook_path}")
