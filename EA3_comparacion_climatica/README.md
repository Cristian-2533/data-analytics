# EA3: Comparación de datos climáticos

Actividad de Analítica de Datos para comparar datos climáticos de Medellín y una ciudad de otro país.

## Estructura de carpetas

```text
AE3_comparacion_climatica/
├── AE3_Piedrahita_Cristian_y_Londoño_Santiago.ipynb
├── README.md
├── borradores/
│   ├── .gitkeep
│   ├── actualizar_seccion_c.py
│   ├── actualizar_seccion_d.py
│   ├── actualizar_seccion_e.py
│   ├── corregir_conteos_b.py
│   ├── corregir_seccion_a.py
│   ├── corregir_seccion_c.py
│   ├── corregir_seccion_d.py
│   └── corregir_seccion_e.py
└── datos/
    ├── .gitkeep
    ├── kampala.csv
    └── medellin.csv
```

## Fuentes de datos

| Ciudad | Fuente | Enlace | Periodo | Frecuencia | Fecha de descarga | Variables y unidades |
|---|---|---|---|---|---|---|
| Medellín, Colombia | Open-Meteo (reanálisis/modelo; no son datos de estaciones) | [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api) | 2025-01-01 a 2025-12-31 | Diaria, hora local `America/Bogota` | 14 de noviembre de 2026 | `temperature_2m_max` (°C), `temperature_2m_min` (°C), `precipitation_sum` (mm) |
| Kampala, Uganda | Open-Meteo (reanálisis/modelo; no son datos de estaciones) | [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api) | 2025-01-01 a 2025-12-31 | Diaria, hora local `Africa/Kampala` | 14 de noviembre de 2026 | `temperature_2m_max` (°C), `temperature_2m_min` (°C), `precipitation_sum` (mm) |

Los CSV incluyen tres líneas iniciales con metadatos y se cargan desde el notebook con `skiprows=3`.
