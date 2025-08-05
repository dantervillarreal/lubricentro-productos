# Lubricentro - Buscador de productos por auto

Aplicación simple en Python + HTML para buscar productos (aceite, filtros, etc.) según el auto (marca, modelo, motor, año).

## 🧱 Estructura

- `backend/` contiene la API en Flask y los archivos `.csv` con la base de datos simulada
- `frontend/` contiene el HTML, CSS y JS del formulario

## ▶️ Cómo ejecutar

1. Entrar a la carpeta `backend`
2. Ejecutar el archivo `start.bat` (en Windows)
3. Abrir `frontend/index.html` en el navegador

## 🔗 Estructura de datos

- `autos.csv`: autos únicos
- `productos.csv`: catálogo completo
- `auto_productos.csv`: relación entre autos y productos

## 🔍 Próximos pasos

- Agregar creación de presupuestos
- Sugerencias automáticas
- Filtros por tipo de producto
- Conexión a base de datos real
