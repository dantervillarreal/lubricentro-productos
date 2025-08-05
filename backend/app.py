from flask import Flask, request, jsonify
from flask_cors import CORS
from productos import obtener_productos

app = Flask(__name__)
CORS(app)  # Permite que el frontend (HTML/JS) pueda hacer fetch sin problemas

@app.route('/api/productos', methods=['POST'])
def buscar_productos():
    data = request.get_json()

    marca = data.get("marca", "").strip()
    modelo = data.get("modelo", "").strip()
    motor = data.get("motor", "").strip()
    anio = data.get("anio", "").strip()

    productos = obtener_productos(marca, modelo, motor, anio)

    return jsonify(productos)

@app.route('/')
def home():
    return "✅ API de productos por auto funcionando"

if __name__ == '__main__':
    app.run(debug=True)


# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from productos import obtener_productos

# app = Flask(__name__)
# CORS(app)  # Habilita CORS para que el frontend pueda hacer fetch desde HTML local

# @app.route('/api/productos', methods=['POST'])
# def buscar_productos():
#     data = request.get_json()

#     # Extraer los campos del request
#     marca = data.get("marca", "").strip()
#     modelo = data.get("modelo", "").strip()
#     motor = data.get("motor", "").strip()
#     anio = data.get("anio", "").strip()

#     resultados = obtener_productos(marca, modelo, motor, anio)
#     return jsonify(resultados)

# @app.route('/')
# def home():
#     return "✅ API de productos del lubricentro funcionando"

# if __name__ == '__main__':
#     app.run(debug=True)
