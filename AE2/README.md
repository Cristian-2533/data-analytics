# AE2 – Manejo de archivos CSV, JSON y TXT

Analítica de Datos – Unidad 1 – Evidencia de Aprendizaje 2.

Este proyecto importa, modifica y guarda un archivo **CSV** y un archivo **JSON** usando solo los módulos estándar de Python (`csv` y `json`), y genera un `resumen.txt` con código.

## Datos usados (descargados manualmente de Hugging Face)

| Formato | Archivo | Dataset | URL de origen | Licencia |
|---|---|---|---|---|
| CSV | `datos/crispr_delivery.csv` (20 registros, 14 columnas) | `deep-principle/science_biology` | https://huggingface.co/datasets/deep-principle/science_biology/blob/main/crispr_delivery.csv | MIT |
| JSON | `datos/questions.json` (80 registros, anidado) | `KeepaceAI/MoveBench` | https://huggingface.co/datasets/KeepaceAI/MoveBench/blob/main/questions.json | CC-BY-4.0 |

Los archivos originales **no se modifican**. Las versiones modificadas se guardan aparte.

## Estructura de la carpeta

```
AE2/
├── manejador_csv.py             # Clase ManejadorCSV
├── manejador_json.py            # Clase ManejadorJSON
├── generador_resumen_txt.py     # Clase GeneradorResumenTXT
├── AE2.ipynb                    # Notebook ejecutado que usa las tres clases
├── resumen.txt                  # Generado por código al ejecutar el notebook
├── README.md
└── datos/
    ├── crispr_delivery.csv              # CSV original
    ├── crispr_delivery_modificado.csv   # CSV modificado
    ├── questions.json                   # JSON original
    └── questions_modificado.json        # JSON modificado
```

## Cómo ejecutar

1. Tener Python 3.9 o superior y Jupyter:
   ```
   pip install notebook
   ```
2. Abrir una terminal dentro de la carpeta `AE2` (los archivos `.py`, el notebook y `datos/` deben estar juntos).
3. Abrir el notebook:
   ```
   jupyter notebook AE2.ipynb
   ```
4. Ejecutar todas las celdas en orden (*Kernel → Restart & Run All*).
5. Al terminar se crean/actualizan `datos/crispr_delivery_modificado.csv`, `datos/questions_modificado.json` y `resumen.txt`.

## Qué hace cada clase

- **`ManejadorCSV`**: `importar()` (csv.reader), `mostrar()`, `buscar_indice()`, `actualizar_valor()`, `agregar_registro()`, `eliminar_registro()`, `guardar()` (csv.writer) y `resumen()`.
- **`ManejadorJSON`**: los mismos métodos, con `json.load` / `json.dump`; permite rutas con puntos para datos anidados (por ejemplo `problem.context`).
- **`GeneradorResumenTXT`**: recibe lo que devuelve `resumen()` de las dos clases anteriores y escribe `resumen.txt` (URL de origen, archivos, métodos usados, registros antes/después y modificaciones).

## Modificaciones realizadas

**CSV:** se corrigieron 3 valores de `USER_MESSAGE` (dos errores de escritura y un espacio sobrante), se agregó 1 registro nuevo y se eliminó 1 registro casi duplicado (20 → 20 registros).

**JSON:** se actualizó `problem.context` del primer registro, se agregó 1 registro nuevo y se eliminó el registro `DA_OQ336` (80 → 80 registros).

## Autoría

Actividad desarrollada por el estudiante responsable de AE2 como parte del trabajo en equipo.
