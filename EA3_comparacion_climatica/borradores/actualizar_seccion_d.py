from copy import deepcopy
from pathlib import Path

import nbformat


NOTEBOOK_NAME = "AE3_Piedrahita_Cristian_y_Londoño_Santiago.ipynb"
SECTION_A = "## A. Predicción, periodo común y variables"
SECTION_B = "## B. Carga y revisión de los datos"
SECTION_C = "## C. Análisis con NumPy"
SECTION_D = "## D. Gráficas comparativas"

D_MARKDOWN = """## D. Gráficas comparativas

Las tres gráficas comparan los mismos días del periodo común. Después de cada figura, el código genera una breve lectura basada en los valores calculados y señala qué no permite concluir."""

D_CODE = '''from IPython.display import Markdown

nombres_meses = [
    "Ene", "Feb", "Mar", "Abr", "May", "Jun",
    "Jul", "Ago", "Sep", "Oct", "Nov", "Dic",
]
meses = np.arange(1, 13)
resumenes_mensuales = {}

for ciudad, df in datos.items():
    periodo_grafica = df.loc[
        df["time"].between(PERIODO_INICIO, PERIODO_FIN)
    ].copy()
    periodo_grafica["mes"] = periodo_grafica["time"].dt.month
    resumenes_mensuales[ciudad] = periodo_grafica.groupby("mes")

tmax_mensual = pd.DataFrame(
    {
        ciudad: grupos["temperature_2m_max (°C)"].mean()
        for ciudad, grupos in resumenes_mensuales.items()
    }
).reindex(meses)

fig, ax = plt.subplots(figsize=(10, 5))
for ciudad in datos:
    ax.plot(meses, tmax_mensual[ciudad], marker="o", label=ciudad)
ax.set_title("Temperatura máxima mensual promedio")
ax.set_xlabel("Mes")
ax.set_ylabel("Temperatura máxima promedio (°C)")
ax.set_xticks(meses, nombres_meses)
ax.legend(title="Ciudad")
ax.grid(True, alpha=0.3)
fig.tight_layout()
plt.show()

mes_pico_medellin = int(tmax_mensual["Medellín"].idxmax())
mes_pico_kampala = int(tmax_mensual["Kampala"].idxmax())
display(
    Markdown(
        f"El promedio mensual de temperatura máxima alcanzó su valor mayor "
        f"en {nombres_meses[mes_pico_medellin - 1]} para Medellín "
        f"({tmax_mensual.loc[mes_pico_medellin, 'Medellín']} °C) y en "
        f"{nombres_meses[mes_pico_kampala - 1]} para Kampala "
        f"({tmax_mensual.loc[mes_pico_kampala, 'Kampala']} °C). "
        "La línea describe promedios mensuales y no permite inferir causas "
        "de las diferencias observadas."
    )
)

precipitacion_mensual = pd.DataFrame(
    {
        ciudad: grupos["precipitation_sum (mm)"].sum()
        for ciudad, grupos in resumenes_mensuales.items()
    }
).reindex(meses)

ancho = 0.38
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(meses - ancho / 2, precipitacion_mensual["Medellín"], ancho, label="Medellín")
ax.bar(meses + ancho / 2, precipitacion_mensual["Kampala"], ancho, label="Kampala")
ax.set_title("Precipitación acumulada por mes")
ax.set_xlabel("Mes")
ax.set_ylabel("Precipitación acumulada (mm)")
ax.set_xticks(meses, nombres_meses)
ax.legend(title="Ciudad")
fig.tight_layout()
plt.show()

mes_lluvioso_medellin = int(precipitacion_mensual["Medellín"].idxmax())
mes_lluvioso_kampala = int(precipitacion_mensual["Kampala"].idxmax())
display(
    Markdown(
        f"El mayor acumulado mensual se registró en "
        f"{nombres_meses[mes_lluvioso_medellin - 1]} para Medellín "
        f"({precipitacion_mensual.loc[mes_lluvioso_medellin, 'Medellín']} mm) "
        f"y en {nombres_meses[mes_lluvioso_kampala - 1]} para Kampala "
        f"({precipitacion_mensual.loc[mes_lluvioso_kampala, 'Kampala']} mm). "
        "Los acumulados mensuales no muestran la distribución de la lluvia "
        "dentro de cada mes ni establecen causalidad."
    )
)

temperaturas_minimas = {
    ciudad: arrays[ciudad]["temperature_2m_min (°C)"] for ciudad in datos
}
limites_bins = np.histogram_bin_edges(
    np.concatenate(list(temperaturas_minimas.values())),
    bins="auto",
)
fig, ax = plt.subplots(figsize=(10, 5))
for ciudad, valores in temperaturas_minimas.items():
    ax.hist(valores, bins=limites_bins, alpha=0.55, label=ciudad)
ax.set_title("Distribución de temperaturas mínimas diarias")
ax.set_xlabel("Temperatura mínima diaria (°C)")
ax.set_ylabel("Frecuencia (días)")
ax.legend(title="Ciudad")
fig.tight_layout()
plt.show()

mediana_tmin_medellin = np.median(temperaturas_minimas["Medellín"])
mediana_tmin_kampala = np.median(temperaturas_minimas["Kampala"])
display(
    Markdown(
        f"Las medianas de temperatura mínima diaria fueron "
        f"{mediana_tmin_medellin} °C en Medellín y "
        f"{mediana_tmin_kampala} °C en Kampala; el histograma permite "
        "comparar sus frecuencias. La figura no conserva el orden de las "
        "fechas ni explica las causas de las diferencias."
    )
)'''


activity_dir = Path(__file__).resolve().parents[1]
notebook_path = activity_dir / NOTEBOOK_NAME
notebook = nbformat.read(notebook_path, as_version=4)

section_indexes = {}
for heading in (SECTION_A, SECTION_B, SECTION_C, SECTION_D):
    matches = [
        index
        for index, cell in enumerate(notebook.cells)
        if cell.cell_type == "markdown" and cell.source.startswith(heading)
    ]
    if len(matches) != 1:
        raise ValueError(f"Se esperaba una sola celda con el encabezado: {heading}")
    section_indexes[heading] = matches[0]

section_d_index = section_indexes[SECTION_D]
if not (
    section_indexes[SECTION_A]
    < section_indexes[SECTION_B]
    < section_indexes[SECTION_C]
    < section_d_index
):
    raise ValueError("El orden de las secciones A, B, C y D no es el esperado.")

protected_cells = deepcopy(notebook.cells[:section_d_index])
notebook.cells[section_d_index].source = D_MARKDOWN
notebook.cells.insert(
    section_d_index + 1,
    nbformat.v4.new_code_cell(source=D_CODE),
)

if notebook.cells[:section_d_index] != protected_cells:
    raise RuntimeError("La modificación alteró celdas anteriores a la sección D.")

nbformat.validate(notebook)
nbformat.write(notebook, notebook_path)
print(f"Sección D escrita en {notebook_path}")
