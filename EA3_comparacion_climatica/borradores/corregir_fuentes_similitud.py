from pathlib import Path
import re
import sys

import nbformat


notebook_directory = Path("EA3_comparacion_climatica")
notebook_paths = list(notebook_directory.glob("EA3_*.ipynb"))
if len(notebook_paths) != 1:
    raise RuntimeError(
        f"Se esperaba exactamente un notebook EA3; encontrados: {len(notebook_paths)}"
    )

notebook_path = notebook_paths[0]
with notebook_path.open(encoding="utf-8") as notebook_file:
    notebook = nbformat.read(notebook_file, as_version=4)

if sys.argv[1:] == ["--verify"]:
    print("CELDAS:", len(notebook.cells))
    for index, cell in enumerate(notebook.cells):
        if cell.cell_type == "markdown":
            headings = re.findall(r"(?m)^#{1,6} .+$", cell.source)
            if headings:
                print(f"Markdown {index}: {headings}")

    source_cells = [
        cell
        for cell in notebook.cells
        if cell.cell_type == "markdown"
        and cell.source.startswith("### Fuentes y periodo común")
    ]
    answer_cells = [
        cell
        for cell in notebook.cells
        if cell.cell_type == "markdown"
        and cell.source.startswith(
            "### Respuesta a la pregunta guía: similitud y diferencia"
        )
    ]
    print(
        "NUEVAS CELDAS MARKDOWN:",
        len(source_cells) == 1 and len(answer_cells) == 1,
        "Fuentes:", len(source_cells),
        "Respuesta:", len(answer_cells),
    )

    rendered_outputs = []
    for cell in notebook.cells:
        for output in cell.get("outputs", []):
            if "text" in output:
                rendered_outputs.append(str(output["text"]))
            for mime_type in ("text/markdown", "text/plain", "text/html"):
                value = output.get("data", {}).get(mime_type)
                if isinstance(value, str):
                    rendered_outputs.append(value)
    execution_text = "\n".join(rendered_outputs)
    claims = [
        "27.0 °C en Medellín y 26.8 °C en Kampala",
        "diferencia absoluta de 0.12 °C",
        "abril en Medellín (316.7 mm) y abril en Kampala (185.3 mm)",
        "El total fue 2193.9 mm en Medellín y 1207.9 mm en Kampala",
        "hubo 267 y 217 días lluviosos",
        "16.5/16.6 °C en Medellín y 17.9/17.9 °C en Kampala",
        "1 día en Medellín y 18 días en Kampala",
        "febrero (3.3 °C)",
    ]
    print("COMPARACIÓN CONTRA SALIDAS:")
    for claim in claims:
        print(("COINCIDE" if claim in execution_text else "NO COINCIDE"), "-", claim)
    for figure in ("21.7", "21.4", "2025-01-01", "2025-12-31"):
        matching_cells = [
            index
            for index, cell in enumerate(notebook.cells)
            if any(
                figure in str(output.get("text", ""))
                or any(
                    figure in str(value)
                    for value in output.get("data", {}).values()
                    if isinstance(value, str)
                )
                for output in cell.get("outputs", [])
            )
        ]
        print(f"VALOR {figure}: celdas con salida {matching_cells}")
        if figure in ("21.7", "21.4"):
            for index in matching_cells:
                for output in notebook.cells[index].get("outputs", []):
                    texts = [str(output.get("text", ""))]
                    texts.extend(
                        str(value)
                        for value in output.get("data", {}).values()
                        if isinstance(value, str)
                    )
                    for text in texts:
                        position = text.find(figure)
                        if position >= 0:
                            excerpt = text[max(0, position - 100) : position + 120]
                            print(f"CONTEXTO {figure} en celda {index}: {excerpt}")
    raise SystemExit(0)

section_a_indexes = [
    index
    for index, cell in enumerate(notebook.cells)
    if cell.cell_type == "markdown"
    and cell.source.startswith("## A. Predicción, periodo común y variables")
]
section_e_indexes = [
    index
    for index, cell in enumerate(notebook.cells)
    if cell.cell_type == "markdown"
    and cell.source.startswith("## E. Interpretación de resultados")
]
if len(section_a_indexes) != 1 or len(section_e_indexes) != 1:
    raise RuntimeError("No se encontraron de forma única las secciones A y E.")

sources_heading = "### Fuentes y periodo común"
answer_heading = "### Respuesta a la pregunta guía: similitud y diferencia"
if any(
    cell.cell_type == "markdown"
    and (cell.source.startswith(sources_heading) or cell.source.startswith(answer_heading))
    for cell in notebook.cells
):
    raise RuntimeError("Ya existe alguna de las celdas Markdown que se iban a insertar.")

old_label = "Similitud y estacionalidad de las máximas"
new_label = "Similitud (y su matiz estacional) en las temperaturas máximas"
matching_code_cells = [
    cell
    for cell in notebook.cells
    if cell.cell_type == "code" and old_label in cell.source
]
if len(matching_code_cells) != 1:
    raise RuntimeError(f"Se esperaba un único rótulo por cambiar; encontrados: {len(matching_code_cells)}.")
matching_code_cells[0].source = matching_code_cells[0].source.replace(
    old_label, new_label, 1
)

sources_cell = nbformat.v4.new_markdown_cell(
    """### Fuentes y periodo común

| Ciudad | Fuente | Enlace | Periodo común | Frecuencia | Variables y unidades |
|---|---|---|---|---|---|
| Medellín, Colombia | Open-Meteo, Historical Weather API | https://open-meteo.com/en/docs/historical-weather-api | Del 1 de enero de 2025 (2025-01-01) al 31 de diciembre de 2025 (2025-12-31) | Diaria | Temperatura máxima (°C), temperatura mínima (°C), precipitación (mm) |
| Kampala, Uganda | Open-Meteo, Historical Weather API | https://open-meteo.com/en/docs/historical-weather-api | Del 1 de enero de 2025 (2025-01-01) al 31 de diciembre de 2025 (2025-12-31) | Diaria | Temperatura máxima (°C), temperatura mínima (°C), precipitación (mm) |

Referencias adicionales: Zippenfennig, P. (2023). Open-Meteo.com Weather API. https://doi.org/10.5281/zenodo.7970649 · Hersbach et al. (2020). The ERA5 global reanalysis. https://doi.org/10.1002/qj.3803 · Consulta y descarga: 14 de noviembre de 2026. Los datos son de reanálisis/modelo, no de estaciones."""
)
answer_cell = nbformat.v4.new_markdown_cell(
    """### Respuesta a la pregunta guía: similitud y diferencia

**Similitud (con cifras).** Las dos ciudades tienen una temperatura máxima anual casi igual: 27.0 °C en Medellín y 26.8 °C en Kampala, una diferencia de solo 0.12 °C. Además, ambas tuvieron abril como mes más lluvioso (316.7 mm en Medellín y 185.3 mm en Kampala) y el rango de la temperatura máxima diaria empieza en valores parecidos (21.7 °C en Medellín y 21.4 °C en Kampala).

**Diferencia (con cifras).** Medellín acumuló 2193.9 mm de lluvia frente a 1207.9 mm en Kampala, y tuvo 267 días lluviosos (≥ 1 mm) frente a 217. La temperatura mínima promedio fue 16.5 °C en Medellín y 17.9 °C en Kampala, y los días con temperatura máxima ≥ 30 °C fueron 1 en Medellín y 18 en Kampala.

**Matiz.** Aunque el promedio anual de la temperatura máxima es casi igual, mes a mes no lo es: la mayor diferencia fue en febrero (3.3 °C). Estos resultados describen 2025, con datos modelados, y no permiten atribuir causas."""
)

notebook.cells.insert(section_a_indexes[0] + 1, sources_cell)
notebook.cells.append(answer_cell)
with notebook_path.open("w", encoding="utf-8") as notebook_file:
    nbformat.write(notebook, notebook_file)

print("CELDAS:", len(notebook.cells))
for index, cell in enumerate(notebook.cells):
    if cell.cell_type == "markdown":
        headings = re.findall(r"(?m)^#{1,6} .+$", cell.source)
        if headings:
            print(f"Markdown {index}: {headings}")
