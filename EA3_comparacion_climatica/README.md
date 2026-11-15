# EA3 · Comparación de datos climáticos: Medellín y Kampala

Actividad S30 (Unidad 2, Evidencia de Aprendizaje 3) de Analítica de Datos. Se comparan, con NumPy y gráficas de Matplotlib, las temperaturas y la precipitación diarias de **Medellín (Colombia)** y **Kampala (Uganda)** durante todo el año 2025.

**Integrantes:** Cristian Piedrahita y Santiago Londoño.

## Pregunta guía

> ¿Qué similitudes y diferencias se observan en las variables climáticas de Medellín y la otra ciudad durante el mismo periodo?

## Resumen de resultados

Ambas ciudades tienen un promedio anual de temperatura máxima casi igual, pero se diferencian en la lluvia, en la temperatura mínima y en la forma en que cambia la temperatura máxima mes a mes. Todos los valores salen del notebook y se calculan con las 365 observaciones diarias de cada ciudad (sin datos faltantes ni fechas duplicadas).

| Indicador (2025) | Medellín | Kampala |
|---|---:|---:|
| Temperatura máxima: promedio (°C) | 27.0 | 26.8 |
| Temperatura máxima: mínima / mayor (°C) | 21.7 / 30.0 | 21.4 / 35.2 |
| Temperatura mínima: promedio (°C) | 16.5 | 17.9 |
| Temperatura mínima: mediana (°C) | 16.6 | 17.9 |
| Precipitación total (mm) | 2193.9 | 1207.9 |
| Días lluviosos (precipitación ≥ 1 mm) | 267 | 217 |
| Días calurosos (temperatura máxima ≥ 30 °C) | 1 | 18 |

Hallazgos principales:

1. **Similitud:** el promedio anual de temperatura máxima difiere solo 0.12 °C entre las dos ciudades. Sin embargo, mes a mes no son iguales: Medellín tuvo su mayor promedio mensual en julio (28.3 °C) y Kampala en febrero (29.2 °C), con una diferencia mensual máxima de 3.3 °C en febrero.
2. **Diferencia:** Medellín acumuló más lluvia (2193.9 mm frente a 1207.9 mm) y tuvo más días lluviosos (267 frente a 217). Ambas ciudades tuvieron su mes más lluvioso en abril (316.7 mm en Medellín y 185.3 mm en Kampala). En el resto de los meses Medellín superó a Kampala, salvo en julio, su mes más seco (62.9 mm).
3. **Temperaturas mínimas y días calurosos:** Kampala tuvo mínimas más altas (promedio 17.9 °C frente a 16.5 °C) y muchos más días con máxima de 30 °C o más (18 frente a 1).

Estos resultados describen únicamente el año 2025 y no se interpretan como causas (ver [Limitaciones](#limitaciones)).

## Datos

| Ciudad | Fuente | Enlace | Periodo | Frecuencia | Fecha de descarga |
|---|---|---|---|---|---|
| Medellín, Colombia (6.22° N, 75.55° O, 1476 m) | Open-Meteo, Historical Weather API | <https://open-meteo.com/en/docs/historical-weather-api> | 2025-01-01 a 2025-12-31 | Diaria, hora local `America/Bogota` | 14 de noviembre de 2026 |
| Kampala, Uganda (0.39° N, 32.58° E, 1174 m) | Open-Meteo, Historical Weather API | <https://open-meteo.com/en/docs/historical-weather-api> | 2025-01-01 a 2025-12-31 | Diaria, hora local `Africa/Kampala` | 14 de noviembre de 2026 |

**Variables usadas (las mismas en ambas tablas):**

| Columna en el CSV | Significado | Unidad |
|---|---|---|
| `time` | Fecha del día (hora local de cada ciudad) | AAAA-MM-DD |
| `temperature_2m_max (°C)` | Temperatura máxima diaria a 2 m | °C |
| `temperature_2m_min (°C)` | Temperatura mínima diaria a 2 m | °C |
| `precipitation_sum (mm)` | Precipitación acumulada del día | mm |

Los CSV conservan el formato original de Open-Meteo: las tres primeras líneas son metadatos (latitud, longitud, elevación y zona horaria) y la tabla empieza en la cuarta, por lo que se leen con `pd.read_csv(..., skiprows=3)`. Ambos archivos pesan menos de 10 KB, así que se guardan en el repositorio y no hace falta descargarlos de nuevo.

**Por qué estas dos tablas son comparables:** vienen de la misma fuente y del mismo servicio, tienen las mismas variables y unidades, cubren exactamente el mismo rango de fechas (01/01/2025 a 31/12/2025), usan la misma frecuencia diaria y ninguna tiene valores faltantes.

## Estructura de la carpeta

```text
EA3_comparacion_climatica/
├── EA3_Piedrahita_Cristian_y_Londoño_Santiago.ipynb   # notebook ejecutado, con salidas y gráficas
├── README.md                                          # este documento
├── datos/
│   ├── medellin.csv                                   # Open-Meteo, Medellín, 2025
│   └── kampala.csv                                    # Open-Meteo, Kampala, 2025
└── borradores/                                        # scripts auxiliares usados para editar el notebook
```

La carpeta `borradores/` guarda solo el registro del proceso de edición del notebook; no se necesita para ejecutarlo.

## Contenido del notebook

El notebook está organizado en las secciones que pide la actividad, y cada etapa se explica en celdas Markdown:

| Sección | Qué contiene |
|---|---|
| **A. Planteamiento** | Predicción escrita antes de calcular, periodo común, variables, coordenadas, zonas horarias y fuente. |
| **B. Carga y revisión** | Lectura de los CSV, columnas, primeras filas, dimensiones, fechas inicial y final, faltantes, duplicados, conversión de tipos (`datetime64[ns]` y `float`) y conteo de observaciones válidas. |
| **C. Análisis con NumPy** | Arrays por variable y ciudad, corte de los primeros siete días, máscaras booleanas (días lluviosos y días calurosos con los mismos umbrales para ambas ciudades), estadísticas descriptivas y un ejemplo de *broadcasting* (matriz ciudad × mes menos el vector de promedios mensuales). |
| **D. Gráficas** | Tres figuras con título, ejes, unidades y leyenda: líneas de temperatura máxima mensual promedio, barras agrupadas de precipitación acumulada por mes e histograma de temperaturas mínimas diarias. Cada una va seguida de una lectura del patrón y de lo que no permite concluir. |
| **E. Interpretación** | Hallazgos con valores concretos, relación con la predicción inicial, efecto del periodo común y de los datos faltantes, y limitaciones. |

## Decisiones metodológicas

- **Periodo común:** del 1 de enero al 31 de diciembre de 2025, sin recortar ni ajustar las fechas de ninguna ciudad.
- **Día lluvioso:** precipitación diaria ≥ 1 mm (variable `UMBRAL_LLUVIA_MM`).
- **Día caluroso:** temperatura máxima ≥ 30 °C (variable `UMBRAL_CALOR_C`). Se aplica el mismo umbral a las dos ciudades. Con este umbral Medellín casi no tiene días calurosos, y ese contraste es parte del resultado.
- **Datos faltantes:** no se reemplazan por cero ni se eliminan filas. En estas tablas no hubo faltantes.
- **Agregaciones:** los promedios mensuales y los acumulados de lluvia se calculan por mes calendario de 2025.
- **Texto generado desde el código:** los números que aparecen en las interpretaciones salen de variables calculadas en el notebook, para que el texto coincida con las salidas.

## Limitaciones

- **Un solo año.** Los resultados describen 2025 y no establecen patrones de largo plazo.
- **Datos modelados.** Open-Meteo entrega datos de reanálisis/modelo, no mediciones de estaciones meteorológicas, por lo que las diferencias entre ciudades dependen también de la resolución del modelo.
- **Zonas horarias distintas.** Cada día se agrega en la hora local de su ciudad (`America/Bogota` y `Africa/Kampala`), de modo que los límites de cada día no corresponden al mismo intervalo en UTC.
- **Sin causalidad.** Se describen diferencias y similitudes observadas; el análisis no permite atribuirlas a causas concretas.

## Cómo reproducirlo

Requiere Python 3 (el notebook se ejecutó con Python 3.11). Desde la raíz del repositorio, en PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install numpy pandas matplotlib notebook
jupyter notebook EA3_comparacion_climatica
```

Después abre `EA3_Piedrahita_Cristian_y_Londoño_Santiago.ipynb` y usa **Kernel → Restart & Run All**. Las rutas de los datos son relativas (`datos/medellin.csv` y `datos/kampala.csv`), así que el notebook debe abrirse desde su propia carpeta, como hace Jupyter por defecto.

El `requirements.txt` de la raíz del repositorio fija las versiones usadas en el curso. Para esta actividad solo se necesitan `numpy`, `pandas`, `matplotlib` y `notebook`.

## Referencias

- Zippenfennig, P. (2023). *Open-Meteo.com Weather API* [Software]. Zenodo. <https://doi.org/10.5281/zenodo.7970649>
- Hersbach, H., Bell, B., Berrisford, P., et al. (2020). The ERA5 global reanalysis. *Quarterly Journal of the Royal Meteorological Society, 146*(730), 1999–2049. <https://doi.org/10.1002/qj.3803>
- Open-Meteo. (s. f.). *Historical Weather API*. Recuperado el 14 de noviembre de 2026, de <https://open-meteo.com/en/docs/historical-weather-api>
