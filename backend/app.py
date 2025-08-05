import streamlit as st
from productos import obtener_productos

st.set_page_config(page_title="Buscador de productos", layout="wide")

st.title("🔧 Buscador de productos por auto")
st.markdown("Completa los datos del vehículo para ver los productos compatibles.")

# Formulario
with st.form("formulario_auto"):
    col1, col2 = st.columns(2)

    with col1:
        marca = st.text_input("Marca", placeholder="Ej: Toyota")
        modelo = st.text_input("Modelo", placeholder="Ej: Corolla")

    with col2:
        motor = st.text_input("Motor", placeholder="Ej: 1.8")
        anio = st.text_input("Año", placeholder="Ej: 2015")

    buscar = st.form_submit_button("🔍 Buscar productos")

if buscar:
    if not (marca and modelo and motor and anio):
        st.warning("⚠️ Completá todos los campos.")
    else:
        resultados = obtener_productos(marca, modelo, motor, anio)

        if isinstance(resultados, list) and isinstance(resultados[0], dict):
            st.success(f"✅ Se encontraron {len(resultados)} productos.")
            st.dataframe(resultados, use_container_width=True)
        else:
            st.warning(resultados[0])


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
