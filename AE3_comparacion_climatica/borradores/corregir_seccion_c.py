from copy import deepcopy
from pathlib import Path

import nbformat


NOTEBOOK_NAME = "AE3_Piedrahita_Cristian_y_Londoño_Santiago.ipynb"
SECTION_C = "## C. Análisis con NumPy"
SECTION_D = "## D. Gráficas comparativas"

C_MARKDOWN = """## C. Análisis con NumPy

Se construyen arrays NumPy para las tres mediciones de cada ciudad. El corte breve muestra un periodo continuo de cada ciudad. Los umbrales de lluvia y calor se definen en las variables `UMBRAL_LLUVIA_MM` y `UMBRAL_CALOR_C` y se aplican de igual manera a ambas ciudades. El broadcasting centra los promedios mensuales de temperatura máxima respecto al promedio compartido de las ciudades."""

C_CODE = '''UMBRAL_LLUVIA_MM = 1.0
UMBRAL_CALOR_C = 30.0
arrays = {}
fechas_comunes = {}
mascaras_lluvia = {}
mascaras_calor = {}
estadisticas = {}
promedios_mensuales_tmax = []

for ciudad, df in datos.items():
    periodo = df.loc[df["time"].between(PERIODO_INICIO, PERIODO_FIN)]
    fechas_comunes[ciudad] = periodo["time"].to_numpy(dtype="datetime64[ns]")
    arrays[ciudad] = {
        columna: periodo[columna].to_numpy(dtype=float)
        for columna in columnas_medicion
    }
    tmax = arrays[ciudad]["temperature_2m_max (°C)"]
    tmin = arrays[ciudad]["temperature_2m_min (°C)"]
    precipitacion = arrays[ciudad]["precipitation_sum (mm)"]
    mascaras_lluvia[ciudad] = np.isfinite(precipitacion) & (
        precipitacion >= UMBRAL_LLUVIA_MM
    )
    mascaras_calor[ciudad] = np.isfinite(tmax) & (tmax >= UMBRAL_CALOR_C)

    print(f"\\n{ciudad}: corte de los primeros siete días")
    display(
        pd.DataFrame(
            {
                "fecha": fechas_comunes[ciudad][:7],
                "temperatura máxima (°C)": tmax[:7],
                "temperatura mínima (°C)": tmin[:7],
                "precipitación (mm)": precipitacion[:7],
            }
        )
    )

    estadisticas[ciudad] = {
        "Temperatura máxima promedio (°C)": np.mean(tmax),
        "Temperatura máxima mínima (°C)": np.min(tmax),
        "Temperatura máxima mayor (°C)": np.max(tmax),
        "Temperatura mínima promedio (°C)": np.mean(tmin),
        "Temperatura mínima menor (°C)": np.min(tmin),
        "Temperatura mínima mayor (°C)": np.max(tmin),
        "Precipitación total (mm)": np.sum(precipitacion),
        f"Días lluviosos (≥ {UMBRAL_LLUVIA_MM:g} mm)": np.count_nonzero(
            mascaras_lluvia[ciudad]
        ),
        f"Días calientes (tmax ≥ {UMBRAL_CALOR_C:g} °C)": np.count_nonzero(
            mascaras_calor[ciudad]
        ),
    }
    meses = periodo["time"].dt.month.to_numpy()
    promedios_mensuales_tmax.append(
        np.array([np.mean(tmax[meses == mes]) for mes in range(1, 13)])
    )

print("\\nEstadísticas descriptivas por ciudad:")
display(pd.DataFrame.from_dict(estadisticas, orient="index"))
display(
    Markdown(
        f"Se definió día lluvioso como precipitación diaria ≥ "
        f"{UMBRAL_LLUVIA_MM:g} mm y día caliente como temperatura máxima ≥ "
        f"{UMBRAL_CALOR_C:g} °C. Ambos umbrales se aplicaron por igual "
        "a las dos ciudades."
    )
)

matriz_mensual_tmax = np.vstack(promedios_mensuales_tmax)
promedio_compartido_por_mes = matriz_mensual_tmax.mean(axis=0)
anomalias_mensuales_tmax = matriz_mensual_tmax - promedio_compartido_por_mes
print(
    "\\nBroadcasting: matriz ciudad × mes",
    matriz_mensual_tmax.shape,
    "menos vector de promedios mensuales",
    promedio_compartido_por_mes.shape,
    "=",
    anomalias_mensuales_tmax.shape,
)
display(
    pd.DataFrame(
        anomalias_mensuales_tmax,
        index=list(datos),
        columns=[f"Mes {mes}" for mes in range(1, 13)],
    )
)'''

C_INTERPRETATION_CODE = '''indice_ciudad = {ciudad: indice for indice, ciudad in enumerate(datos)}
indice_febrero = 1
indice_julio = 6
desviacion_febrero_medellin = anomalias_mensuales_tmax[
    indice_ciudad["Medellín"], indice_febrero
]
desviacion_febrero_kampala = anomalias_mensuales_tmax[
    indice_ciudad["Kampala"], indice_febrero
]
desviacion_julio_medellin = anomalias_mensuales_tmax[
    indice_ciudad["Medellín"], indice_julio
]
desviacion_julio_kampala = anomalias_mensuales_tmax[
    indice_ciudad["Kampala"], indice_julio
]

display(
    Markdown(
        "Cada valor de la matriz es la desviación de la temperatura máxima "
        "mensual de una ciudad respecto al promedio de las dos ciudades "
        "en ese mismo mes. "
        f"En febrero, Medellín se desvía {desviacion_febrero_medellin:.2f} °C "
        f"y Kampala {desviacion_febrero_kampala:.2f} °C; "
        f"en julio, Medellín se desvía {desviacion_julio_medellin:.2f} °C "
        f"y Kampala {desviacion_julio_kampala:.2f} °C. "
        "Como solo hay dos ciudades, sus desviaciones respecto a la media "
        "compartida son iguales en magnitud y opuestas en signo. "
        "Esto describe diferencias relativas y no sus causas."
    )
)'''


activity_dir = Path(__file__).resolve().parents[1]
notebook_path = activity_dir / NOTEBOOK_NAME
notebook = nbformat.read(notebook_path, as_version=4)

section_indexes = {}
for heading in (SECTION_C, SECTION_D):
    matches = [
        index
        for index, cell in enumerate(notebook.cells)
        if cell.cell_type == "markdown" and cell.source.startswith(heading)
    ]
    if len(matches) != 1:
        raise ValueError(f"Se esperaba una sola celda con el encabezado: {heading}")
    section_indexes[heading] = matches[0]

section_c_index = section_indexes[SECTION_C]
section_d_index = section_indexes[SECTION_D]
if section_c_index >= section_d_index or notebook.cells[section_c_index + 1].cell_type != "code":
    raise ValueError("No se encontró la celda de código de la sección C.")

code_cell_index = section_c_index + 1
original_ids = {
    cell.id
    for cell in notebook.cells
    if cell.cell_type != "markdown"
    or not cell.source.startswith(SECTION_C)
}
original_cells = {
    cell.id: deepcopy(cell)
    for cell in notebook.cells
    if cell.id in original_ids and cell.id != notebook.cells[code_cell_index].id
}

notebook.cells[section_c_index].source = C_MARKDOWN
code_cell = notebook.cells[code_cell_index]
code_cell.source = C_CODE
code_cell.execution_count = None
code_cell.outputs = []
notebook.cells.insert(
    code_cell_index + 1,
    nbformat.v4.new_code_cell(source=C_INTERPRETATION_CODE),
)

for cell_id, original_cell in original_cells.items():
    matches = [cell for cell in notebook.cells if cell.id == cell_id]
    if len(matches) != 1 or matches[0] != original_cell:
        raise RuntimeError(f"Se alteró una celda fuera de C: {cell_id}")

nbformat.validate(notebook)
nbformat.write(notebook, notebook_path)
print(f"Sección C actualizada en {notebook_path}")
