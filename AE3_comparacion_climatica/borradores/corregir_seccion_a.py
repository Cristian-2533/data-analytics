from copy import deepcopy
from pathlib import Path

import nbformat


NOTEBOOK_NAME = "AE3_Piedrahita_Cristian_y_Londoño_Santiago.ipynb"
SECTION_A = "## A. Predicción, periodo común y variables"
SECTION_B = "## B. Carga y revisión de los datos"

A_MARKDOWN = """## A. Predicción, periodo común y variables

**Predicción previa:** Esperaba que Medellín y Kampala, por estar cerca del ecuador y a altitudes parecidas, tuvieran temperaturas máximas similares a lo largo del año, y que Medellín fuera la ciudad más lluviosa.

La comparación usa el periodo común de ambas ciudades y las variables de temperatura máxima, temperatura mínima y precipitación diaria. Los metadatos, la fuente específica y su fecha de descarga se muestran a continuación desde variables del notebook."""

A_METADATA_CODE = '''from IPython.display import Markdown, display

FECHA_DESCARGA = pd.Timestamp("2026-11-14")
URL_FUENTE_OPEN_METEO = (
    "https://open-meteo.com/en/docs/historical-weather-api"
)
METADATOS_CIUDADES = {
    "Medellín, Colombia": {
        "latitud": 6.22,
        "longitud": -75.55,
        "elevacion_m": 1476,
        "zona_horaria": "America/Bogota",
    },
    "Kampala, Uganda": {
        "latitud": 0.39,
        "longitud": 32.58,
        "elevacion_m": 1174,
        "zona_horaria": "Africa/Kampala",
    },
}

filas_metadatos = []
for ciudad, metadatos in METADATOS_CIUDADES.items():
    direccion_longitud = "O" if metadatos["longitud"] < 0 else "E"
    filas_metadatos.append(
        f"| {ciudad} | "
        f"{metadatos['latitud']:.2f}° N, "
        f"{abs(metadatos['longitud']):.2f}° {direccion_longitud} | "
        f"{metadatos['elevacion_m']:.0f} m | "
        f"`{metadatos['zona_horaria']}` |"
    )

display(
    Markdown(
        f"**Periodo común:** {PERIODO_INICIO.strftime('%d/%m/%Y')} a "
        f"{PERIODO_FIN.strftime('%d/%m/%Y')}, con observaciones diarias. "
        "Las temperaturas se expresan en °C y la precipitación en mm.\\n\\n"
        "| Ciudad | Coordenadas | Elevación | Zona horaria local |\\n"
        "|---|---:|---:|---|\\n"
        + "\\n".join(filas_metadatos)
        + f"\\n\\n**Fuente:** [Open-Meteo Historical Weather API]"
        f"({URL_FUENTE_OPEN_METEO}), datos de reanálisis/modelo, no de "
        "estaciones meteorológicas. "
        f"**Fecha de descarga:** {FECHA_DESCARGA.day} de noviembre de "
        f"{FECHA_DESCARGA.year}."
    )
)'''


activity_dir = Path(__file__).resolve().parents[1]
notebook_path = activity_dir / NOTEBOOK_NAME
notebook = nbformat.read(notebook_path, as_version=4)

section_indexes = {}
for heading in (SECTION_A, SECTION_B):
    matches = [
        index
        for index, cell in enumerate(notebook.cells)
        if cell.cell_type == "markdown" and cell.source.startswith(heading)
    ]
    if len(matches) != 1:
        raise ValueError(f"Se esperaba una sola celda con el encabezado: {heading}")
    section_indexes[heading] = matches[0]

section_a_index = section_indexes[SECTION_A]
section_b_index = section_indexes[SECTION_B]
setup_matches = [
    index
    for index in range(section_a_index + 1, section_b_index)
    if notebook.cells[index].cell_type == "code"
    and "PERIODO_INICIO =" in notebook.cells[index].source
]
if section_a_index >= section_b_index or len(setup_matches) != 1:
    raise ValueError("No se encontró la celda de preparación entre A y B.")

original_cells = {
    cell.id: deepcopy(cell)
    for cell in notebook.cells
    if cell.cell_type != "markdown" or not cell.source.startswith(SECTION_A)
}
notebook.cells[section_a_index].source = A_MARKDOWN
notebook.cells.insert(
    setup_matches[0] + 1,
    nbformat.v4.new_code_cell(source=A_METADATA_CODE),
)

for cell_id, original_cell in original_cells.items():
    matches = [cell for cell in notebook.cells if cell.id == cell_id]
    if len(matches) != 1 or matches[0] != original_cell:
        raise RuntimeError(f"Se alteró una celda fuera de A: {cell_id}")

nbformat.validate(notebook)
nbformat.write(notebook, notebook_path)
print(f"Sección A actualizada en {notebook_path}")
