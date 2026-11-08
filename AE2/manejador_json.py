"""Manejo de archivos JSON con el módulo estándar `json`.

Misma idea que ManejadorCSV, pero con JSON:
    1. importar()   -> lee el archivo con json.load
    2. modificar    -> actualizar_valor / agregar_registro / eliminar_registro
    3. guardar()    -> escribe un JSON NUEVO con json.dump
    4. resumen()    -> entrega los datos que necesita la clase del resumen .txt

Un JSON de datos suele ser una LISTA de registros, y cada registro es un
diccionario (clave: valor). Por ejemplo:
    [ {"nombre": "Ana", "edad": 30}, {"nombre": "Luis", "edad": 25} ]
A veces la lista viene dentro de un diccionario, por ejemplo {"data": [ ... ]};
esta clase también lo detecta.

Si un registro tiene datos anidados (un diccionario dentro de otro), se llega a
ellos con una ruta separada por puntos, por ejemplo "problem.context".

El archivo original nunca se toca: siempre se guarda con otro nombre.
"""

import json
import copy


def _corto(texto, ancho=60):
    """Acorta un texto largo para mostrarlo o registrarlo (sin saltos de línea)."""
    texto = str(texto).replace("\n", " ")
    return texto if len(texto) <= ancho else texto[: ancho - 3] + "..."


def _acortar_textos(objeto, ancho):
    """Devuelve una copia del objeto con los textos largos acortados (solo para mostrar)."""
    if isinstance(objeto, dict):
        return {clave: _acortar_textos(valor, ancho) for clave, valor in objeto.items()}
    if isinstance(objeto, list):
        return [_acortar_textos(valor, ancho) for valor in objeto]
    if isinstance(objeto, str):
        return _corto(objeto, ancho)
    return objeto


class ManejadorJSON:
    def __init__(self, ruta_origen, url_origen):
        self.ruta_origen = ruta_origen     # ruta relativa del archivo descargado
        self.url_origen = url_origen       # URL exacta de Hugging Face

        self.contenido = None              # lo que devuelve json.load (todo el archivo)
        self.clave_lista = None            # si la lista de registros está dentro de un dict
        self.registros = []                # la lista de registros (diccionarios)
        self.contenido_original = None     # copia para mostrar el "antes"
        self.modificaciones = []           # registro de lo que se hizo, para el resumen
        self.ruta_guardado = None
        self._metodos_usados = []          # métodos que realmente se llamaron

    def _usar(self, nombre_metodo):
        """Anota que un método se ejecutó (así el resumen refleja lo que pasó de verdad)."""
        if nombre_metodo not in self._metodos_usados:
            self._metodos_usados.append(nombre_metodo)

    @staticmethod
    def _navegar(registro, ruta):
        """Devuelve (diccionario_que_contiene_la_clave, ultima_clave) para una ruta con puntos."""
        partes = ruta.split(".")
        destino = registro
        for parte in partes[:-1]:
            destino = destino[parte]
        return destino, partes[-1]

    # ------------------------------------------------------------------ 1. IMPORTAR
    def importar(self):
        """Lee el JSON y localiza la lista de registros."""
        self._usar("importar")
        with open(self.ruta_origen, mode="r", encoding="utf-8") as archivo:
            self.contenido = json.load(archivo)

        if isinstance(self.contenido, list):
            self.registros = self.contenido
        elif isinstance(self.contenido, dict):
            # Buscamos dentro del diccionario la primera clave cuyo valor sea una lista
            for clave, valor in self.contenido.items():
                if isinstance(valor, list):
                    self.clave_lista = clave
                    self.registros = valor
                    break
            else:
                raise ValueError("El JSON es un diccionario pero no contiene una lista de registros.")
        else:
            raise ValueError("El JSON no tiene un formato de registros reconocible.")

        self.contenido_original = copy.deepcopy(self.contenido)
        return self.registros

    # ------------------------------------------------------------------ MOSTRAR
    def mostrar(self, cantidad=3, original=False, ancho=60):
        """Imprime los primeros registros con formato legible. Los textos largos se acortan solo al mostrar."""
        self._usar("mostrar")
        if original:
            if self.clave_lista:
                datos = self.contenido_original[self.clave_lista]
            else:
                datos = self.contenido_original
        else:
            datos = self.registros
        for registro in datos[:cantidad]:
            print(json.dumps(_acortar_textos(registro, ancho), indent=2, ensure_ascii=False))
        print(f"... total: {len(datos)} registros")

    # ------------------------------------------------------------------ BUSCAR
    def buscar_indice(self, clave, valor):
        """Devuelve la posición del primer registro cuya `clave` (admite ruta con puntos) vale `valor`."""
        self._usar("buscar_indice")
        for posicion, registro in enumerate(self.registros):
            contenedor, ultima = self._navegar(registro, clave)
            if contenedor.get(ultima) == valor:
                return posicion
        raise ValueError(f"No se encontró '{valor}' en la clave '{clave}'.")

    # ------------------------------------------------------------------ 2. MODIFICAR
    def actualizar_valor(self, indice, clave, nuevo_valor):
        """Cambia un valor: en el registro `indice`, la clave (admite ruta con puntos) pasa a `nuevo_valor`."""
        self._usar("actualizar_valor")
        contenedor, ultima = self._navegar(self.registros[indice], clave)
        valor_anterior = contenedor.get(ultima)
        contenedor[ultima] = nuevo_valor
        self.modificaciones.append(
            f"Actualizar valor: registro {indice}, clave '{clave}': "
            f"'{_corto(valor_anterior)}' -> '{_corto(nuevo_valor)}'"
        )

    def agregar_registro(self, registro):
        """Agrega un registro (un diccionario) al final de la lista."""
        self._usar("agregar_registro")
        if not isinstance(registro, dict):
            raise ValueError("El registro debe ser un diccionario.")
        self.registros.append(registro)
        self.modificaciones.append(
            f"Agregar registro al final (posición {len(self.registros) - 1}): "
            f"{_corto(json.dumps(registro, ensure_ascii=False), 80)}"
        )

    def eliminar_registro(self, indice):
        """Elimina el registro que está en la posición `indice`."""
        self._usar("eliminar_registro")
        eliminado = self.registros.pop(indice)
        self.modificaciones.append(
            f"Eliminar registro de la posición {indice}: "
            f"{_corto(json.dumps(eliminado, ensure_ascii=False), 80)}"
        )
        return eliminado

    # ------------------------------------------------------------------ 3. GUARDAR
    def guardar(self, ruta_salida):
        """Escribe un JSON nuevo con json.dump, conservando el archivo original."""
        self._usar("guardar")
        if ruta_salida == self.ruta_origen:
            raise ValueError("No se puede sobrescribir el archivo original.")

        with open(ruta_salida, mode="w", encoding="utf-8") as archivo:
            # indent=2 lo deja legible; ensure_ascii=False conserva tildes, ñ y caracteres chinos
            json.dump(self.contenido, archivo, indent=2, ensure_ascii=False)

        self.ruta_guardado = ruta_salida
        return ruta_salida

    # ------------------------------------------------------------------ 4. RESUMEN
    def resumen(self):
        """Devuelve un diccionario con los resultados reales, para la tercera clase."""
        self._usar("resumen")
        if self.clave_lista:
            cantidad_original = len(self.contenido_original[self.clave_lista])
        else:
            cantidad_original = len(self.contenido_original)
        return {
            "formato": "JSON",
            "url_origen": self.url_origen,
            "archivo_importado": self.ruta_origen,
            "archivo_guardado": self.ruta_guardado,
            "registros_originales": cantidad_original,
            "registros_finales": len(self.registros),
            "columnas": sorted({clave for r in self.registros for clave in r}),
            "modificaciones": self.modificaciones,
            "clase": self.__class__.__name__,
            "metodos_usados": list(self._metodos_usados),
        }
