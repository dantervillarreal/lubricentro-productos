import csv
import os

# Cargar CSV con separador ;
def cargar_csv(nombre_archivo):
    ruta = os.path.join(os.path.dirname(__file__), nombre_archivo)
    with open(ruta, newline='', encoding='utf-8-sig') as archivo:
        return list(csv.DictReader(archivo, delimiter=';'))

# Cargar datos
autos = cargar_csv("autos.csv")
productos = cargar_csv("productos.csv")
auto_productos = cargar_csv("auto_productos.csv")

# Función principal: devuelve lista de productos según el auto
def obtener_productos(marca, modelo, motor, anio):
    # Buscar el id_auto que coincida
    id_auto = None
    for auto in autos:
        if (auto["marca"].strip().lower() == marca.strip().lower() and
            auto["modelo"].strip().lower() == modelo.strip().lower() and
            auto["motor"].strip() == motor.strip() and
            auto["anio"].strip() == anio.strip()):
            id_auto = auto["id_auto"]
            break

    if not id_auto:
        return ["❌ Auto no encontrado"]

    # Buscar los id_producto relacionados
    ids_producto = [rel["id_producto"] for rel in auto_productos if rel["id_auto"] == id_auto]

    # Buscar los productos correspondientes
    productos_encontrados = []
    for prod in productos:
        if prod["id_producto"] in ids_producto:
            productos_encontrados.append({
                "codigo": prod["codigo"],
                "descripcion": prod["descripcion"],
                "tipo": prod["tipo"],
                "precio_unit": prod["precio_unit"],
                "stock": prod["stock"],
                "precio_final": prod["precio_final"]
            })

    if not productos_encontrados:
        return ["❌ No hay productos cargados para este auto"]

    return productos_encontrados


# import csv
# import os

# def cargar_productos_csv():
#     ruta = os.path.join(os.path.dirname(__file__), "productos.csv")
#     productos = []

#     with open(ruta, newline='', encoding="utf-8-sig") as archivo:
#         lector = csv.DictReader(archivo, delimiter=';')  # 👈 aseguramos el delimitador
#         for fila in lector:
#             # Normalizamos campos esperados
#             fila_normalizada = {
#                 "marca": fila.get("marca", "").strip(),
#                 "modelo": fila.get("modelo", "").strip(),
#                 "motor": str(fila.get("motor", "")).strip(),
#                 "anio": str(fila.get("anio", "")).strip(),
#                 "productos": [p.strip() for p in fila.get("productos", "").split(",")]
#             }
#             productos.append(fila_normalizada)

#     return productos

# productos_db = cargar_productos_csv()

# def obtener_productos(marca, modelo, motor, anio):
#     for entrada in productos_db:
#         if (entrada["marca"].lower() == marca.lower() and
#             entrada["modelo"].lower() == modelo.lower() and
#             entrada["motor"] == motor and
#             entrada["anio"] == anio):
#             return entrada["productos"]
#     return ["No se encontraron productos para esos datos"]
