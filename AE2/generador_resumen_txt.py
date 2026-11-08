"""Generación del resumen.txt a partir de los resultados reales de las otras clases.

Esta clase NO conoce los datos: solo recibe los diccionarios que devuelve el
método resumen() de ManejadorCSV y ManejadorJSON, y los escribe en un archivo .txt.
Así el texto sale del código y de lo que realmente pasó, no de lo que escribimos a mano.
"""

from datetime import datetime


class GeneradorResumenTXT:
    def __init__(self, resultados):
        # `resultados` es una lista con un diccionario por formato (CSV, JSON)
        self.resultados = resultados
        self.contenido = ""

    def construir(self):
        """Arma el texto del resumen y lo deja en self.contenido."""
        lineas = []
        lineas.append("RESUMEN DE LA EJECUCIÓN - AE2: Manejo de archivos CSV y JSON")
        lineas.append(f"Generado el: {datetime.now():%Y-%m-%d %H:%M:%S}")
        lineas.append("=" * 60)

        for r in self.resultados:
            lineas.append("")
            lineas.append(f"FORMATO: {r['formato']}")
            lineas.append("-" * 60)
            lineas.append(f"URL de origen:        {r['url_origen']}")
            lineas.append(f"Archivo importado:    {r['archivo_importado']}")
            lineas.append(f"Archivo guardado:     {r['archivo_guardado']}")
            lineas.append(f"Clase utilizada:      {r['clase']}")
            lineas.append(f"Métodos utilizados:   {', '.join(r['metodos_usados'])}")
            lineas.append(f"Registros originales: {r['registros_originales']}")
            lineas.append(f"Registros finales:    {r['registros_finales']}")
            lineas.append(f"Columnas/claves:      {', '.join(r['columnas'])}")
            lineas.append("Modificaciones realizadas:")
            if r["modificaciones"]:
                for numero, texto in enumerate(r["modificaciones"], start=1):
                    lineas.append(f"  {numero}. {texto}")
            else:
                lineas.append("  (ninguna)")

        total_original = sum(r["registros_originales"] for r in self.resultados)
        total_final = sum(r["registros_finales"] for r in self.resultados)
        lineas.append("")
        lineas.append("=" * 60)
        lineas.append(f"Registros procesados (originales, ambos formatos): {total_original}")
        lineas.append(f"Registros resultantes (finales, ambos formatos):   {total_final}")
        lineas.append("")
        lineas.append("Este resumen fue generado por código con la clase "
                      f"{self.__class__.__name__} (método construir).")

        self.contenido = "\n".join(lineas) + "\n"
        return self.contenido

    def guardar(self, ruta_salida="resumen.txt"):
        """Escribe el resumen en un archivo .txt."""
        if not self.contenido:
            self.construir()
        with open(ruta_salida, mode="w", encoding="utf-8") as archivo:
            archivo.write(self.contenido)
        return ruta_salida

    def mostrar(self):
        """Imprime el contenido del resumen (para verlo en el notebook)."""
        if not self.contenido:
            self.construir()
        print(self.contenido)
