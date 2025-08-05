import streamlit as st
from productos import obtener_productos
from presupuesto import generar_presupuesto_pdf


st.set_page_config(page_title="Buscador de productos", layout="wide")
st.title("🔧 Buscador de productos por auto")

seleccionados = []
total = 0.0

# Inicializar estado si no existe
if "resultados" not in st.session_state:
    st.session_state.resultados = []

# Formulario para buscar auto
with st.form("formulario_auto"):
    col1, col2 = st.columns(2)
    with col1:
        marca = st.text_input("Marca", placeholder="Ej: Toyota")
        modelo = st.text_input("Modelo", placeholder="Ej: Corolla")
    with col2:
        motor = st.text_input("Motor", placeholder="Ej: 1.8")
        anio = st.text_input("Año", placeholder="Ej: 2015")
    buscar = st.form_submit_button("🔍 Buscar productos")

# Si se hace submit, guardar los resultados en session_state
if buscar:
    if not (marca and modelo and motor and anio):
        st.warning("⚠️ Completá todos los campos.")
    else:
        resultados = obtener_productos(marca, modelo, motor, anio)
        st.session_state.resultados = resultados

# Mostrar resultados si existen
if st.session_state.resultados:
    resultados = st.session_state.resultados

    if isinstance(resultados, list) and isinstance(resultados[0], dict):
        st.success(f"✅ Se encontraron {len(resultados)} productos.")
        # seleccionados = []
        # total = 0

        st.markdown("### Seleccioná productos para el presupuesto:")

        for i, prod in enumerate(resultados):
            col1, col2 = st.columns([0.05, 0.95])
            with col1:
                check = st.checkbox("", key=f"check_{i}")
            with col2:
                st.markdown(
                    f"**{prod['descripcion']}** – {prod['tipo']} – ${prod['precio_final']}"
                )
            if check:
                seleccionados.append(prod)
                total += float(prod["precio_final"])

        if seleccionados:
            st.divider()
            # st.subheader(f"🧾 Total seleccionado: ${total:,.2f}")
        else:
            st.info("Seleccioná uno o más productos para ver el total.")
    else:
        st.warning(resultados[0])

if seleccionados:
    st.divider()
    st.subheader(f"🧾 Total seleccionado: ${total:,.2f}")

    if st.button("📄 Generar presupuesto PDF"):
        pdf = generar_presupuesto_pdf(seleccionados, total)
        st.download_button(
            label="⬇️ Descargar PDF",
            data=pdf,
            file_name="presupuesto_fresco.pdf",
            mime="application/pdf"
        )
# else:
#     st.info("Seleccioná uno o más productos para ver el total.")


# import streamlit as st
# from productos import obtener_productos

# st.set_page_config(page_title="Buscador de productos", layout="wide")

# st.title("🔧 Buscador de productos por auto")
# st.markdown("Completa los datos del vehículo para ver los productos compatibles.")

# # Formulario
# with st.form("formulario_auto"):
#     col1, col2 = st.columns(2)

#     with col1:
#         marca = st.text_input("Marca", placeholder="Ej: Toyota")
#         modelo = st.text_input("Modelo", placeholder="Ej: Corolla")

#     with col2:
#         motor = st.text_input("Motor", placeholder="Ej: 1.8")
#         anio = st.text_input("Año", placeholder="Ej: 2015")

#     buscar = st.form_submit_button("🔍 Buscar productos")

#Reemplazado por la región resultados
# if buscar:
#     if not (marca and modelo and motor and anio):
#         st.warning("⚠️ Completá todos los campos.")
#     else:
#         resultados = obtener_productos(marca, modelo, motor, anio)

#         if isinstance(resultados, list) and isinstance(resultados[0], dict):
#             st.success(f"✅ Se encontraron {len(resultados)} productos.")
#             st.dataframe(resultados, use_container_width=True)
#         else:
#             st.warning(resultados[0])


# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from productos import obtener_productos

# app = Flask(__name__)
# CORS(app)  # Permite que el frontend (HTML/JS) pueda hacer fetch sin problemas

# @app.route('/api/productos', methods=['POST'])
# def buscar_productos():
#     data = request.get_json()

#     marca = data.get("marca", "").strip()
#     modelo = data.get("modelo", "").strip()
#     motor = data.get("motor", "").strip()
#     anio = data.get("anio", "").strip()

#     productos = obtener_productos(marca, modelo, motor, anio)

#     return jsonify(productos)

# @app.route('/')
# def home():
#     return "✅ API de productos por auto funcionando"

# if __name__ == '__main__':
#     app.run(debug=True)


# # from flask import Flask, request, jsonify
# # from flask_cors import CORS
# # from productos import obtener_productos

# # app = Flask(__name__)
# # CORS(app)  # Habilita CORS para que el frontend pueda hacer fetch desde HTML local

# # @app.route('/api/productos', methods=['POST'])
# # def buscar_productos():
# #     data = request.get_json()

# #     # Extraer los campos del request
# #     marca = data.get("marca", "").strip()
# #     modelo = data.get("modelo", "").strip()
# #     motor = data.get("motor", "").strip()
# #     anio = data.get("anio", "").strip()

# #     resultados = obtener_productos(marca, modelo, motor, anio)
# #     return jsonify(resultados)

# # @app.route('/')
# # def home():
# #     return "✅ API de productos del lubricentro funcionando"

# # if __name__ == '__main__':
# #     app.run(debug=True)
