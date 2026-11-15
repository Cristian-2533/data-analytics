from copy import deepcopy
from pathlib import Path

import nbformat


NOTEBOOK_NAME = "AE3_Piedrahita_Cristian_y_Londoño_Santiago.ipynb"
SECTION_E = "## E. Interpretación de resultados"

E_MARKDOWN = """## E. Interpretación de resultados

Los hallazgos y el contexto de la comparación se generan a partir de las variables calculadas en las secciones anteriores. Se describen diferencias observadas sin atribuir causalidad."""

E_CODE = '''from IPython.display import Markdown

nombres_meses_completos = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
]
key_dias_lluviosos = f"Días lluviosos (≥ {UMBRAL_LLUVIA_MM:g} mm)"
key_dias_calor = f"Días calientes (tmax ≥ {UMBRAL_CALOR_C:g} °C)"

promedio_tmax_medellin = estadisticas["Medellín"][
    "Temperatura máxima promedio (°C)"
]
promedio_tmax_kampala = estadisticas["Kampala"][
    "Temperatura máxima promedio (°C)"
]
diferencia_promedios_tmax = abs(
    promedio_tmax_medellin - promedio_tmax_kampala
)
mes_pico_tmax_medellin = int(tmax_mensual["Medellín"].idxmax())
mes_pico_tmax_kampala = int(tmax_mensual["Kampala"].idxmax())
diferencias_tmax_mensuales = (
    tmax_mensual["Medellín"] - tmax_mensual["Kampala"]
).abs()
mes_mayor_diferencia_tmax = int(diferencias_tmax_mensuales.idxmax())
mayor_diferencia_tmax_mensual = float(
    diferencias_tmax_mensuales.loc[mes_mayor_diferencia_tmax]
)

total_precipitacion_medellin = estadisticas["Medellín"][
    "Precipitación total (mm)"
]
total_precipitacion_kampala = estadisticas["Kampala"][
    "Precipitación total (mm)"
]
dias_lluviosos_medellin = estadisticas["Medellín"][key_dias_lluviosos]
dias_lluviosos_kampala = estadisticas["Kampala"][key_dias_lluviosos]
mes_lluvioso_medellin = int(precipitacion_mensual["Medellín"].idxmax())
mes_lluvioso_kampala = int(precipitacion_mensual["Kampala"].idxmax())
mes_seco_medellin = int(precipitacion_mensual["Medellín"].idxmin())
total_mes_seco_medellin = float(
    precipitacion_mensual.loc[mes_seco_medellin, "Medellín"]
)

promedio_tmin_medellin = estadisticas["Medellín"][
    "Temperatura mínima promedio (°C)"
]
promedio_tmin_kampala = estadisticas["Kampala"][
    "Temperatura mínima promedio (°C)"
]
mediana_tmin_medellin = float(
    np.median(arrays["Medellín"]["temperature_2m_min (°C)"])
)
mediana_tmin_kampala = float(
    np.median(arrays["Kampala"]["temperature_2m_min (°C)"])
)
dias_calor_medellin = estadisticas["Medellín"][key_dias_calor]
dias_calor_kampala = estadisticas["Kampala"][key_dias_calor]

def formato_conteo_dias(conteo):
    unidad = "día" if conteo == 1 else "días"
    return f"{conteo} {unidad}"

calidad_medellin = resumen_calidad["Medellín"]
calidad_kampala = resumen_calidad["Kampala"]
fechas_medellin = datos["Medellín"].loc[
    datos["Medellín"]["time"].between(PERIODO_INICIO, PERIODO_FIN), "time"
].to_numpy(dtype="datetime64[ns]")
fechas_kampala = datos["Kampala"].loc[
    datos["Kampala"]["time"].between(PERIODO_INICIO, PERIODO_FIN), "time"
].to_numpy(dtype="datetime64[ns]")
fechas_compartidas = np.intersect1d(fechas_medellin, fechas_kampala)

if (
    calidad_medellin["faltantes"] == 0
    and calidad_kampala["faltantes"] == 0
    and calidad_medellin["fechas_duplicadas"] == 0
    and calidad_kampala["fechas_duplicadas"] == 0
):
    texto_calidad = (
        "No hubo faltantes ni duplicados, por lo que no se eliminó ni "
        "se rellenó ningún día. "
    )
else:
    texto_calidad = (
        "No se rellenaron datos ni se eliminaron filas durante la revisión. "
    )

prediccion_lluvia_confirmada = (
    total_precipitacion_medellin > total_precipitacion_kampala
    and dias_lluviosos_medellin > dias_lluviosos_kampala
)
resultado_prediccion_lluvia = (
    "se confirma en el periodo estudiado"
    if prediccion_lluvia_confirmada
    else "no se confirma por ambos indicadores en el periodo estudiado"
)

timezone_medellin = METADATOS_CIUDADES["Medellín, Colombia"]["zona_horaria"]
timezone_kampala = METADATOS_CIUDADES["Kampala, Uganda"]["zona_horaria"]

display(
    Markdown(
        f"- **Similitud y estacionalidad de las máximas.** El promedio "
        f"anual de temperatura máxima fue {promedio_tmax_medellin:.1f} °C "
        f"en Medellín y {promedio_tmax_kampala:.1f} °C en Kampala "
        f"(diferencia absoluta de {diferencia_promedios_tmax:.2f} °C). "
        f"El mayor promedio mensual ocurrió en "
        f"{nombres_meses_completos[mes_pico_tmax_medellin - 1]} para Medellín "
        f"({tmax_mensual.loc[mes_pico_tmax_medellin, 'Medellín']:.1f} °C) "
        f"y en {nombres_meses_completos[mes_pico_tmax_kampala - 1]} para "
        f"Kampala ({tmax_mensual.loc[mes_pico_tmax_kampala, 'Kampala']:.1f} °C). "
        f"La mayor diferencia mensual fue en "
        f"{nombres_meses_completos[mes_mayor_diferencia_tmax - 1]} "
        f"({mayor_diferencia_tmax_mensual:.1f} °C), lo que matiza la "
        "similitud de los promedios anuales.\\n\\n"
        f"- **Precipitación.** El total fue {total_precipitacion_medellin:.1f} mm "
        f"en Medellín y {total_precipitacion_kampala:.1f} mm en Kampala; "
        f"con el umbral de {UMBRAL_LLUVIA_MM:g} mm, hubo "
        f"{dias_lluviosos_medellin} y {dias_lluviosos_kampala} días lluviosos, "
        "respectivamente. El mes más lluvioso fue "
        f"{nombres_meses_completos[mes_lluvioso_medellin - 1]} en Medellín "
        f"({precipitacion_mensual.loc[mes_lluvioso_medellin, 'Medellín']:.1f} mm) "
        f"y {nombres_meses_completos[mes_lluvioso_kampala - 1]} en Kampala "
        f"({precipitacion_mensual.loc[mes_lluvioso_kampala, 'Kampala']:.1f} mm); "
        f"el mes más seco de Medellín fue "
        f"{nombres_meses_completos[mes_seco_medellin - 1]} "
        f"({total_mes_seco_medellin:.1f} mm).\\n\\n"
        f"- **Temperaturas mínimas y días de calor.** El promedio/mediana "
        f"de temperatura mínima fue {promedio_tmin_medellin:.1f}/"
        f"{mediana_tmin_medellin:.1f} °C en Medellín y "
        f"{promedio_tmin_kampala:.1f}/{mediana_tmin_kampala:.1f} °C en Kampala. "
        f"Con el umbral de calor de {UMBRAL_CALOR_C:g} °C, se contaron "
        f"{formato_conteo_dias(dias_calor_medellin)} en Medellín y "
        f"{formato_conteo_dias(dias_calor_kampala)} en Kampala.\\n\\n"
        f"- **Cobertura de datos.** Medellín tuvo "
        f"{calidad_medellin['observaciones_validas']} de "
        f"{calidad_medellin['dias_esperados']} observaciones válidas y Kampala "
        f"{calidad_kampala['observaciones_validas']} de "
        f"{calidad_kampala['dias_esperados']}; faltantes: "
        f"{calidad_medellin['faltantes']} y {calidad_kampala['faltantes']}; "
        f"fechas duplicadas: {calidad_medellin['fechas_duplicadas']} y "
        f"{calidad_kampala['fechas_duplicadas']}. "
        f"{texto_calidad}Ambas series comparten {len(fechas_compartidas)} "
        "fechas del periodo común, lo que permite comparar los mismos días.\\n\\n"
        f"- **Predicción previa.** La parte de temperaturas máximas se "
        f"confirma a escala del promedio anual, con una diferencia de "
        f"{diferencia_promedios_tmax:.2f} °C, aunque los picos y la mayor "
        f"diferencia mensual muestran estacionalidad distinta. La predicción "
        f"de que Medellín sería más lluviosa {resultado_prediccion_lluvia}.\\n\\n"
        f"El periodo común fue {PERIODO_INICIO.strftime('%d/%m/%Y')} a "
        f"{PERIODO_FIN.strftime('%d/%m/%Y')}, así que los resultados describen "
        "ese periodo y no establecen patrones de largo plazo. Los días se "
        f"agregan en hora local ({timezone_medellin} y {timezone_kampala}); "
        "sus límites no corresponden al mismo intervalo UTC. Open-Meteo "
        "provee datos de reanálisis/modelo, no mediciones de estaciones. "
        "Estos resultados describen diferencias y no permiten atribuir causalidad."
    )
)'''


repo_root = Path(__file__).resolve().parents[2]
activity_dir = repo_root / "AE3_comparacion_climatica"
notebook_path = activity_dir / NOTEBOOK_NAME
notebook = nbformat.read(notebook_path, as_version=4)

section_indexes = [
    index
    for index, cell in enumerate(notebook.cells)
    if cell.cell_type == "markdown" and cell.source.startswith(SECTION_E)
]
if len(section_indexes) != 1:
    raise ValueError("Se esperaba una sola celda con el encabezado de E.")

markdown_index = section_indexes[0]
code_index = markdown_index + 1
if code_index >= len(notebook.cells) or notebook.cells[code_index].cell_type != "code":
    raise ValueError("No se encontró la celda de código de la sección E.")

markdown_cell = notebook.cells[markdown_index]
code_cell = notebook.cells[code_index]
original_cells = {
    cell.id: deepcopy(cell)
    for cell in notebook.cells
    if cell.id not in (markdown_cell.id, code_cell.id)
}
markdown_cell.source = E_MARKDOWN
code_cell.source = E_CODE
code_cell.execution_count = None
code_cell.outputs = []

for cell_id, original_cell in original_cells.items():
    matches = [cell for cell in notebook.cells if cell.id == cell_id]
    if len(matches) != 1 or matches[0] != original_cell:
        raise RuntimeError(f"Se alteró una celda fuera de E: {cell_id}")

nbformat.validate(notebook)
nbformat.write(notebook, notebook_path)
print(f"Sección E ampliada en {notebook_path}")
