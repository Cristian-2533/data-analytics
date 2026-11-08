"""Manejo de archivos CSV con el módulo estándar `csv`.

Esta clase hace cuatro cosas, en este orden:
    1. importar()          -> lee el CSV con csv.reader
    2. modificar           -> actualizar_valor / agregar_registro / eliminar_registro
    3. guardar()           -> escribe un CSV NUEVO con csv.writer (incluye encabezados)
    4. resumen()           -> entrega los datos que necesita la clase del resumen .txt

Importante: el archivo original nunca se toca. Siempre se guarda con otro nombre.
"""

import csv
import copy


def _corto(texto, ancho=60):
    """Acorta un texto largo para mostrarlo o registrarlo (sin saltos de línea)."""
    texto = str(texto).replace("\n", " ")
    return texto if len(texto) <= ancho else texto[: ancho - 3] + "..."


class ManejadorCSV:
    def __init__(self, ruta_origen, url_origen):
        # Ruta relativa del archivo descargado, por ejemplo "datos/mi_archivo.csv"
        self.ruta_origen = ruta_origen
        # URL exacta de Hugging Face de donde se descargó (la pide el resumen)
        self.url_origen = url_origen

        self.encabezados = []          # nombres de las columnas
        self.filas = []                # lista de filas; cada fila es una lista de textos
        self.filas_originales = []     # copia para poder mostrar el "antes"
        self.modificaciones = []       # registro de lo que se hizo, para el resumen
        self.ruta_guardado = None
        self._metodos_usados = []      # métodos que realmente se llamaron

    def _usar(self, nombre_metodo):
        """Anota que un método se ejecutó (así el resumen refleja lo que pasó de verdad)."""
        if nombre_metodo not in self._metodos_usados:
            self._metodos_usados.append(nombre_metodo)

    # ------------------------------------------------------------------ 1. IMPORTAR
    def importar(self):
        """Lee el CSV. La primera fila son los encabezados; el resto son los registros."""
        self._usar("importar")
        # Algunos CSV tienen celdas con textos muy largos: subimos el límite de csv.
        csv.field_size_limit(10_000_000)

        # newline="" es lo que recomienda Python para leer y escribir CSV
        with open(self.ruta_origen, mode="r", newline="", encoding="utf-8") as archivo:
            lector = csv.reader(archivo)
            self.encabezados = next(lector)
            self.filas = [fila for fila in lector]

        self.filas_originales = copy.deepcopy(self.filas)
        return self.filas

    # ------------------------------------------------------------------ MOSTRAR
    def mostrar(self, cantidad=5, original=False, columnas=None, ancho=40):
        """Imprime las primeras filas. Las celdas largas se acortan solo al mostrarlas.

        columnas: lista con los nombres de las columnas a mostrar (por defecto, todas).
        """
        self._usar("mostrar")
        datos = self.filas_originales if original else self.filas
        nombres = columnas if columnas else self.encabezados
        posiciones = [self.encabezados.index(nombre) for nombre in nombres]

        print(" | ".join(nombres))
        for fila in datos[:cantidad]:
            print(" | ".join(_corto(fila[p], ancho) for p in posiciones))
        print(f"... total: {len(datos)} registros")

    # ------------------------------------------------------------------ BUSCAR
    def buscar_indice(self, nombre_columna, valor):
        """Devuelve la posición de la primera fila cuyo valor en esa columna es exactamente `valor`."""
        self._usar("buscar_indice")
        columna = self.encabezados.index(nombre_columna)
        for posicion, fila in enumerate(self.filas):
            if fila[columna] == valor:
                return posicion
        raise ValueError(f"No se encontró '{valor}' en la columna '{nombre_columna}'.")

    # ------------------------------------------------------------------ 2. MODIFICAR
    def actualizar_valor(self, indice_fila, nombre_columna, nuevo_valor):
        """Cambia UN valor: la celda de la fila `indice_fila` en la columna indicada."""
        self._usar("actualizar_valor")
        columna = self.encabezados.index(nombre_columna)
        valor_anterior = self.filas[indice_fila][columna]
        self.filas[indice_fila][columna] = str(nuevo_valor)
        self.modificaciones.append(
            f"Actualizar valor: fila {indice_fila}, columna '{nombre_columna}': "
            f"'{_corto(valor_anterior)}' -> '{_corto(nuevo_valor)}'"
        )

    def agregar_registro(self, registro):
        """Agrega una fila al final. `registro` es una lista en el orden de las columnas."""
        self._usar("agregar_registro")
        if len(registro) != len(self.encabezados):
            raise ValueError(
                f"El registro tiene {len(registro)} valores y el archivo tiene "
                f"{len(self.encabezados)} columnas."
            )
        self.filas.append([str(valor) for valor in registro])
        self.modificaciones.append(
            f"Agregar registro al final (posición {len(self.filas) - 1}): "
            f"{[_corto(valor, 30) for valor in registro]}"
        )

    def eliminar_registro(self, indice_fila):
        """Elimina la fila que está en la posición `indice_fila`."""
        self._usar("eliminar_registro")
        eliminado = self.filas.pop(indice_fila)
        self.modificaciones.append(
            f"Eliminar registro de la posición {indice_fila}: "
            f"{[_corto(valor, 30) for valor in eliminado[:2]]} ..."
        )
        return eliminado

    # ------------------------------------------------------------------ 3. GUARDAR
    def guardar(self, ruta_salida):
        """Escribe un CSV nuevo con los encabezados y las filas ya modificadas."""
        self._usar("guardar")
        if ruta_salida == self.ruta_origen:
            raise ValueError("No se puede sobrescribir el archivo original.")

        with open(ruta_salida, mode="w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(self.encabezados)   # primero los encabezados
            escritor.writerows(self.filas)        # luego todos los registros

        self.ruta_guardado = ruta_salida
        return ruta_salida

    # ------------------------------------------------------------------ 4. RESUMEN
    def resumen(self):
        """Devuelve un diccionario con los resultados reales, para la tercera clase."""
        self._usar("resumen")
        return {
            "formato": "CSV",
            "url_origen": self.url_origen,
            "archivo_importado": self.ruta_origen,
            "archivo_guardado": self.ruta_guardado,
            "registros_originales": len(self.filas_originales),
            "registros_finales": len(self.filas),
            "columnas": self.encabezados,
            "modificaciones": self.modificaciones,
            "clase": self.__class__.__name__,
            "metodos_usados": list(self._metodos_usados),
        }
