from copy import deepcopy
from pathlib import Path

import nbformat


NOTEBOOK_NAME = "AE3_Piedrahita_Cristian_y_Londoño_Santiago.ipynb"
SECTION_A = "## A. Predicción, periodo común y variables"
SECTION_B = "## B. Carga y revisión de los datos"
SECTION_C = "## C. Análisis con NumPy"

C_MARKDOWN = """## C. Análisis con NumPy

Se construyen arrays NumPy para las tres mediciones de cada ciudad. El corte breve muestra los primeros siete días del periodo común. Se define día lluvioso como precipitación diaria ≥ 1 mm y día caliente como temperatura máxima ≥ 30 °C; los mismos umbrales se aplican a ambas ciudades. El centrado de los promedios mensuales de temperatura máxima muestra broadcasting: se resta a una matriz ciudad × mes el vector de promedios por mes compartido."""

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
        "Días lluviosos (≥ 1 mm)": np.count_nonzero(mascaras_lluvia[ciudad]),
        "Días calientes (tmax ≥ 30 °C)": np.count_nonzero(mascaras_calor[ciudad]),
    }
    meses = periodo["time"].dt.month.to_numpy()
    promedios_mensuales_tmax.append(
        np.array([np.mean(tmax[meses == mes]) for mes in range(1, 13)])
    )

print("\\nEstadísticas descriptivas por ciudad:")
display(pd.DataFrame.from_dict(estadisticas, orient="index"))

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


activity_dir = Path(__file__).resolve().parents[1]
notebook_path = activity_dir / NOTEBOOK_NAME
notebook = nbformat.read(notebook_path, as_version=4)

section_indexes = {}
for heading in (SECTION_A, SECTION_B, SECTION_C):
    matches = [
        index
        for index, cell in enumerate(notebook.cells)
        if cell.cell_type == "markdown" and cell.source.startswith(heading)
    ]
    if len(matches) != 1:
        raise ValueError(f"Se esperaba una sola celda con el encabezado: {heading}")
    section_indexes[heading] = matches[0]

section_c_index = section_indexes[SECTION_C]
if not (
    section_indexes[SECTION_A]
    < section_indexes[SECTION_B]
    < section_c_index
):
    raise ValueError("El orden de las secciones A, B y C no es el esperado.")

protected_cells = deepcopy(notebook.cells[:section_c_index])
notebook.cells[section_c_index].source = C_MARKDOWN
notebook.cells.insert(
    section_c_index + 1,
    nbformat.v4.new_code_cell(source=C_CODE),
)

if notebook.cells[:section_c_index] != protected_cells:
    raise RuntimeError("La modificación alteró celdas anteriores a la sección C.")

nbformat.validate(notebook)
nbformat.write(notebook, notebook_path)
print(f"Sección C escrita en {notebook_path}")
