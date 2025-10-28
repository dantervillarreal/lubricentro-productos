import csv
import os
from typing import Dict, List

import pandas as pd
import streamlit as st

from metricas import cargar_busquedas
from productos import cargar_csv

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PRODUCTOS_FILE = os.path.join(BASE_DIR, "productos.csv")
AUTO_PRODUCTOS_FILE = os.path.join(BASE_DIR, "auto_productos.csv")

st.title("🛠️ Panel administrativo")


def leer_csv(nombre_archivo: str) -> List[Dict[str, str]]:
    ruta = os.path.join(BASE_DIR, nombre_archivo)
    if not os.path.exists(ruta):
        return []

    with open(ruta, newline="", encoding="utf-8-sig") as archivo:
        lector = csv.DictReader(archivo, delimiter=";")
        return list(lector)


def escribir_productos(datos: List[Dict[str, str]]) -> None:
    fieldnames = [
        "id_producto",
        "codigo",
        "descripcion",
        "tipo",
        "precio_unit",
        "stock",
        "precio_final",
    ]
    with open(PRODUCTOS_FILE, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=fieldnames, delimiter=";")
        escritor.writeheader()
        for fila in datos:
            escritor.writerow({campo: str(fila.get(campo, "")) for campo in fieldnames})


def proximo_id(datos: List[Dict[str, str]], campo: str) -> int:
    if not datos:
        return 1
    return max(int(item[campo]) for item in datos if item.get(campo)) + 1


def mostrar_tab_carga_productos() -> None:
    st.subheader("➕ Cargar nuevos productos")

    productos = cargar_csv("productos.csv")
    autos = leer_csv("autos.csv")

    autos_options = {
        f"{auto['marca']} {auto['modelo']} {auto['motor']} ({auto['anio']})": auto["id_auto"]
        for auto in autos
    }

    with st.form("form_nuevo_producto"):
        col1, col2 = st.columns(2)

        with col1:
            codigo = st.text_input("Código", placeholder="Ej: ACE102")
            descripcion = st.text_input("Descripción", placeholder="Ej: Aceite sintético 5W30")
            tipo = st.text_input("Tipo", placeholder="Ej: Aceite")
            stock = st.number_input("Stock", min_value=0, value=0, step=1)
        with col2:
            precio_unit = st.number_input("Precio unitario", min_value=0.0, value=0.0, step=100.0)
            precio_final = st.number_input("Precio final", min_value=0.0, value=0.0, step=100.0)
            autos_relacionados = st.multiselect(
                "Asociar a autos",
                options=list(autos_options.keys()),
                help="Seleccioná los autos compatibles con este producto",
            )

        submitted = st.form_submit_button("Guardar producto")

    if submitted:
        errores = []
        if not codigo.strip():
            errores.append("El código es obligatorio.")
        if not descripcion.strip():
            errores.append("La descripción es obligatoria.")
        if not tipo.strip():
            errores.append("El tipo es obligatorio.")
        if precio_unit <= 0:
            errores.append("El precio unitario debe ser mayor a 0.")
        if precio_final <= 0:
            errores.append("El precio final debe ser mayor a 0.")
        if any(prod["codigo"].strip().lower() == codigo.strip().lower() for prod in productos):
            errores.append("Ya existe un producto con ese código.")

        if errores:
            for err in errores:
                st.error(err)
        else:
            nuevo_id = proximo_id(productos, "id_producto")
            nuevo_producto = {
                "id_producto": str(nuevo_id),
                "codigo": codigo.strip(),
                "descripcion": descripcion.strip(),
                "tipo": tipo.strip(),
                "precio_unit": f"{precio_unit:.2f}",
                "stock": str(stock),
                "precio_final": f"{precio_final:.2f}",
            }

            encabezado_productos = [
                "id_producto",
                "codigo",
                "descripcion",
                "tipo",
                "precio_unit",
                "stock",
                "precio_final",
            ]

            with open(PRODUCTOS_FILE, "a", newline="", encoding="utf-8") as archivo:
                escritor = csv.writer(archivo, delimiter=";")
                if not productos:
                    escritor.writerow(encabezado_productos)
                escritor.writerow([nuevo_producto[campo] for campo in encabezado_productos])

            productos.append(nuevo_producto)

            if autos_relacionados:
                relaciones_existentes = leer_csv("auto_productos.csv")
                siguiente_relacion = proximo_id(relaciones_existentes, "id_auto_producto")
                asociaciones_a_registrar = []

                for opcion in autos_relacionados:
                    id_auto = autos_options.get(opcion)
                    if not id_auto:
                        continue
                    asociaciones_a_registrar.append((str(siguiente_relacion), id_auto, str(nuevo_id)))
                    siguiente_relacion += 1

                if asociaciones_a_registrar:
                    archivo_existe = os.path.exists(AUTO_PRODUCTOS_FILE)
                    with open(AUTO_PRODUCTOS_FILE, "a", newline="", encoding="utf-8") as archivo:
                        escritor = csv.writer(archivo, delimiter=";")
                        if not archivo_existe:
                            escritor.writerow(["id_auto_producto", "id_auto", "id_producto"])
                        escritor.writerows(asociaciones_a_registrar)

            st.success("Producto guardado correctamente.")

    if productos:
        st.markdown("### Productos existentes")
        st.dataframe(pd.DataFrame(productos))
    else:
        st.info("Todavía no hay productos cargados.")


def mostrar_tab_actualizar_precios() -> None:
    st.subheader("💲 Actualizar precios")

    productos = cargar_csv("productos.csv")
    if not productos:
        st.info("No hay productos para actualizar.")
        return

    opciones = {f"{prod['codigo']} – {prod['descripcion']}": prod for prod in productos}

    with st.form("form_actualizar_precios"):
        seleccion = st.selectbox("Seleccioná un producto", list(opciones.keys()))
        producto = opciones[seleccion]

        col1, col2 = st.columns(2)
        with col1:
            precio_unitario = st.number_input(
                "Precio unitario",
                min_value=0.0,
                value=float(producto["precio_unit"]),
                step=100.0,
            )
        with col2:
            precio_final = st.number_input(
                "Precio final",
                min_value=0.0,
                value=float(producto["precio_final"]),
                step=100.0,
            )

        submitted = st.form_submit_button("Actualizar")

    if submitted:
        if precio_unitario <= 0 or precio_final <= 0:
            st.error("Los precios deben ser mayores a 0.")
            return

        for prod in productos:
            if prod["id_producto"] == producto["id_producto"]:
                prod["precio_unit"] = f"{precio_unitario:.2f}"
                prod["precio_final"] = f"{precio_final:.2f}"
                break

        escribir_productos(productos)
        st.success("Precios actualizados correctamente.")


def mostrar_tab_metricas() -> None:
    st.subheader("📊 Métricas de búsquedas")

    busquedas = cargar_busquedas()
    if not busquedas:
        st.info("Todavía no hay búsquedas registradas.")
        return

    df = pd.DataFrame(busquedas)
    df["total_resultados"] = pd.to_numeric(df["total_resultados"], errors="coerce").fillna(0).astype(int)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    columnas_auto = ["marca", "modelo", "motor", "anio"]
    for columna in columnas_auto:
        if columna in df:
            df[columna] = df[columna].fillna("")
        else:
            df[columna] = ""

    total_busquedas = len(df)
    busquedas_con_resultados = int((df["total_resultados"] > 0).sum())
    promedio_resultados = df["total_resultados"].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de búsquedas", total_busquedas)
    col2.metric("Con resultados", busquedas_con_resultados)
    col3.metric("Promedio de resultados", f"{promedio_resultados:.1f}")

    st.markdown("#### Últimas búsquedas")
    st.dataframe(df.sort_values("timestamp", ascending=False).head(20))

    st.markdown("#### Tendencias")
    col1, col2 = st.columns(2)
    with col1:
        top_marcas = df["marca"].value_counts().head(5)
        if not top_marcas.empty:
            st.bar_chart(top_marcas)
    with col2:
        df["auto"] = df[columnas_auto].agg(" ".join, axis=1)
        top_autos = df["auto"].value_counts().head(5)
        if not top_autos.empty:
            st.bar_chart(top_autos)


tab_carga, tab_precios, tab_metricas = st.tabs([
    "Cargar productos",
    "Actualizar precios",
    "Métricas",
])

with tab_carga:
    mostrar_tab_carga_productos()

with tab_precios:
    mostrar_tab_actualizar_precios()

with tab_metricas:
    mostrar_tab_metricas()
